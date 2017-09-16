---
title:  "Hello World (C++)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
img: robots/robot5.png
thumb: robots/robot5.png
tags: 
- app
- cpp
- scif
- singularity
files:
 - hello-world.cpp
 - SingularityApp.cpp
---

```yaml
%apprun cpp
    exec hello-world.cpp
%appfiles cpp
    hello-world.cpp
%appinstall cpp
    g++ hello-world.cpp -o bin/hello-world.cpp
```
