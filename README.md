# find_files_on_SE
Search an alien directory for files that are on the specified SE

example format of the call:

find_local_data.py --alien-path /alice/sim/2020/LHC20b1b1/6/264076 --se-name LBL_HPCS

Will search subdirectories of /alice/sim/2020/LHC20b1b1/6/264076 for all files named root_archive.zip (default, can be changed with --fname arguement). 
For every file found, it check to see if it is on SE with a name containing the string LBL_HPCS

The output will give both the alien filename and the pfn on the SE. For example:

File = /alice/sim/2020/LHC20b1b1/6/264076/083/root_archive.zip PFN = root://alicemgm0.lbl.gov:1094//06/56258/fc0bf5e6-5205-11ea-8448-dfb8b396012b

Requires that process is run within the jalien environment & one should have a valid proxy certificate / jalien token.

For example, to set up for running script on Cori:  

shifter --image=mfasel/cc7-alice:latest --module=cvmfs bash
/cvmfs/alice.cern.ch/bin/alienv enter VO_ALICE@AliPhysics::vAN-20200529_JALIEN-1

[AliPhysics/vAN-20200529_JALIEN-1] ~ > alien.py
Enter PEM pass phrase:
Welcome to the ALICE GRID

AliEn[jporter]:/alice/cern.ch/user/j/jporter/ >exit
Exit
[AliPhysics/vAN-20200529_JALIEN-1] jalien_scripts > 


