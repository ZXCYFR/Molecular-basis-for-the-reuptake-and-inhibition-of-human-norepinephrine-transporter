#!/bin/sh

cp ../LDP.log LDP.out
antechamber -i LDP.out -fi gout -o LDP.mol2 -fo mol2 -c resp -s 2 -rn LDP -at gaff2 -nc 1
rm -f ANTECHAMBER* QOUT qout punch ATOMTYPE.INF esout

parmchk2 -i LDP.mol2 -f mol2 -o LDP.frcmod
tleap -f leap.in
