---
title:  "Hello World (R)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- ubuntu
- debian
- R
- scif
- singularity
files:
 - hello-world.R
 - R.scif
---

```yaml
%apprun hello-world-R
    exec Rscript $SCIF_APPROOT/hello-world.R
%appfiles hello-world-R
    hello-world.R
%appinstall hello-world-R
    apt-get install -y r-base
```
