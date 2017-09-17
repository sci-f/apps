---
title:  "Hello World (cat)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- ubuntu
- debian
- cat
- scif
- singularity
files:
 - hello-world.cat
 - SingularityApp.cat
---

```yaml
%apprun cat
    exec cat $SINGULARITY_APPROOT/hello-world.cat
%appfiles cat
    hello-world.cat
```
