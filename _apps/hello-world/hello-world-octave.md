---
title:  "Hello World (octave)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- octave
- ubuntu
- debian
- scif
- singularity
files:
 - hello-world.octave
 - SingularityApp.octave
---

```yaml
%apprun hello-world-octave
    exec octave --no-gui --silent $SINGULARITY_APPROOT/hello-world.octave
%appenv hello-world-octave
    DISPLAY=localhost:0.0
    export DISPLAY
%appfiles hello-world-octave
    hello-world.octave
%appinstall hello-world-octave
    apt-get install -y octave
```
