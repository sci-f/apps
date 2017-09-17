---
title:  "Hello World (Go)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- scif
- singularity
- ubuntu
- debian
- go
files:
 - hello-world.go
 - SingularityApp.go
---

```yaml
%apprun hello-world-go
    exec hello-world.go
%appenv hello-world-go
    GOROOT=/scif/apps/go
    export GOROOT
%appfiles hello-world-go
    hello-world.go
%appinstall hello-world-go
    wget https://storage.googleapis.com/golang/go1.8.3.linux-amd64.tar.gz
    tar --strip-components=1 -zxf go1.8.3.linux-amd64.tar.gz
    bin/go build hello-world.go && mv hello-world bin/hello-world.go
```
