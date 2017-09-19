---
title:  "SCI-F Help"
date:   2017-09-18 05:24:00
author: Vanessa Sochat
tags: 
- scif
- help
- linux
- singularity
---

```yaml

%apphelp docs-scif-help

A Standard Container Integration Format (SCI-F)
apps container makes it easy to run various 
metrics over an analysis of interest  (the 
container's main runscript). Each installed 
app can be thought of as a particular context 
to evoke the container's main runscript.

# List all apps
singularity apps <container>

# Run a specific app
singularity run --app <app> <container>

# Loop over all apps
for app in $(singularity apps <container>); do
    singularity run --app $app <container>
done
```
