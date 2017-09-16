---
title:  "Hello World (Ruby)"
date:   2017-09-15 12:00:00
author: Vanessa Sochat
img: robots/robot10.png
thumb: robots/robot10.png
tags: 
- scif
- singularity
- app
- ruby
files:
 - hello-world.rb
 - SingularityApp.rb
---

{% highlight ruby %}
%apprun hello-world-ruby
    exec ruby $SINGULARITY_APPROOT/hello-world.rb
%appfiles hello-world-ruby
    hello-world.rb
%appinstall hello-world-ruby
    apt-get install -y ruby
{% endhighlight %}
