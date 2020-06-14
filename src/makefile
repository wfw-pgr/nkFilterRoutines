target = ../pylib.so
object = \
  linearfilter1d.f90 \
  linearfilter2d.f90

#FC = ifort
FC = gfortran

FFLAGS  = -O3 -fopenmp
LDFLAGS =
PYFLAGS = -shared -fPIC

.SUFFIXES: .so .f90
$(target): $(object)
	$(FC) $(PYFLAGS) $(FFLAGS) $(LDFLAGS) -o $(target) $(object)

.PHONY:all clean
clean:
	$(RM) $(target) 
all: clean $(target)
