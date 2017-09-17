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
%apprun perl
    exec perl6 $SINGULARITY_APPROOT/hello-world.pl
%appfiles perl
    hello-world.pl
%appinstall perl
    apt-get install -y perl6
```
