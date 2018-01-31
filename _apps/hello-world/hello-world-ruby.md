---
title:  "Hello World (Ruby)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
tags: 
- scif
- singularity
- ubuntu
- debian
- ruby
files:
 - hello-world.rb
 - rb.scif
---

```ruby
%apprun hello-world-ruby
    exec ruby $SCIF_APPROOT/hello-world.rb
%appfiles hello-world-ruby
    hello-world.rb
%appinstall hello-world-ruby
    apt-get install -y ruby
```
