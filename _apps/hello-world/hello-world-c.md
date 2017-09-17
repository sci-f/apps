---
title:  "Hello World (C)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- c
- ubuntu
- debian
- scif
- singularity
files:
 - hello-world.c
 - SingularityApp.c
---

```yaml
%apprun c
    exec hello-world.c
%appfiles c
    hello-world.c
%appinstall hello-world-c
    apt-get install -y gcc
    gcc hello-world.c -o bin/hello-world.c
```
