---
title:  "Hello World (Zsh)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
img: robots/robot12.png
thumb: robots/robot12.png
tags: 
- app
- zsh
- shell
- scif
- singularity
files:
 - hello-world.zsh
 - SingularityApp.zsh
---

```yaml
%apprun hello-world-zsh
    exec /bin/zsh $SINGULARITY_APPROOT/hello-world.zsh
%appfiles hello-world-zsh
    hello-world.zsh
%appinstall hello-world-zsh
    apt-get install -y zsh > /dev/null 2>&1
```
