!---------------------------------------------------------------------
!---------------------------------------------------------------------
!
!  scrnpb module
!
!---------------------------------------------------------------------
!---------------------------------------------------------------------

module scrnpb

    include 'scrf.h'

    character*1024 :: fname, file_suffix
    character(len=SCR_MAX_FILENAME) :: fname_scr
    character(len=SCR_MAX_FILENAME) :: ckptname

    integer(kind=4) :: flag; 
    integer(kind=4) :: valid; 
    integer :: ios

    ! The outer computational state.
    integer :: step = 1
    integer :: niter


    character(len=255) :: scr_checkpoint_dir
    
end module scrnpb

