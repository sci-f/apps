---
layout: post
title:  "CarrierSeq: sequence analysis workflow with SCIF"
author: Vanessasaurus
date:   2018-01-31 11:12:01 -0600
github: https://github.com/vsoch/carrierseq/tree/master
categories:
 - Examples
---

Some time ago we featured the [CarrierSeq workflow](https://sci-f.github.io/apps/examples/carrierseq) run with Singularity. At the time, SCIF was available only for Singularity, and with great feedback from reviewers and the community, SCIF (the Scientific Filesystem) was re-fashioned to be install-able in any container technology (Docker or Singularity) or on your host! 

Just to hammer it into your brain, I'll remind you what the Scientific Filesystem, referred to as SCIF, is. SCIF is a specification for a filesystem organizational, a set of environment variables, and functions that control the two in order to optimize the usability and discoverability of scientific applications. Thus, in this second tutorial we are again going to install a Scientific Filesystem into a Docker container **and the same one** into a Singularity container **using the same scif recipe file**.

<!--more--> 

# Overview
The Scientific Filesystem (SCIF) is a host (or container) agnostic specification for a filesystem organization, set of environment variables, and functions to control them to make scientific applications discoverable, and easy to use. We are installing a SCIF via a shared SCIF recipe file, [carrierseq.scif](https://github.com/vsoch/carrierseq/blob/master/carrierseq.scif) that defines applications for mapping, poisson, and other helpers into **both** a Docker and Singularity container. If we need to make changes, we can just edit the **one file**. For each, we will build a development container (with tools like samtools and bwa exposed as entrypoints) and a pipeline production container (to put those commands together to run a step like "mapping." For a quick look at how the same commands are run between Docker and Singularity - below we have a Singularity container called `cseq` and a docker container `vanessa/cseq`. For the detailed walkthroughs, jump down to [Details](#details).


## CarrierSeq Pipeline Container
List apps in container

```
$ ./cseq apps
$ docker run vanessa/cseq apps

  download
      help
   mapping
   poisson
    readme
 reference
   sorting

```

Ask for help for the application called "readme"

```
$ ./cseq help readme
$ docker run vanessa/cseq help readme
```

Print the repository's README.md to the console

```
$ ./cseq run readme
$ docker run vanessa/cseq run readme

#### CarrierSeq
#### About

bioRxiv doi: https://doi.org/10.1101/175281

CarrierSeq is a sequence analysis workflow for low-input nanopore
            sequencing which employs a genomic carrier.

           Github Contributors: Angel Mojarro (@amojarro), 
                                Srinivasa Aditya Bhattaru (@sbhattaru), 
                                Christopher E. Carr (@CarrCE), 
                                and Vanessa Sochat (@vsoch).
 
fastq-filter from: https://github.com/nanoporetech/fastq-filter

[MORE]
```

Inspect the container

```
$ ./cseq inspect
$ docker run vanessa/cseq inspect
```

or a single scientific application

```
$ cseq inspect mapping
$ docker run vanessa/cseq inspect mapping
```

Run three entrypoints in a row, and bind a data directory

```
$ singularity run --bind data:/scif/data cseq run mapping
$ singularity run --bind data:/scif/data cseq run poisson
$ singularity run --bind data:/scif/data cseq run sorting

$ docker run -v $PWD/data:/scif/data vanessa/cseq run mapping
$ docker run -v $PWD/data:/scif/data vanessa/cseq run poisson
$ docker run -v $PWD/data:/scif/data vanessa/cseq run sorting
```

Create an interactive session with an application context

```
$ ./cseq shell mapping
$ docker run -it vanessa/cseq shell mapping
```

## CarrierSeq Development Container

List applications

```
$ docker run vanessa/cseq:dev apps
$ ./cseq-dev apps
       bwa
    fqtrim
      help
    python
     seqtk
sra-toolkit
```

Open interactive python

```
$ ./cseq-dev run python
$ docker run -it vanessa/cseq:dev run python
[python] executing /bin/bash /scif/apps/python/scif/runscript
Python 2.7.9 (default, Jun 29 2016, 13:08:31) 
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Load container with bwa on path

```
$ ./cseq-dev shell bwa
$ docker run -it vanessa/cseq:dev shell bwa
[bwa] executing /bin/bash 
$ which bwa
$ /scif/apps/bwa/bin/bwa
```

# Details
This tutorial assumes that you are familiar with and have Docker installed on your machine. You also need to download some data files to use with your container. If you aren't familar with genomic analysis (as I'm not) you will be utterly confused about how to download data. The reference is provided in the "reference" folder of the repository, but the input data isn't. The container was originally designed to download it's own data, but due to a <a href="https://github.com/amojarro/carrierseq/issues/1" target="_blank">change in the sri-toolkit</a> the original data is provided as a manual <a href="https://www.dropbox.com/sh/vyor82ulzh7n9ke/AAC4W8rMe4z5hdb7j4QhF_IYa?dl=0" target="_blank">download link from Dropbox</a>.


## The SCIF Recipe
Let's take a look at a (truncated) application definition in the scif carrierseq recipe, [carrierseq.scif](https://github.com/vsoch/carrierseq/blob/master/carrierseq.scif).

```
%appinstall mapping
    # Install bwa
    git clone https://github.com/lh3/bwa.git build
    cd build && git checkout v0.7.15
    make
    mv -t ../bin bwa bwakit   
    # Install fqtrim
    cd .. 
    wget https://ccb.jhu.edu/software/fqtrim/dl/fqtrim-0.9.5.tar.gz
    tar xvfz fqtrim-0.9.5.tar.gz && cd fqtrim-0.9.5 && make release
    mv fqtrim ../bin

%appenv mapping
    all_reads=$SCIF_DATA/all_reads.fastq
    bwa_threads=${CSEQ_BWATHREADS:-1}
    q_score=${CSEQ_QSCORE:-9}
    output_folder=$SCIF_DATA
    export all_reads reference_genome bwa_threads q_score output_folder

%appfiles mapping
    /python/quality_score_filter.py bin/quality_score_filter.py
%apprun mapping
    source $SCIF_APPENV_reference

    # Create all input directories
    mkdir -p $SCIF_DATA/00_bwa # map all reads to carrier reference genome
...
```

We have sections like these for each internal module (a SCIF application) that we want to create. The above is for the application "mapping." These definitions are in the file `carrierseq.scif` and when we create the SCIF in the container it starts empty. We then install the recipe to the container. [Here](https://github.com/vsoch/carrierseq/blob/master/carrierseq.scif) is the recipe ( `carrierseq.scif`) and installing it to (any) container comes down to installing the scif client, and pointing it at the recipe.

```
pip install scif
scif install carrierseq.scif
```

After installation, all the steps in `appinstall`s are performed, the various metadata, environments, and entry point run scripts are created, and we are ready to go! Let's see what this looks like when done in a Singularity and Docker container.


# CarrierSeq Scientific Filesystem (Singularity)
Singularity is a container, similar to Docker, that is secure to run in HPC environments. By way of using a Scientific Filesystem (SCIF) with Singularity, we have a lot of freedom in deciding on what level of functions we want to expose to the user. A developer will want easy access to the core tools (e.g., bwa, seqtk) while a user will likely want one level up, on the level of a collection of steps associated with some task (e.g., mapping). We will walk through the steps of building and using each one.

## Setup
You first need to install Singularity. For this tutorial, we are using the development branch with the current version 2.4.x. You can install it doing the following.

```
git clone -b development https://www.github.com/singularityware/singularity.git
cd singularity
./autogen.sh
./configure --prefix=/usr/local
make
sudo make install
```

Now you are ready to go! If the above steps tell you to install any missing dependencies, you should do that.


## Build the image
Building looks like this:

```
sudo singularity build cseq Singularity
```

This will build a read only (essentially frozen) image, so your pipeline is forever preserved.


## Exploring the Container
If you didn't know anything about the image, you would want to explore it. SCIF 
provides easy commands to do that. When we just execute the container, the SCIF shows us
it's default help:

```
./cseq 
[help] executing /bin/bash /scif/apps/help/scif/runscript
    CarrierSeq is a sequence analysis workflow for low-input nanopore
    sequencing which employs a genomic carrier.
    Github Contributors: Angel Mojarro (@amojarro),
                         Srinivasa Aditya Bhattaru (@sbhattaru),
                         Christopher E. Carr (@CarrCE),
                         Vanessa Sochat (@vsoch).
    fastq-filter from: https://github.com/nanoporetech/fastq-filter
    To see applications installed in the Scientific Filesystem:
    scif apps
    To run a typical pipeline, you might do:
    scif run mapping
    scif run poisson
    scif run sorting
    If you install in a container, the entrypoint should be scif, and then
    issue the above commands to it.
```

### SCI-F Apps

You can see apps in the image, as instructed:

```
./cseq apps
  download
      help
   mapping
   poisson
    readme
 reference
   sorting
```

or see help for a specific app. For example, readme exists only to capture and then
print the entire readme of the repository (or any repository container README.md for
which the SCIF is installed for) to the console:

```
./cseq run readme | tail
The matrix illustrates the reads/channel distribution of B. subtilis, contamination, and HQNRs across all 512 nanopore channels. Here we are able to visually identify overly productive channels (e.g., 191 reads/channel, etc) producing likely HQNRs.
![alt text](https://github.com/amojarro/carrierseq/blob/master/example/carrierseq_roi_q9_p005.png)

### HQNR Pore Occupancy
“Bad” channels identified by CarrierSeq as HQNR-associated (reads/channel > 7).
![alt text](https://github.com/amojarro/carrierseq/blob/master/example/carrierseq_hqnrs_q9_p005.png)

### Target Reads Pore Occupancy
“Good” channels identified by CarrierSeq as non-HQNR-associated (reads/channel ≤ 7). Channels producing 6 or more reads yield HQNRs that have satisfied our CarrierSeq parameters. By imposing a stricter p-value, CarrierSeq may be able to reject more HQNRs (e.g., xcrit = 5).
![alt text](https://github.com/amojarro/carrierseq/blob/master/example/carrierseq_target_reads_q9_p005.png)
```

And then we can ask for help for any of the pipeline steps:

```
./cseq help download
```

We can also look at metadata for the entire image, or for an app.  The inspect
command can expose environment variables, labels, the definition file, tests, and
runscripts.

```
# Returns a large data structure with all apps
./cseq inspect

# Returns for a particular app
./cseq inspect download
{
    "download": {
        "apphelp": [
            "   The original sra-toolkit does not serve the correct data, so for now you ",
            "   should download data from ",
            "   https://www.dropbox.com/sh/vyor82ulzh7n9ke/AAC4W8rMe4z5hdb7j4QhF_IYa?dl=0) and then move into some data folder you intend to mount:",
            "      mv $HOME/Downloads/all_reads.fastq data/"
        ]
    }
}
```

## Overall Strategy
Since the data is rather large, we are going to map a folder to our $PWD where the analysis is to run. This directory, just like the modular applications, has a known and predictable location. So our steps are going to look like this:

```
# 0. Make an empty random folder to bind to for data.
mkdir data

# 1. Download data, map the data base to an empty folder on our local machine
#     (we actually will do this from the browser as the sri toolkit is changed.
# 2. Perform mapping step of pipeline, mapping the same folder.
# 3. perform poisson regression on filtered reads
# 4. Finally, sort results

# Download data from https://www.dropbox.com/sh/vyor82ulzh7n9ke/AAC4W8rMe4z5hdb7j4QhF_IYa?dl=0
# See issue --> https://github.com/amojarro/carrierseq/issues/1
cseq="singularity run --bind data:/scif/data cseq"

# $cseq run <app>
```

## CarrierSeq Pipeline
The common user might want access to the larger scoped pipeline that the software provides. In the case of CarrierSeq, this means (optionally, download) mapping, poisson, and then sorting. If the image isn't provided (e.g., a Singularity Registry or Singularity Hub) the user can build from the build recipe file, `Singularity.devel`. If you haven't done this already:

```
sudo singularity build cseq Singularity.devel
```

The author is still working on updating the automated download, for now download from [here](https://www.dropbox.com/sh/vyor82ulzh7n9ke/AAC4W8rMe4z5hdb7j4QhF_IYa?dl=0) and then move into some data folder you intend to mount:

```
mv $HOME/Downloads/all_reads.fastq data/
```

Let's be lazy and put the bind and singularity command into an environment variable so we don't need
to type it many times.

```
cseq="singularity run --bind data:/scif/data cseq"
```

And then the various steps of the pipeline are run as was specified above:

```
$cseq run mapping
$cseq run poisson
$cseq run sorting
```

There are even helper functions that the main ones use to get various environments. For example, the `reference` app serves only to return the path to the reference genome!

```
$ ./cseq exec reference echo [e]reference_genome
[reference] executing /bin/echo $reference_genome
$SCIF_APPROOT_reference/lambda_ecoli.fa
```

or run quietly

```
$ ./cseq --quiet exec reference echo [e]reference_genome
$SCIF_APPROOT_reference/lambda_ecoli.fa
```
and what is that evaluated to?

```
./cseq --quiet exec reference echo [e]SCIF_APPROOT_reference/lambda_ecoli.fa
/scif/apps/reference/lambda_ecoli.fa
```

Cool!


### 1. Mapping
To run mapping, bind the data folder to the image, and specify the app to be mapping:

```
singularity run --bind data:/scif/data cseq run mapping
```

## 2. Poisson

```
singularity run --bind data:/scif/data cseq run poisson
```

## 3. Sorting

```
singularity run --bind data:/scif/data cseq run sorting
```


## How Can I Change It?
Given two containers that share the same input and output schema, I could
swap out of the steps:


```
...
singularity run --bind data:/scif/data container1 run sorting
singularity run --bind data:/scif/data container2 run sorting
```

or even provide a single container with multiple options for the same step


```
...
singularity run --bind data:/scif/data cseq run sorting1
singularity run --bind data:/scif/data cseq run sorting2
```

As a user, you want a container that exposes enough metadata to run different steps of the pipeline, but you don't want to need to know the specifics of each command call or path within the container. In the above, I can direct the container to my mapped input directory
and specify a step in the pipeline, and I dont need to understand how to use `bwa` or `grep` or `seqtk`, or any of the other software
that makes up each.


### Interactive Environment
If you are curious about all the Scientific Filesystem variables available to you:

```
$cseq exec mapping env | grep SCIF_
```

and read [the specification](https://sci-f.github.io/specification) for a complete list.

Or if you wanted an interactive shell to explore running commands inside the container:

```
singularity shell --bind data:/scif/data cseq
```

or enter a shell in context of a scif application (mapping)

```
$ singularity run cseq shell mapping
$ echo $SCIF_APPNAME
mapping
```

## CarrierSeq Development
The developer has a different use case - to have easy command line access to the lowest level of executables installed in the container. Given a global install of all software, without SCI-F I would need to look at `$PATH` to see what has been added to the path, and then list executables in path locations to find new software installed to, for example, `/usr/bin`. There is no way to easily and programatically "sniff" a container to understand the changes, and the container is a black development box, perhaps only understood by the creator or with careful inspection of the build recipe.

In this use case, we want to build the development container.

```
sudo singularity build carrierseq.dev.img Singularity.devel
```

Now when we look at apps, we see all the core software that can be combined in specific ways to produce a pipeline step like "mapping".

```
singularity apps carrierseq.dev.img
bwa
fqtrim
python
seqtk
sra-toolkit
```

each of which might be run, exec to activate the app environment, or shell to shell into the container under the context of a specific app:

```
# Open interactive python
singularity run --app python carrierseq.dev.img

# Load container with bwa on path
$ singularity shell --app bwa carrierseq.dev.img
$ which bwa
$ /scif/apps/bwa/bin/bwa
```

These two images that serve equivalent software is a powerful example of the flexibility of SCI-F. The container creator can choose the level of detail to expose to a user that doesn't know how it was created, or perhaps has varying levels of expertise. A lab that is using core tools for working with sequence data might have preference for the development container, while a finalized pipeline distributed with a publication would have preference for the first. In both cases, the creator doesn't need to write custom scripts for a container to run a particular app, or to expose environment variables, tests, or labels. By way of using SCI-F, this happens automatically. 

# CarrierSeq Scientific Filesystem (Docker)

## Build the image
Building looks like this. Notice that we aren't using the primary Dockerfile](https://github.com/vsoch/carrierseq/blob/master/Dockerfile) in the repository, we are using the [Dockerfile.scif](https://github.com/vsoch/carrierseq/blob/master/Dockerfile.scif) that is the version for the Scientific Filesystem.

```
docker build -f Dockerfile.scif -t vanessa/cseq .
```

## Exploring the Container
If you didn't know anything about the image, you would want to explore it. SCIF 
provides easy commands to do that. 
Let's also define a quicker entry point to using the container:

```
cseq="docker run vanessa/cseq"
```

If we didn't know anything and executed the container, we would see the scif client, and it would give us the following commands.

```
$cseq
```

### SCI-F Apps

You can see apps in the image:

```
$cseq apps
  download
      help
   mapping
   poisson
    readme
 reference
   sorting
```

or see help for a specific app. For example, readme exists only to capture and then
print the entire readme of the repository (or any repository container README.md for
which the SCIF is installed for) to the console:

```
$cseq run readme | tail
The matrix illustrates the reads/channel distribution of B. subtilis, contamination, and HQNRs across all 512 nanopore channels. Here we are able to visually identify overly productive channels (e.g., 191 reads/channel, etc) producing likely HQNRs.
![alt text](https://github.com/amojarro/carrierseq/blob/master/example/carrierseq_roi_q9_p005.png)

### HQNR Pore Occupancy
"Bad" channels identified by CarrierSeq as HQNR-associated (reads/channel > 7).
![alt text](https://github.com/amojarro/carrierseq/blob/master/example/carrierseq_hqnrs_q9_p005.png)

### Target Reads Pore Occupancy
"Good" channels identified by CarrierSeq as non-HQNR-associated (reads/channel ≤ 7). Channels producing 6 or more reads yield HQNRs that have satisfied our CarrierSeq parameters. By imposing a stricter p-value, CarrierSeq may be able to reject more HQNRs (e.g., xcrit = 5).
![alt text](https://github.com/amojarro/carrierseq/blob/master/example/carrierseq_target_reads_q9_p005.png)
```

And then we can ask for help for any of the pipeline steps:

```
$cseq help download
```

We can also look at metadata for the entire image, or for an app.  The inspect
command can expose environment variables, labels, the definition file, tests, and
runscripts.

```
# Returns a large data structure with all apps
$cseq inspect

# Returns for a particular app
$cseq inspect download
{
    "download": {
        "apphelp": [
            "   The original sra-toolkit does not serve the correct data, so for now you ",
            "   should download data from ",
            "   https://www.dropbox.com/sh/vyor82ulzh7n9ke/AAC4W8rMe4z5hdb7j4QhF_IYa?dl=0) and then move into some data folder you intend to mount:",
            "      mv $HOME/Downloads/all_reads.fastq data/"
        ]
    }
}
```

## Overall Strategy
Since the data is rather large, we are going to map a folder to our $PWD where the analysis is to run. This directory, just like the modular applications, has a known and predictable location. So our steps are going to look like this:

```
# 0. Make an empty random folder to bind to for data.
mkdir data
```
1. Download data, map the data base to an empty folder on our local machine
     (we actually will do this from the browser as the sri toolkit is changed.
2. Perform mapping step of pipeline, mapping the same folder.
3. perform poisson regression on filtered reads
4. Finally, sort results

Let's add a volume to our command:

```
cseq="docker run -v $PWD/data:/scif/data vanessa/cseq"
```

## CarrierSeq Pipeline
The common user might want access to the larger scoped pipeline that the software provides. In the case of CarrierSeq, this means (optionally, download) mapping, poisson, and then sorting. If the image isn't provided (e.g., a Singularity Registry or Singularity Hub) the user can build from the build recipe file, `Singularity`. If you haven't done this already:

```
docker build -t vanessa/cseq .
```

The author is still working on updating the automated download, for now download from [here](https://www.dropbox.com/sh/vyor82ulzh7n9ke/AAC4W8rMe4z5hdb7j4QhF_IYa?dl=0) and then move into some data folder you intend to mount:

``
mv $HOME/Downloads/all_reads.fastq data/
```

Let's be lazy and put the bind and singularity command into an environment variable so we don't need
to type it many times.

```
cseq="docker run -v $PWD/data:/scif/data vanessa/cseq"
```

And then the various steps of the pipeline are run as was specified above:

```
$cseq run mapping
$cseq run poisson
$cseq run sorting
```

### 1. Mapping
To run mapping, bind the data folder to the image, and specify the app to be mapping:

```
cseq="docker run -v $PWD/data:/scif/data vanessa/cseq"
$cseq run mapping
```

## 2. Poisson

```
cseq="docker run -v $PWD/data:/scif/data vanessa/cseq"
$cseq run poisson
```

## 3. Sorting

```
cseq="docker run -v $PWD/data:/scif/data vanessa/cseq"
$cseq run sorting
```


## How Can I Change It?
Given two containers that share the same input and output schema, I could
swap out of the steps:


```
...
docker run -v $PWD/data:/scif/data vanessa/cseq run sorting
docker run -v $PWD/data:/scif/data vanessa/another run sorting
```

or even provide a single container with multiple options for the same step


```
...
docker run -v $PWD/data:/scif/data vanessa/cseq run sorting1
docker run -v $PWD/data:/scif/data vanessa/cseq run sorting2
```

As a user, you want a container that exposes enough metadata to run different steps of the pipeline, but you don't want to need to know the specifics of each command call or path within the container. In the above, I can direct the container to my mapped input directory
and specify a step in the pipeline, and I dont need to understand how to use `bwa` or `grep` or `seqtk`, or any of the other software
that makes up each.


### Interactive Environment
If you are curious about all the Scientific Filesystem variables available to you:

```
$CSEQ exec mapping env | grep SCIF_
```

Or if you wanted an interactive shell to explore running commands inside the container:

```
singularity shell --bind data:/scif/data cseq
```

or enter a shell in context of a scif application (mapping)

```
$ singularity run cseq shell mapping
$ echo $SCIF_APPNAME
mapping
```

## CarrierSeq Development
The developer has a different use case - to have easy command line access to the lowest level of executables installed in the container. Given a global install of all software, without SCI-F I would need to look at `$PATH` to see what has been added to the path, and then list executables in path locations to find new software installed to, for example, `/usr/bin`. There is no way to easily and programatically "sniff" a container to understand the changes, and the container is a black development box, perhaps only understood by the creator or with careful inspection of the build recipe.

In this use case, we want to build the development container.

```
$ docker build -f Dockerfile.devel -t vanessa/cseq:dev .
```

We can run the container and get some default help printed

```
docker run vanessa/cseq:dev
[help] executing /bin/bash /scif/apps/help/scif/runscript
    This is a development image for CarrierSeq, meaning that it exposes the
    underlying tools (bwa, samtools) as applications in the Scientific
    Filesystem.
    If you want to run the CarrierSeq workflow, use the carrierseq.scif recipe.
    Github Contributors: Angel Mojarro (@amojarro),
                         Srinivasa Aditya Bhattaru (@sbhattaru),
                         Christopher E. Carr (@CarrCE),
                         Vanessa Sochat (@vsoch).
    To see applications installed in the Scientific Filesystem:
    scif apps
    To run a tool, you might do:
    scif run bwa
    scif run samtools
    Or get help or metadata
    scif help bwa
    scif inspect bwa
    If you install in a container, the entrypoint should be scif, and then
    issue the above commands to it.
```

Now when we look at apps, we see all the core software that can be combined in specific ways to produce a pipeline step like "mapping".

```
$ docker run vanessa/cseq:dev apps
bwa
fqtrim
python
seqtk
sra-toolkit
```

each of which might be run, exec to activate the app environment, or shell to shell into the container under the context of a specific app:

```
# Open interactive python
$ docker run -it vanessa/cseq:dev run python

# Load container with bwa on path
$ docker run -it vanessa/cseq:dev shell bwa
$ which bwa
$ /scif/apps/bwa/bin/bwa
```

These two images that serve equivalent software is a powerful example of the flexibility of SCIF. The container creator can choose the level of detail to expose to a user that doesn't know how it was created, or perhaps has varying levels of expertise. A lab that is using core tools for working with sequence data might have preference for the development container, while a finalized pipeline distributed with a publication would have preference for the first. In both cases, the creator doesn't need to write custom scripts for a container to run a particular app, or to expose environment variables, tests, or labels. By way of using SCIF, this happens automatically. 

These two images that serve equivalent software is a powerful example of the flexibility of SCI-F. The container creator can choose the level of detail to expose to a user that doesn't know how it was created, or perhaps has varying levels of expertise. A lab that is using core tools for working with sequence data might have preference for the development container, while a finalized pipeline distributed with a publication would have preference for the first. In both cases, the creator doesn't need to write custom scripts for a container to run a particular app, or to expose environment variables, tests, or labels. By way of using SCI-F, this happens automatically. 

See the original repository <a href="https://github.com/amojarro/carrierseq" target="_blank">CarrierSeq here</a> or the <a href="https://github.com/vsoch/carrierseq/tree/singularity" target="_blank">Singularity CarrierSeq here</a>.
