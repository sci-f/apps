---
title:  "Hello World (octave)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
categories:
- app
- octave
img: robots/robot6.png
thumb: robots/robot6.png
tags: 
- scif
- singularity
files:
 - hello-world.octave
 - SingularityApp.octave
---

```yaml
%apprun octave
    exec octave --no-gui --silent $SINGULARITY_APPROOT/hello-world.octave
%appenv octave
    DISPLAY=localhost:0.0
    export DISPLAY
%appfiles octave
    hello-world.octave
%appinstall octave
    apt-get install -y octave
```
