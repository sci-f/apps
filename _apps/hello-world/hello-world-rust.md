---
title:  "Hello World (Rust)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
img: robots/robot11.png
thumb: robots/robot11.png
tags: 
- app
- rust
- scif
- singularity
files:
 - hello-world.rs
 - SingularityApp.rs
---

```yaml
%apprun hello-world-rust
    exec hello-world.rust
%appfiles hello-world-rust
    hello-world.rs
%appinstall hello-world-rust
    curl -f -L https://static.rust-lang.org/rustup.sh -O
    chmod u+x rustup.sh
    RUSTUP_PREFIX=$PWD ./rustup.sh
    bin/rustc hello-world.rs -o bin/hello-world.rust
```
