#!/bin/bash

workdir=`pwd`
archivelocation=./
name=$(basename $workdir)
optstring=":l:n:"

while getopts ${optstring} arg; do
  case "${arg}" in

    l) archivelocation="${OPTARG}" ;;
    n) name="${OPTARG}" ;;
    ?)
      echo "Invalid option: -${OPTARG}." ;;
  esac
done

#get submission partition from EZTS config file
default_partition=$(grep "default_partition" utilities/config.py)
default_partition=${default_partition#*=}

echo -n "#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=EZTS-clean
#SBATCH --partition=$default_partition
#SBATCH --mem=10Gb
#SBATCH --output=EZTS-clean.o
#SBATCH --error=EZTS-clean.e
#SBATCH --time=1-00

cd $workdir

find $workdir -name '"*rwf"' -delete
find $workdir -name '"Gau*"' -delete
find $workdir -name '"*.chk"' -exec /work/lopez/g16/formchk {} \;
find $workdir -name '"*.chk"' -delete
find $workdir -name '"*gbw"' -delete
find $workdir -name '"*.*tmp*"' -delete
find $workdir -name '"*.scf*"' -delete
find $workdir -name '"*.prop*"' -delete

tar cf - lowest_ts | xz -z - > $1/$name-lowest_ts.tar.xz

" > EZTS-clean.sbatch

sbatch $workdir/EZTS-clean.sbatch
echo "Job submitted to archive and clean $workdir"

echo "Archive will be located at: $archivelocation/$name-lowest_ts.tar.xz"


