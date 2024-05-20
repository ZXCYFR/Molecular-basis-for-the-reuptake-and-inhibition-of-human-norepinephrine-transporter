#!/bin/sh

cp ../LNR.log LNR.out
antechamber -i LNR.out -fi gout -o LNR.mol2 -fo mol2 -c resp -s 2 -rn LNR -at gaff2 -nc 1
rm -f ANTECHAMBER* QOUT qout punch ATOMTYPE.INF esout

parmchk2 -i LNR.mol2 -f mol2 -o LNR.frcmod
tleap -f leap.in
