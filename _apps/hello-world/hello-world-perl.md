---
title:  "Hello World (perl)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- scif
- singularity
- ubuntu
- debian
- perl
files:
 - hello-world.pl
 - pl.scif
---

```yaml
%apprun hello-world-perl
    exec perl6 $SCIF_APPROOT/hello-world.pl
%appfiles hello-world-perl
    hello-world.perl
%appinstall hello-world-perl
    apt-get install -y perl6
```
