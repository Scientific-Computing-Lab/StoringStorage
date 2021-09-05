import argparse
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile


class Environment(object):

    def __init__(self, logger, options):
        self.logger = logger
        self._options = options

    def _create_dmtcp_directories(self):
        # Once the directory instance is deleted from memory, the temporary
        # directory, its inner directories and files are deleted as well.
        # Since the working directory is used througout the entire run, we must
        # keep a live reference to the temporary directory.
        self.logger.info('Creating DMTCP Directories...')
        self._dmtcp_working_dir = tempfile.TemporaryDirectory(
            prefix=self._options.nvram_mount_directory)

        self._dmtcp_checkpoint_dir = os.path.join(
            self._dmtcp_working_dir.name, 'checkpoints')
        os.mkdir(self._dmtcp_checkpoint_dir)
        self.logger.info('DMTCP checkpoint directory: %s',
                         self._dmtcp_checkpoint_dir)

        self._dmtcp_tmp_dir = os.path.join(self._dmtcp_working_dir.name, 'tmp')
        os.mkdir(self._dmtcp_tmp_dir)
        self.logger.info('DMTCP tmp directory: %s', self._dmtcp_tmp_dir)

    def _compile_benchmark(self):
        try:
            self.logger.info('Compiling BT benchmark with CLASS: %s',
                             self._options.benchmark_class)
            output = subprocess.run(
                ['make', 'bt', f'CLASS={self._options.benchmark_class}'])
            self.logger.info('BT benchmark compiled succesfully.')
        except subprocess.CalledProcessError:
            self.logger.error('BT benchmark compilation failed.')

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc, value, tb):
        self.teardown()

    def _clean_up_benchmarks(self):
        self.logger.info('Cleaning up BT compilation object files.')
        output = subprocess.run(['make', 'clean'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            if os.path.exists('dmtcp/bin'):
                self.logger.info('Cleaning up BT compilation binary files.')
                shutil.rmtree('dmtcp/bin')
        except BaseException as ex:
            self.logger.warn('Failed cleaning BT binaries: %s', ex)

    def _clean_up_dmtcp(self):
        self.logger.info('Cleaning up DMTCP checkpoint mapping files.')
        dmtcp_map_files = os.path.join(
            '/tmp', f'dmtcp-{os.getenv("USER")}@{os.getenv("HOSTNAME")}')
        if os.path.exists(dmtcp_map_files):
            shutil.rmtree(dmtcp_map_files)
        if os.path.exists('.dmtcp'):
            shutil.rmtree('.dmtcp')

    def setup(self):
        self. _create_dmtcp_directories()
        self._compile_benchmark()

    def teardown(self):
        self._clean_up_benchmarks()
        self._clean_up_dmtcp()

    def run(self):
        # We explicitly use subprocess.POpen in order to run the coordinator as a background process.
        with subprocess.Popen([
            f'dmtcp_coordinator',
            f'--exit-on-last',
            f'--coord-port', str(self._options.coord_port),
            f'--tmpdir', self._dmtcp_tmp_dir,
            f'--ckptdir', self._dmtcp_checkpoint_dir,
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as coordinator:
            bt = subprocess.Popen([
                f'dmtcp_launch',
                f'--allow-file-overwrite',
                f'--no-gzip',
                f'--join-coordinator',
                f'--coord-port', str(self._options.coord_port),
                f'--tmpdir', self._dmtcp_tmp_dir,
                f'--ckptdir', self._dmtcp_checkpoint_dir,

                f'mpirun',
                f'-np', str(self._options.procs),
                f'./bin/bt.{self._options.benchmark_class}.x',
            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time_step_regex = re.compile('Time step\s+(\d+)')
            while bt.poll() is None:
                line = bt.stdout.readline()
                if not line:
                    continue
                line = line.decode('utf8').strip()
                print(line)

                # Checking if we should crash.
                if not self._options.crash:
                    continue

                match = time_step_regex.match(line)
                if not match:
                    continue
                time_step = int(match.group(1))
                if time_step != self._options.crash_iteration:
                    continue

                self.logger.info('Performing a crash...')
                subprocess.run(['dmtcp_command', '--coord-port',
                               str(self._options.coord_port), '--kill'])

    def recover(self):
        if not self._options.recover:
            return
        self.logger.info('Performing a recovery...')

        # We explicitly use subprocess.POpen in order to run the coordinator as a background process.
        with subprocess.Popen([
            f'dmtcp_coordinator',
            f'--exit-on-last',
            f'--coord-port', str(self._options.coord_port),
            f'--tmpdir', self._dmtcp_tmp_dir,
            f'--ckptdir', self._dmtcp_checkpoint_dir,
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as coordinator:
            bt = subprocess.run([
                os.path.join(self._dmtcp_checkpoint_dir,
                             'dmtcp_restart_script.sh'),
                f'--coord-port', str(self._options.coord_port),
                f'--tmpdir', self._dmtcp_tmp_dir,
                f'--ckptdir', self._dmtcp_checkpoint_dir,
                f'--restartdir', self._dmtcp_checkpoint_dir,
            ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nvram-mount-directory', type=str, action='store',
                        required=True, help='The mount directory of nvram.')
    parser.add_argument('-c', '--benchmark-class', type=str, action='store', required=True,
                        help='The benchmark class.')
    parser.add_argument('-p', '--procs', action='store', type=int, default=1,
                        help='The number of processes to run the benchmark with.')
    parser.add_argument('-o', '--coord_port', action='store', type=int, default=1,
                        help='The checkpoint interval to run the benchmark with.')

    parser.add_argument('--crash', action='store_true', dest='crash',
                        help='If set, the benchmark would perform a crash at the specified iteration.')
    parser.add_argument('--no-crash', action='store_false', dest='crash',
                        help='If set, the benchmark would not perform a crash.')
    parser.add_argument('-i', '--crash-iteration', action='store', type=int, default=-1,
                        help='The iteration to crash/restart the benchmark.')

    parser.add_argument('--recover', action='store_true', dest='recover',
                        help='If true, the benchmark would perform a recovery after a crash.')
    parser.add_argument('--no-recover', action='store_false', dest='recover',
                        help='If true, the benchmark would not perform a recovery after a crash.')

    parser.set_defaults(crash=False, recover=False)
    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stdout,
        level=os.environ.get("LOGLEVEL", "INFO"),
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    with Environment(logger=logging.getLogger('environment'), options=args) as env:
        env.run()
        env.recover()


if __name__ == '__main__':
    main()
