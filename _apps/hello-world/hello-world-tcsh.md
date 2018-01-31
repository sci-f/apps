---
title:  "Hello World (tcsh)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- ubuntu
- debian
- tsch
- shell
- scif
- singularity
files:
 - hello-world.tcsh
 - tcsh.scif
---

```yaml
%apprun hello-world-tcsh
    exec tcsh $SCIF_APPROOT/hello-world.tcsh
%appfiles hello-world-tcsh
    hello-world.tcsh
%appinstall hello-world-tcsh
    apt-get install -y tcsh
```
