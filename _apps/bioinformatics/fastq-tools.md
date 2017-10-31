---
title:  "fastq-tools"
date: 2017-10-30 12:00:00
author: Alain DOmissy
tags: 
- ubuntu
- debian
- bioinformatics
- fastq
- scif
- singularity
files:
 - hello-world.R
 - SingularityApp.fastq-tools
---

```yaml
%appinstall fastqtools
     apt-get -y install libpcre3-dev
     apt-get -y install zlibc
%appfiles fastqtools
    tools/fastq-tools   bin/
    tools/fastq-kmers   bin/
    tools/fastq-match   bin/
    tools/fastq-uniq    bin/
    tools/fastq-qual    bin/
    tools/fastq-sample  bin/
    tools/fastq-qualadj bin/
    tools/fastq-sort    bin/
    tools/fastq-qscale  bin/
%appenv fastqtools
    FASTQTOOLS_HOME=${APPROOT_fastqtools}
    export FASTQTOOLS_HOME
%apphelp fastqtools
    fastqtools provide a number of small and efficient programs to perform common tasks
    with high throughput sequencing data in the FASTQ format.
    All of the programs work with typical FASTQ files as well as gzipped FASTQ files.
%apprun fastqtools
    fastqtools "$@"
```
