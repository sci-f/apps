---
title:  "Metrics strace"
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
%appinstall metrics-bash-strace
    apt-get install -y strace
%apprun metrics-bash-strace
    unset SINGULARITY_APPNAME
    exec strace -c -t /.singularity.d/actions/run
```
