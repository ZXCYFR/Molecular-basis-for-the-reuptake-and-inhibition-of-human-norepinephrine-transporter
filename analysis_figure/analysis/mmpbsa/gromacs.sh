#!/bash/sh

cpptraj pbc.in
cpptraj -p ../../../sys.prmtop -y prod_nopbc.nc -x prod.xtc
rm -f prod_nopbc.nc

acpype -p ../../../sys.prmtop -x ../../../sys.rst7 
mv ./sys.amb2gmx/sys_GMX.gro ./sys.gro
mv ./sys.amb2gmx/sys_GMX.top ./sys.top
rm -rf sys.amb2gmx

gmx editconf -f sys.gro -o sys.pdb

gmx make_ndx -f sys.gro 



