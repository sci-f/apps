---
title:  "Hello World (Go)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
categories:
- app
- go
img: robots/robot5.png
thumb: robots/robot5.png
tags: 
- scif
- singularity
files:
 - hello-world.go
 - SingularityApp.go
---

```yaml
%apprun go
    exec hello-world.go
%appenv go
    GOROOT=/scif/apps/go
    export GOROOT
%appfiles go
    hello-world.go
%appinstall go
    wget https://storage.googleapis.com/golang/go1.8.3.linux-amd64.tar.gz
    tar --strip-components=1 -zxf go1.8.3.linux-amd64.tar.gz
    bin/go build hello-world.go && mv hello-world bin/hello-world.go
```
