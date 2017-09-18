---
title:  "Cow Fortune"
date: 2017-09-18 05:25:00
author: Vanessa Sochat
tags: 
- fun
- debian
- ubuntu
- scif
- singularity
---

```yaml
%appinstall cow-fortune
    apt-get install -y lolcat fortune
%apprun cow-fortune
    /usr/games/fortune | /usr/games/lolcat
    apt-get moo
```
