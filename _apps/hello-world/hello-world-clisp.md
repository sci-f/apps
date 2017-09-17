---
title:  "Hello World (clisp)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- ubuntu
- debian
- scif
- singularity
- clisp
files:
 - hello-world.clisp
 - SingularityApp.clisp
---

```yaml
%apprun clisp
    exec clisp $SINGULARITY_APPROOT/hello-world.clisp
%appfiles clisp
    hello-world.clisp
%appinstall clisp
    apt-get install -y clisp
```
