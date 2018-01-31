---
title:  "workflow-cwltool"
date: 2017-11-15 00:00:00
author: Alain Domissy
tags: 
- ubuntu
- debian
- workflow
- cwltool
- CWL
- scif
- singularity
files:
 - cwltool.scif
 
---

```yaml
%appinstall workflow-cwltool
    apt update -y --fix-missing
    apt install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion
    MINICONDAURL=https://repo.continuum.io/miniconda/Miniconda3-4.3.30-Linux-x86_64.sh
    wget --quiet ${MINICONDAURL} -O miniconda.sh
    /bin/bash miniconda.sh -b -p miniconda
    rm miniconda.sh
    PATH=/scif/apps/workflow-cwltool/miniconda/bin:$PATH
    export PATH
    /scif/apps/workflow-cwltool/miniconda/bin/conda install -y --channel bioconda --channel glaxosmithkline python=2.7.14 cwltool=1.0.20170928192020 typing=3.5.3.0

%appfiles workflow-cwltool
%appenv workflow-cwltool
    CWLTOOL_HOME=/scif/apps/workflow-cwltool
    export CWLTOOL_HOME
    PATH=/scif/apps/workflow-cwltool/miniconda/bin:$PATH
    export PATH
%apphelp workflow-cwltool
    cwltool is the Common Workflow Language reference implementation.
    It is recommended to create the following alias:
    alias cwltool="singularity run --app workflow-cwltool \${SINGULARITY_CONTAINER}"
    More help is then available by running
    cwltool --help
%apprun workflow-cwltool
    cwltool "$@"
%applabels workflow-cwltool
    MAINTAINER adomissy@ucsd.edu
    BUILD_VERSION 0.0.1
    WRAPPEDTOOL_VERSION 1.0.20170928192020
    WRAPPEDTOOL_INFO http://www.commonwl.org/
```
