---
title:  "Hpc Sge Submission"
date: 2017-09-18 05:25:00
author: Vanessa Sochat
tags: 
- sge
- scif
- hpc
- ubuntu
- debian
- singularity
---

```yaml
%apphelp hpc-sge-submit
This will print (to the console) an sge submission script.
Note that you can measure time using the appinstall example,
or remove these lines and provide and export the variables
to the app's environment.

    singularity run --app hpc-sge-submit <container>

# add your email
    singularity run --app hpc-sge-submit <container> vsochat@stanford.edu

# save to file:
    singularity run --app hpc-sge-submit <container> >> <job-file>.job
    
# add other arguments
    singularity run --app hpc-sge-submit <container> -q normal

# Run
    qsub <job-file>.job


%appenv hpc-sge-submit
DEBIAN_FRONTEND=noninteractive
export DEBIAN_FRONTEND


%appinstall hpc-sge-submit
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


%apprun hpc-sge-submit
MEMORY_MB=$(echo "$(( ${MEMORY_KB%% *} / 1024))")
echo "#!/bin/bash"
echo "# run_job.sh"
echo "module load singularity"
echo "singularity run $PWD/$SINGULARITY_CONTAINER"
echo "# submission command"
QUEUE="-q normal"
if [ $# -ne 0 ]
  then
    QUEUE=$1
fi
echo "# qsub $QUEUE -w e -N pokemon.job -l h_vmem=${MEMORY_MB}G -l h_rt=$TIME_HMS -o pokemon.out -e pokemon.err run_job.sh"
```
