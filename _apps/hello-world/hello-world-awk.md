---
title:  "Hello World (awk)"
date:   2017-08-29 16:54:46
author: Vanessa Sochat
img: robots/robot1.png
thumb: robots/robot1.png
tags: 
- scif
- singularity
- app
- awk
files:
 - hello-world.awk
 - SingularityApp.awk
---

```yaml
%apprun hello-world-awk
    exec awk -f $SINGULARITY_APPROOT/hello-world.awk
%appfiles hello-world-awk
    hello-world.awk
```
