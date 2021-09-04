!---------------------------------------------------------------------
!---------------------------------------------------------------------

subroutine bt_scr_recover

!---------------------------------------------------------------------
! Recover BT state from previous checkpoints.
!---------------------------------------------------------------------

    use bt_data
    use mpinpb
    use scrnpb

    implicit none

    integer :: error
    integer :: readunit

    call timer_start(t_recover)

    ! Starts a restart.
    call scr_start_restart(ckptname, error)

    write (file_suffix, '(i5.5)') node

    fname = "bt.checkpoint."//trim(file_suffix)
    if (len_trim(scr_checkpoint_dir) .ne. 0) then
      fname = trim(scr_checkpoint_dir)//"/"//fname
    end if
    call scr_route_file(fname, fname_scr, error)

    print *, "Checkpoint file: ", fname_scr

    readunit = node
    open (unit=readunit, file=fname_scr, form='unformatted', action='read')
    ! Outer loop information recovery.
    read (readunit, iostat=ios) step
    read (readunit, iostat=ios) niter

    ! BT state recovery.
    read(readunit, iostat=ios) rho_i
    read(readunit, iostat=ios) square
    read(readunit, iostat=ios) forcing
    read(readunit, iostat=ios) u
    read(readunit, iostat=ios) rhs

!---------------------------------------------------------------------
!     Timer constants
!---------------------------------------------------------------------
    read(readunit, iostat=ios) timeron
    call recover_timers(node, ios)

    close (node)

    call scr_complete_restart(1, error)
    call timer_stop(t_recover)

    return
end subroutine bt_scr_recover

! ---------------------------------------------------------------------
! ---------------------------------------------------------------------

subroutine bt_scr_checkpoint

!---------------------------------------------------------------------
! Performs a checkpoint.
!---------------------------------------------------------------------

    use bt_data
    use mpinpb
    use scrnpb

    implicit none

    integer :: error
    integer :: writeunit
    integer :: need_checkpoint

    call scr_need_checkpoint(need_checkpoint, error)
    if (need_checkpoint .ne. 1) then
        return
    endif

    call timer_start(t_checkpoint)

    ! Starting a checkpoint.
    call scr_start_checkpoint(error)

    write (file_suffix, '(i5.5)') node

    fname = "bt.checkpoint."//trim(file_suffix)
    if (len_trim(scr_checkpoint_dir) .ne. 0) then
      fname = trim(scr_checkpoint_dir)//"/"//fname
    end if
    call scr_route_file(fname, fname_scr, error)

    writeunit = node
    open (unit=writeunit, file=fname_scr, form='unformatted', action='write')
    ! Outer loop information checkpoint.
    write (writeunit, iostat=ios) step
    write (writeunit, iostat=ios) niter

    ! BT state checkpoint.
    write(writeunit, iostat=ios) rho_i
    write(writeunit, iostat=ios) square
    write(writeunit, iostat=ios) forcing
    write(writeunit, iostat=ios) u
    write(writeunit, iostat=ios) rhs


!---------------------------------------------------------------------
!     Timer constants
!---------------------------------------------------------------------
    write(writeunit, iostat=ios) timeron
    call checkpoint_timers(node, ios)

    close (node)

    call scr_complete_checkpoint(1, error)
    call timer_stop(t_checkpoint)

    return
end subroutine bt_scr_checkpoint
