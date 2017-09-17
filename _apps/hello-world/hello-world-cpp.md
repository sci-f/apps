---
title:  "Hello World (C++)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- ubuntu
- debian
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
