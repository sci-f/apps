---
title:  "Hello World (clisp)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
img: robots/robot4.png
thumb: robots/robot4.png
tags: 
- scif
- singularity
- app
- clisp
files:
 - hello-world.clisp
 - SingularityApp.clisp
---

```yaml
%apprun clisp
    exec clisp $SINGULARITY_APPROOT/hello-world.clisp
%appfiles clisp
    hello-world.clisp
%appinstall clisp
    apt-get install -y clisp
```
