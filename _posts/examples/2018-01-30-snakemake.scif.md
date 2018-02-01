---
layout: post
title:  "Snakemake and the Scientific Filesystem"
author: "@vsoch and @fbartusch"
date:   2018-01-30 11:13:01
github: https://github.com/sci-f/snakemake.scif
categories:
 - Examples
---

> Here is a story of snakemake, the workflow manager that could, and his partner in crime, the Scientific Filesystem!

What do you get when you combine a [Scientific Filesystem](https://sci-f.github.io), an organized, programmatically accessible, and discoverable specification for scientific applications, and [Snakemake](https://snakemake.readthedocs.io/en/latest/), a workflow management system is a tool to create scalable data analyses? In a container? Reproducibility, of course! Here we will go through a small tutorial to generate:

 - a scientific filesystem
 - in a container (Docker **and** Singularity!)
 - with Snakemake as a workflow manager.

<!--more-->


# Overview
The Scientific Filesystem (SCIF) is a host (or container) agnostic specification for a filesystem organization, set of environment variables, and functions to control them to make scientific applications discoverable, and easy to use. We are installing a SCIF via a shared SCIF recipe file, [snakemake_tutorial.scif](https://github.com/sci-f/snakemake.scif/blob/master/snakemake_tutorial.scif) that will install your scientific applications bwa, samtools, and the workflow management engine Snakemake workflow in **both** Docker and Singularity containers. If we need to make changes, we can just edit the **one file**. For a quick look at how the same commands are run between Docker and Singularity - below we have a Singularity container called `snakemake.simg` and a docker container `vanessa/snakemake.scif`. We will first start with a side by side quickstart, and then for interested readers, go through the details of each one with building separately for [Singularity](#Singularity) and then [Docker](#docker).

# Get recipe, workflow and test data

The repository contains all you need to reproduce the following tutorial. It contains the SCIF recipe file, the Snakemake tutorial workflow, and test data.

```
git clone https://github.com/sci-f/snakemake.scif.git
```

# Containers Side by Side
In summary:

> Two containers! One Recipe!


## Building containers

```
sudo singularity build snakemake.simg Singularity
```
```
docker build -t vanessa/snakemake.scif .
```

## Run the workflow 

The `Snakefile` specifies rules that should be executed. State a target file and Snakemake will build a directed acyclic graph (DAG) from the rules until the target file is reached. The rules are then executed to create the target file. The Snakefile hides the details of the environment provided by SCIF in the container as you can see from the commands below. All commands can be executed from outside the container or from within the container.

In all cases we bind the example dataset to the data directory provided by SCIF. SCIF provides the environment in which the workflow steps are executed. The workflow steps themself and therefore the interaction with SCIF is implemented in the Snakefile.

**Inside container, Singularity**

```
singularity shell --bind data/:/scif/data snakemake.simg
snakemake all
```

**Inside container, Docker**

To run the whole workflow we need the Snakefile which is not part of the container. To access the Snakefile from within the Docker container, we need an additional mount.

```
docker run -v $PWD/data:/scif/data:z -v $PWD:/working_dir -it -w /working_dir --entrypoint /bin/bash vanessa/snakemake.scif
snakemake all
```

<hr>

**Outside Container, Singularity**

```
singularity exec --bind data/:/scif/data snakemake.simg snakemake all
```

**Outside Container, Docker**

Because Docker does not mount the current working directory, we mount it to a the SCIF data directory of the SCIF snakemake app. The snakemake app will execute snakemake in `/scif/data/snakemake`, thus snakemake can find the Snakefile.

```
docker run -v $PWD/data:/scif/data:z -v $PWD:/scif/data/snakemake:z -it vanessa/snakemake.scif run snakemake all
```

## Generate graphical representation of the workflow

The whole workflow should finish within 5 seconds ... too fast to realize what is happening. A visualization of the whole workflow we just ran would be nice ...

The SCIF app `graphviz_create_dag` generates a directed acyclic graph of the workflow execution plan. This is a feature of Snakemake, but needs Graphviz as additional dependency. Therefore Graphviz is installed in the `appinstall` section of this app.

```
rm -r data/calls/ /data/mapped_reads/ data/sorted_reads/ data/report.html
```

Now we can generate the graph of the execution plan. The plan is computed from the Snakefile in our current working directory and the target file we specify. In this case we want to create the final report file
`report.html`. The directed acyclic graph of the workflow should be saved at`data/dag.svg`. The commands for Singularity and Docker are as follows:

**Singularity**

```
singularity run --bind data/:/scif/data snakemake.simg run graphviz_create_dag $PWD report.html dag.svg
> [graphviz_create_dag] executing /bin/bash /scif/apps/graphviz_create_dag/scif/runscript /home/fbartusch/github/snakemake_tutorial report.html dag.svg
> Building DAG of jobs...
```

**Docker**

In contrast to Singularity, Docker cannot access the current working directory. Therefore we mount the current working directory to the SCIF data folder of the `graphviz_create_dag` app.

```
docker run -v $PWD/data:/scif/data:z -v $PWD:/scif/data/graphviz_create_dag:z -it vanessa/snakemake.scif run graphviz_create_dag /scif/data/graphviz_create_dag report.html dag.svg
> [graphviz_create_dag] executing /bin/bash /scif/apps/graphviz_create_dag/scif/runscript /scif/data/graphviz_create_dag report.html dag.svg
> Building DAG of jobs...
```

## Map with bwa mem 

Instead of running the whole workflow at once with Snakemake, we can also use the SCIF environment to execute computations. The following examples also illustrate special SCIF syntax for working with environment variables or piping output to a file.
First, we map the reads with bwa mem to the reference genome.

**Inside container, Singularity** 

Note the use of `[e]` so we can easily pass the environment variable to the SCIF. Otherwise, it would be evaluated on the host.

```
singularity shell --bind data/:/scif/data snakemake.simg
mkdir /scif/data/mapped_reads
scif run bwa mem -o [e]SCIF_DATA/mapped_reads/A.sam [e]SCIF_DATA/genome.fa [e]SCIF_DATA/samples/A.fastq
```

**Inside container, Docker**

```
docker run -v $PWD/data:/scif/data:z -it --entrypoint /bin/bash vanessa/snakemake.scif
mkdir -p /scif/data/mapped_reads
scif run bwa mem -o [e]SCIF_DATA/mapped_reads/A.sam [e]SCIF_DATA/genome.fa [e]SCIF_DATA/samples/A.fastq
```

<hr>

**Outside container, Singularity**

```
mkdir -p data/mapped_reads
singularity run --bind data:/scif/data snakemake.simg run bwa mem -o [e]SCIF_DATA/mapped_reads/A.sam [e]SCIF_DATA/genome.fa [e]SCIF_DATA/samples/A.fastq
```

**Outside the container, Docker**

```
mkdir -p data/mapped_reads
docker run -v $PWD/data:/scif/data:z vanessa/snakemake.scif run bwa mem -o [e]SCIF_DATA/mapped_reads/A.sam [e]SCIF_DATA/genome.fa [e]SCIF_DATA/samples/A.fastq
```

## Sam to Bam Conversion

**Inside the container, Singularity**

Note the use of `[out]` as a substitute for `>`. If you wanted to use `>` you could put the entire thing in quotes.

```
singularity shell --bind data/:/scif/data snakemake.simg
scif run samtools view -Sb [e]SCIF_DATA/mapped_reads/A.sam [out] [e]SCIF_DATA/mapped_reads/A.bam    # or
scif run samtools 'view -Sb $SCIF_DATA/mapped_reads/A.sam > $SCIF_DATA/mapped_reads/A.bam'
> [samtools] executing /bin/bash /scif/apps/samtools/scif/runscript view -Sb $SCIF_DATA/mapped_reads/A.sam > $SCIF_DATA/mapped_reads/A.bam
```

**Inside the container, Docker**
```
docker run -v $PWD/data:/scif/data:z -it --entrypoint /bin/bash vanessa/snakemake.scif
scif run samtools view -Sb [e]SCIF_DATA/mapped_reads/A.sam [out] [e]SCIF_DATA/mapped_reads/A.bam    # or
scif run samtools 'view -Sb $SCIF_DATA/mapped_reads/A.sam > $SCIF_DATA/mapped_reads/A.bam'
> [samtools] executing /bin/bash /scif/apps/samtools/scif/runscript view -Sb $SCIF_DATA/mapped_reads/A.sam > $SCIF_DATA/mapped_reads/A.bam
```

<hr>

**Outside the container, Singularity**

```
singularity run --bind data:/scif/data snakemake.simg run samtools view -Sb [e]SCIF_DATA/mapped_reads/A.sam [out] [e]SCIF_DATA/mapped_reads/A.bam   # or
singularity run --bind data:/scif/data snakemake.simg run samtools 'view -Sb $SCIF_DATA/mapped_reads/A.sam > $SCIF_DATA/mapped_reads/A.bam'
```

**Outside the container, Docker**

```
docker run -v $PWD/data:/scif/data vanessa/snakemake.scif run samtools view -Sb [e]SCIF_DATA/mapped_reads/A.sam [out] [e]SCIF_DATA/mapped_reads/A.bam   # or
docker run -v $PWD/data:/scif/data vanessa/snakemake.scif run samtools 'view -Sb $SCIF_DATA/mapped_reads/A.sam > $SCIF_DATA/mapped_reads/A.bam'
```

## Interactive development
This can be done for Docker or Singularity, just with different commands to shell into the container!

```
docker run -it -v $PWD/data:/scif/data:z vanessa/snakemake.scif pyshell
singularity run --bind data/:/scif/data snakemake.simg pyshell
```

```
Found configurations for 4 scif apps
bwa
graphviz_create_dag
samtools
snakemake
[scif] /scif bwa | graphviz_create_dag | samtools | snakemake
Python 3.6.2 |Anaconda, Inc.| (default, Sep 22 2017, 02:03:08) 
[GCC 7.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> 

# Activate bwa 
client.activate('samtools')

# Environment variables active
client.environment

# Run bwa interactively
args = ['mem', '-o', '[e]SCIF_DATA/mapped_reads/a.sam', '[e]SCIF_DATA/genome.fa', '[e]SCIF_DATA/samples/A.fastq']
client.run('bwa', args=args)

# Run sam--bam interactively
args = ["view", "-Sb", "/scif/data/mapped_reads/r1_subset.sam", ">", "/scif/data/mapped_reads/r1_subset.bam"]
client.run('samtools', args=args)
```

See the Github repository <a href="https://github.com/sci-f/snakemake.scif" target="_blank">snakemake.scif</a> if you have any questions or issues.
