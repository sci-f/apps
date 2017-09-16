---
title:  "Hello World (bash)"
date:   2017-08-29 16:54:46
author: Vanessa Sochat
img: robots/robot2.png
thumb: robots/robot2.png
tags: 
- app
- bash
- shell
- scif
- singularity
files:
 - hello-world.bash
---

```yaml
%apprun bash
    exec /bin/bash hello-world.bash
%appfiles bash
    hello-world.bash bin/hello-world.bash
```
