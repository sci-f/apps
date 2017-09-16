---
title:  "Hello World (python)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
img: robots/robot8.png
thumb: robots/robot8.png
tags: 
- app
- python
- scif
- singularity
files:
 - hello-world.py
 - SingularityApp.py
---

```yaml
%apprun python
    exec python $SINGULARITY_APPROOT/hello-world.py
%appfiles python
    hello-world.py
%appinstall python
    apt-get install -y python python-dev
```
