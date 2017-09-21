---
title:  "SCI-F Readme"
date:   2017-09-20 08:25:00
author: Vanessa Sochat
tags: 
- scif
- help
- linux
- singularity
---

```yaml

%apphelp docs-readme

This module will add a README from a repo to a 
container, and then print it out fully for the user
when the app is run:

    singularity run --app docs-readme <container>


%apprun docs-readme
cat ${SINGULARITY_APPROOT}/README.md

%appfiles docs-readme
README*
```
