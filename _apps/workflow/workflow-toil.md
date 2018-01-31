---
title:  "workflow-toil"
date: 2017-11-15 00:00:00
author: Alain Domissy
tags: 
- ubuntu
- debian
- workflow
- toil
- cwltoil
- CWL
- scif
- singularity
files:
 - toil.scif
 
---

```yaml
%appinstall workflow-toil
    apt update -y --fix-missing
    apt install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion
    MINICONDAURL=https://repo.continuum.io/miniconda/Miniconda3-4.3.30-Linux-x86_64.sh
    wget --quiet ${MINICONDAURL} -O miniconda.sh
    /bin/bash miniconda.sh -b -p miniconda
    rm miniconda.sh
    PATH=/scif/apps/workflow-toil/miniconda/bin:$PATH
    export PATH
    /scif/apps/workflow-toil/miniconda/bin/conda install -y --channel bioconda --channel glaxosmithkline python=2.7.14 cwltool=1.0.20170928192020 typing=3.5.3.0

%appfiles workflow-toil
%appenv workflow-toil
    CWLTOOL_HOME=/scif/apps/workflow-toil
    export CWLTOOL_HOME
    PATH=/scif/apps/workflow-toil/miniconda/bin:$PATH
    export PATH
%apphelp workflow-toil
    Scalable, efficient, cross-platform pipeline management system, written
    entirely in Python, and designed around the principles of functional
    programming
    It is recommended to create the following aliases:
    alias toil="singularity run --app workflow-toil \${SINGULARITY_CONTAINER}"
    alias cwltoil="singularity exec --app workflow-toil \${SINGULARITY_CONTAINER} cwltoil"
    alias cwltool="singularity exec --app workflow-toil \${SINGULARITY_CONTAINER} cwltool"
    More help is then available by running
    toil --help
%apprun workflow-toil
    toil "$@"
%applabels workflow-toil
    MAINTAINER adomissy@ucsd.edu
    BUILD_VERSION 0.0.1
    WRAPPEDTOOL_VERSION 3.11.0
    WRAPPEDTOOL_INFO http://toil.ucsc-cgl.org/
```
