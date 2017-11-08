---
title:  "App Name"
date:   YYYY-MM-DD HH:MM:SS
author: Vanessa Sochat
tags: 
- scif
- singularity
files:
 - app-file.sh
 - SingularityApp.appname
---

```yaml
%apprun appname
    exec $SINGULARITY_APPROOT/app-file.sh
%appfiles appname
    app-file.sh
```
