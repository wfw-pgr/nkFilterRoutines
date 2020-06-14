subroutine linearfilter2d( fxy, ret, alpha, LI, LJ )
  implicit none
  integer         , intent(in)  :: LI, LJ
  double precision, intent(in)  :: fxy(LI,LJ)
  double precision, intent(out) :: ret(LI,LJ)
  double precision, intent(in)  :: alpha
  double precision              :: denom
  integer                       :: i, j, ip1, im1, jp1, jm1
  
  denom = 1.d0 / ( 1.d0 + 4.d0*alpha + 4.d0*alpha**2 )
  do j=1, LJ
     jp1 = min( j+1, LJ )
     jm1 = max( j-1,  1 )
     do i=1, LI
        ip1 = min( i+1, LI )
        im1 = max( i-1,  1 )
        ret(i,j) =   denom    * ( fxy(i,j) &
             &     + alpha    * ( fxy(im1,j  ) + fxy(ip1,j  ) + fxy(i  ,jm1) + fxy(i  ,jp1) ) &
             &     + alpha**2 * ( fxy(im1,jm1) + fxy(ip1,jm1) + fxy(im1,jp1) + fxy(ip1,jp1) ) )
     enddo
  enddo
  
  return
end subroutine linearfilter2d
