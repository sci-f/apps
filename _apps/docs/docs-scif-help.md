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

A Scientific Filesystem (SCI-F) makes it easy to expose multiple
    entry points, environments, and help for scientific applications,
    whether installed in a container or on the host. A runscript entry
    point can be everything from an interactive environment to a script
    to execute.

    # List all applications
    ./<container> apps

    # Run a specific application
    ./<container> run <app>

    # Loop over all applications
    for app in $(./<container> apps); do
        ./<container> run $app
    done
```
