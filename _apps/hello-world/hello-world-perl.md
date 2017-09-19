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
 - SingularityApp.pl
---

```yaml
%apprun hello-world-perl
    exec perl6 $SINGULARITY_APPROOT/hello-world.pl
%appfiles hello-world-perl
    hello-world.perl
%appinstall hello-world-perl
    apt-get install -y perl6
```
