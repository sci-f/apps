---
title:  "Hello World (R)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
categories:
- app
- R
img: robots/robot9.png
thumb: robots/robot9.png
tags: 
- scif
- singularity
files:
 - hello-world.R
 - SingularityApp.R
---

```yaml
%apprun R
    exec Rscript $SINGULARITY_APPROOT/hello-world.R
%appfiles R
    hello-world.R
%appinstall R
    apt-get install -y r-base
```
