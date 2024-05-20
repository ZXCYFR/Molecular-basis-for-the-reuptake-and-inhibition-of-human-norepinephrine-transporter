#!/bash/sh

mkdir rmsd rmsd_LDP rmsf cluster distance

cpptraj pbc.in

cpptraj rmsd.in 
mv rmsd_*.out ./rmsd/

cpptraj rmsd_LDP.in 
mv rmsd_*.out ./rmsd_LDP/

cpptraj rmsf.in
mv rmsf_*.out ./rmsf/

cpptraj cluster.in
mv rep.c*.pdb cnumvtime.dat cpopvtime.agr summary.dat info.dat ./cluster/

cpptraj distance.in
mv distance*.out mindist_*.out distance
