---
title:  "Hello World (Julia)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
categories:
- app
- julia
img: robots/robot6.png
thumb: robots/robot6.png
tags: 
- scif
- singularity
files:
 - hello-world.jl
 - SingularityApp.jl
---

```yaml
%apprun julia
    exec julia $SINGULARITY_APPROOT/hello-world.jl
%appfiles julia
    hello-world.jl
%appinstall julia
    apt-get install -y julia
```
