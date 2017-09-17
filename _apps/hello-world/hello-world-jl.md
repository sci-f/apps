---
title:  "Hello World (Julia)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- ubuntu
- debian
- julia
- scif
- singularity
files:
 - hello-world.jl
 - SingularityApp.jl
---

```yaml
%apprun hello-world-julia
    exec julia $SINGULARITY_APPROOT/hello-world.jl
%appfiles hello-world-julia
    hello-world.jl
%appinstall hello-world-julia
    apt-get install -y julia
```
