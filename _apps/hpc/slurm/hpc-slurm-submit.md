---
title:  "Hpc Slurm Submission"
date: 2017-09-18 05:25:00
author: Vanessa Sochat
tags: 
- slurm
- scif
- hpc
- ubuntu
- debian
- singularity
---

```yaml
%apphelp hpc-slurm-submit
This will print (to the console) a slurm submission script.
Note that you can measure time using the %appinstall example,
or remove these lines and provide and export the variables
to the app's environment.

    singularity run --app slurm <container>

# add your email
    singularity run --app slurm <container> vsochat@stanford.edu

# save to file:
    singularity run --app slurm <container> >> <job-file>.job
    
# and then submit
    sbatch <job-file>.job

%appenv hpc-slurm-submit
DEBIAN_FRONTEND=noninteractive
export DEBIAN_FRONTEND

%appinstall hpc-slurm-submit
    apt-get update && apt-get install -y time
    TIME="TIME_HMS=%E\nMEMORY_KB=%M"
    export TIME

    ### 
    # This command assumes your container has a primary runscript.
    # You can change the path to be another if you like, or simply
    # don't estimate, just export the TIME_HMS and MEMORY_KB in
    # a new %appenv hpc-slurm-submit section
    ###
  
    SINGULARITY_APPNAME= /usr/bin/time -o times.txt /.singularity.d/actions/run

    IFS=''
    while read line
    do
    echo $line >> $SINGULARITY_ENVIRONMENT
    done < times.txt
    echo "export TIME_HMS MEMORY_KB" >> $SINGULARITY_ENVIRONMENT


%apprun hpc-slurm-submit
MEMORY_MB=$(echo "$(( ${MEMORY_KB%% *} / 1024))")
echo "#!/bin/bash"
echo "#SBATCH --nodes=1"
echo "#SBATCH -p normal"
echo "#SBATCH --qos=normal"
echo "#SBATCH --mem=$MEMORY_MB"
echo "#SBATCH --job-name=pokemon.job"
echo "#SBATCH --error=%j.err"
echo "#SBATCH --output=%j.out"
if [ $# -ne 0 ]
  then
    echo "#SBATCH --mail-user=$1"
fi
echo "#SBATCH --mail-type=ALL"
echo "#SBATCH --time=$TIME_HMS"
echo "module load singularity"
echo "singularity run $PWD/$SINGULARITY_CONTAINER"
echo "# example: run the job script command line:"
echo "# sbatch pokemon.job"
```
