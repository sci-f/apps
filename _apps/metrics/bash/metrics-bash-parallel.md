---
title:  "Metrics Parallel"
date: 2017-09-18 05:25:00
author: Vanessa Sochat
tags: 
- metric
- debian
- ubuntu
- scif
- singularity
---

```yaml
%appinstall metrics-bash-parallel
    apt-get install -y parallel
%apprun metrics-bash-parallel
    unset SINGULARITY_APPNAME
    COMMAND="/.singularity.d/actions/run"
    parallel /bin/bash ::: $COMMAND $COMMAND $COMMAND
```
