---
title:  "fastq-tools"
date: 2017-10-30 12:00:00
author: Alain Domissy
tags: 
- ubuntu
- debian
- bioinformatics
- fastq
- scif
- singularity
files:
 - fastq-tools
 - SingularityApp.fastq-tools
 
---

```yaml
%appinstall fastq-tools
    apt-get -y install wget
    apt-get -y install autoconf libtool build-essential
    apt-get -y install libpcre3-dev
    apt-get -y install zlibc libz-dev
    # apt-get -y install libncurses5-dev
    wget  https://github.com/dcjones/fastq-tools/archive/v0.8.tar.gz -O fastq-tools-0.8.tar.gz
    tar --extract --gzip --file fastq-tools-0.8.tar.gz
    rm fastq-tools-0.8.tar.gz
    cd fastq-tools-0.8
    ./autogen.sh && ./configure && make
    cd -
    #cp -puv fastq-tools-0.8/src/fastq-{grep,kmers,match,uniq,qual,sample,qualadj,sort,qscale} bin/
    cp  fastq-tools-0.8/src/fastq-grep    bin/
    cp  fastq-tools-0.8/src/fastq-kmers   bin/
    cp  fastq-tools-0.8/src/fastq-match   bin/
    cp  fastq-tools-0.8/src/fastq-uniq    bin/
    cp  fastq-tools-0.8/src/fastq-qual    bin/
    cp  fastq-tools-0.8/src/fastq-sample  bin/
    cp  fastq-tools-0.8/src/fastq-qualadj bin/
    cp  fastq-tools-0.8/src/fastq-qscale  bin/
    #rm -rf fastq-tools-0.8
%appfiles fastq-tools
    fastq-tools bin/
%appenv fastq-tools
    FASTQTOOLS_HOME=/scif/apps/fastq-tools
    export FASTQTOOLS_HOME
%apphelp fastq-tools
    fastq-tools provide a number of small and efficient programs to perform common tasks
    with high throughput sequencing data in the FASTQ format.
    All of the programs work with typical FASTQ files as well as gzipped FASTQ files.
%apprun fastq-tools
    fastq-tools "$@"
```