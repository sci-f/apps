---
title:  "Hello World (Zsh)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- ubuntu
- debian
- zsh
- shell
- scif
- singularity
files:
 - hello-world.zsh
 - zsh.scif
---

```yaml
%apprun hello-world-zsh
    exec /bin/zsh $SCIF_APPROOT/hello-world.zsh
%appfiles hello-world-zsh
    hello-world.zsh
%appinstall hello-world-zsh
    apt-get install -y zsh > /dev/null 2>&1
```
