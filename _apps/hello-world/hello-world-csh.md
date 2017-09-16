---
title:  "Hello World (csh)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
categories:
img: robots/robot5.png
thumb: robots/robot5.png
tags: 
- scif
- singularity
- app
- csh
- shell
files:
 - hello-world.csh
 - SingularityApp.c
---

```yaml
%apprun csh
    exec csh $SINGULARITY_APPROOT/hello-world.csh
%appfiles csh
    hello-world.csh
%appinstall csh
    apt-get install -y csh
```
