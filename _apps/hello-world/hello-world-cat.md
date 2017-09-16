---
title:  "Hello World (cat)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
categories:
- app
- cat
img: robots/robot3.png
thumb: robots/robot3.png
tags: 
- scif
- singularity
files:
 - hello-world.cat
 - SingularityApp.cat
---

```yaml
%apprun cat
    exec cat $SINGULARITY_APPROOT/hello-world.cat
%appfiles cat
    hello-world.cat
```
