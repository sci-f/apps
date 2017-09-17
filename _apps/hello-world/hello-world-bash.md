---
title:  "Hello World (bash)"
date:   2017-08-29 16:54:46
author: Vanessa Sochat
tags: 
- bash
- shell
- scif
- ubuntu
- debian
- singularity
files:
 - hello-world.bash
---
```
%apprun hello-world-bash
    exec /bin/bash hello-world.bash
%appfiles hello-world-bash
    hello-world.bash bin/hello-world.bash
```
