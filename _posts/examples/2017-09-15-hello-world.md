---
layout: post
title:  "Hello World, Using SCI-F for Modular Software Evaluation"
date:   2017-09-13 16:16:01 -0600
author: Vanessasaurus
github: https://github.com/sci-f/container.scif
asciinema: hello-world-scif.json
categories:
 - Examples
 - Applications
---

A common question pertains to evaluation of different solutions toward a common goal. An individual might ask "How does implementation "A" compare to implementation "B" as evaluated by one or more metrics?” For a systems admin, the metric might pertain to running times, resource usage, or efficiency. For a researcher, he or she might be interested in looking at variability (or consistency) of outputs. Importantly, it should be possible to give a container serving such a purpose to a third party that does not know locations of executables, or environment variables to load, and the container runs equivalently. SCI-F allows for this by way of providing modular software applications, each corresponding to a custom environment, libraries, and potentially files.

<!--more--> 

## Method
To demonstrate this use case, we developed a container that implements the most basic function for a program, a print to the console, for each of 19 different languages (R, awk, bash, c, cat, chapel, clisp, cpp, csh, go, julia, octave, perl, python, ruby, rust, tcsh, zsh). The container is designed as a means to collect a series of metrics relative to timing and system resources for each language. The metrics pertain to system resources provided by the time (time(1) - Linux manual page ) and strace (strace(1): trace system calls/signals...) utilities. A user that did not create the container could ask it for global help:

```
$ singularity help container.img


This container will say hello-world (in dinosaur)!

Examples:

     # See all installed languages
     singularity apps <container>

     # See help for a specific language
     singularity --app <language> <container> help to see help  |or|

     # Run a specific languages
     singularity --app <language> <container>

```

or see all applications installed:

```
$ singularity apps container.img
   awk
   bash
   …
   zsch
```

Or run any particular language:

```
$ singularity run --app bash container.img
RaawwWWWWWRRRR!!
```

Importantly, in the example above, using "run" for the application "bash" handles loading environment variables, adding the application folders to the path, and executing the associated runscript. The application also optionally can serve it’s own labels, environment metadata, and specifics about its size with the “inspect” command:

```
singularity inspect --app bash container.img

{
    "SINGULARITY_APP_NAME": "bash",
    "SINGULARITY_APP_SIZE": "1MB"
}
```

Therefore, the metric evaluation could be run, across modules, without knowing the applications installed with a simple for loop.

```
for app in $(singularity apps container.img)
    do
    singularity run --app $app container.img
done
```

In the case of metric evaluation, it would be up to the implementor to decide to evaluate the software internally (above) or externally. For example, an external evaluation might look like the following:

```
for app in $(singularity apps container.img)
    do
    /usr/bin/time -a singularity run --app $app container.img
done
```

In practice, for general metrics like timing and host resources, it is advantageous to perform tests externally, as the containers themselves can be agnostic to the tests. For tests that look at system calls (e.g., strace as in the example above) calling externally would mean needing to properly account for the call to the singularity software itself in the results.

## Results
To demonstrate the value of using SCI-F containers, we ran a simple function to print to the command line in 19 languages, and were able to run the analysis in entirety without knowing the specific commands for each language. The resulting table of features pertaining to times and resources (Supplementary Table 1) demonstrates a wide span of differences between the seemingly identical calls. A principle component analysis (PCA) of these features shows distinct groups (see [full results](https://github.com/sci-f/container.scif/blob/master/logs/languages_metrics.ipynb) here)
