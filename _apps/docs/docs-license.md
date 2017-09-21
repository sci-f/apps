---
title:  "SCI-F License"
date:   2017-09-20 08:25:00
author: Vanessa Sochat
tags: 
- scif
- license
- linux
- singularity
---

```yaml

%apphelp docs-license

This module will add a LICENSE from a repo to a 
container, and then print it out fully for the user
when the app is run:

    singularity run --app docs-license <container>


%apprun docs-license
cat ${SINGULARITY_APPROOT}/LICENSE

%appfiles docs-license
LICENSE*
```
