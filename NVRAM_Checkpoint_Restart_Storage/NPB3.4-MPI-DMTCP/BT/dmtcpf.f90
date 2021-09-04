
module dmtcpf

use iso_c_binding, only : C_CHAR, C_NULL_CHAR
implicit none

interface
  subroutine dmtcpf_checkpoint(string) bind(C, name="dmtcpc_checkpoint")
    use iso_c_binding, only: c_char
    character(kind=c_char) :: string(*)
  end subroutine dmtcpf_checkpoint
end interface

end module dmtcpf
