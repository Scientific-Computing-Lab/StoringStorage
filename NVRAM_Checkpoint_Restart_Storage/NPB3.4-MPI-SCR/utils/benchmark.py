import argparse
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import timeit


class Environment(object):

    def __init__(self, logger, options):
        self.logger = logger
        self._options = options

    def _create_scr_directories(self):
        # Once the directory instance is deleted from memory, the temporary
        # directory, its inner directories and files are deleted as well.
        # Since the working directory is used througout the entire run, we must
        # keep a live reference to the temporary directory.
        self.logger.info('Creating SCR Directories...')
        self._scr_working_dir = tempfile.TemporaryDirectory(
            prefix=self._options.nvram_mount_directory)
        self._scr_cache_root_dir = tempfile.TemporaryDirectory(
            prefix=self._options.scr_cache_dir)

        self._scr_checkpoint_dir = os.path.join(
            self._scr_working_dir.name, 'checkpoints')
        os.mkdir(self._scr_checkpoint_dir)
        os.environ['SCR_CHECKPOINT_DIR'] = self._scr_checkpoint_dir
        self.logger.info('SCR checkpoint directory: %s',
                         self._scr_checkpoint_dir)

        self._scr_cache_dir = os.path.join(
            self._scr_cache_root_dir.name, 'cache')
        os.mkdir(self._scr_cache_dir)
        self.logger.info('SCR cache directory: %s', self._scr_cache_dir)


    def _create_scr_config_file(self):
        self._create_scr_directories()

        os.mkdir(os.path.join(self._scr_working_dir.name, 'ctrl'))

        self._scr_config_file = tempfile.NamedTemporaryFile(mode='w+')
        self._scr_config_file.writelines([
            f'DEBUG=2\n',

            f'SCR_FLUSH=1\n',
            f'SCR_CRC_ON_FLUSH=0\n',

            f'SCR_PREFIX = {self._scr_checkpoint_dir}\n',
            f'SCR_CACHE_BASE = {self._scr_cache_dir}\n'
        ])

        self._scr_config_file.flush()
        os.environ['SCR_CONF_FILE'] = self._scr_config_file.name

    def _compile_benchmark(self):
        try:
            self.logger.info('Compiling BT benchmark with CLASS: %s',
                             self._options.benchmark_class)
            output = subprocess.run(
                ['make', 'bt', f'CLASS={self._options.benchmark_class}'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            if os.path.exists('scr/bin'):
                self.logger.info('Cleaning up BT compilation binary files.')
                shutil.rmtree('scr/bin')
        except BaseException as ex:
            self.logger.warn('Failed cleaning BT binaries: %s', ex)

    def _clean_up_scr(self):
        self.logger.info('Cleaning up SCR checkpoint mapping files.')
        scr_map_files = os.path.join('/tmp', os.getenv('USER'), 'scr.defjobid')
        if os.path.exists(scr_map_files):
            shutil.rmtree(scr_map_files)
        if os.path.exists('.scr'):
            shutil.rmtree('.scr')

    def setup(self):
        self._create_scr_config_file()
        self._compile_benchmark()

    def teardown(self):
        self._clean_up_benchmarks()
        self._clean_up_scr()

    def run(self):
        with subprocess.Popen([
            'mpirun',
            '-np', str(self._options.procs),
            f'bin/bt.{self._options.benchmark_class}.x',
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as bt:
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
                bt.terminate()

    def recover(self):
        if not self._options.recover:
            return
        
        self.logger.info('Performing a recovery...')
        # Deleting checkpoints written to the cache to enforce recovery from 
        # the persistent memory.
        shutil.rmtree(self._scr_cache_dir)
        subprocess.run([
            'mpirun',
            '-np', str(self._options.procs),
            f'bin/bt.{self._options.benchmark_class}.x',
        ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nvram_mount_directory', type=str, action='store',
                        required=True, help='The mount directory of nvram.')
    parser.add_argument('--scr_cache_dir', type=str, action='store',
                        help='The cache directory of SCR.', default='/dev/shm/')
    parser.add_argument('-c', '--benchmark_class', type=str, action='store', required=True,
                        help='The benchmark class')
    parser.add_argument('-p', '--procs', action='store', type=int, default=1,
                        help='The number of processes to run the benchmark with.')

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
        start = timeit.default_timer()
        env.run()
        env.recover()
        end = timeit.default_timer()
        logging.getLogger("main").info("Total run-time: %s", end - start)


if __name__ == '__main__':
    main()
