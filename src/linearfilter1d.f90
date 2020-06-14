subroutine linearfilter1d( data, ret, alpha, nFilter, LI )
  implicit none
  integer         , intent(in)  :: LI, nFilter
  double precision, intent(in)  :: data(LI)
  double precision, intent(out) :: ret(LI)
  double precision, intent(in)  :: alpha
  double precision              :: denom
  integer                       :: i, ip1, im1, k
  double precision, allocatable :: data_(:)

  allocate( data_(LI) )
  do i=1, LI
     ret(i) = data(i)
  enddo
  
  denom = 1.d0 / ( 1.d0 + 2.d0*alpha )
  do k=1, nFilter
     ! -- update data_ -- !
     do i=1, LI
        data_(i) = ret(i)
     enddo
     ! -- smoothing    -- !
     do i=1, LI
        ip1    = min( i+1, LI )
        im1    = max( i-1,  1 )
        ret(i) = denom * ( data_(i) + alpha*( data_(im1) + data_(ip1) ) )
     enddo
  enddo
  
  return
end subroutine linearfilter1d
