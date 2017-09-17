---
title:  "Hello World (awk)"
date:   2017-08-29 16:54:46
author: Vanessa Sochat
tags: 
- scif
- singularity
- awk
- ubuntu
- debian
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
