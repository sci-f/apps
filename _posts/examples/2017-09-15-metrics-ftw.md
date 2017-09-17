---
layout: post
title:  "Container Metrics: Evaluating a container from Different Angles via SCI-F Apps "
author: Vanessasaurus
date:   2017-09-13 16:16:01 -0600
github: https://github.com/containers-ftw/metrics-ftw
asciinema: container-metrics-ftw.json
categories:
 - Examples
 - Metrics
---

For this next use case, a scientist is interested in running a series of metrics over an analysis of interest (the container’s main function, executed by it’s primary runscript).  He has been given a container with a runscript, and several installed supporting metrics (SCI-F apps also in the container), and knows nothing beyond that. 

<!--more-->

Each installed SCI-F app can be thought of as a particular context to evoke the container's main runscript, and the apps themselves are relatively agnostic to the runscript itself. Importantly, using the image for its intended purpose is not impacted by the presence of these supporting tools. The command to run the image is unchanged. When the scientist runs the image, he sees it perform it’s primary function, a print of “Hello World!” to the console.

```bash
singularity run metrics.img 
Hello-World!
```

At this point, the scientist doesn’t know what the metrics are, or the particular environment or locations in the container. Given that the container has SCI-F, the scientist can ask the container to tell him what metrics are installed:

```bash
 singularity apps metrics.img 
custom
linter
parallel
strace
time
```

And then run the metric easily by simply specifying it’s name:

```bash
singularity run --app time metrics.img
```

or even writing the previous command into a loop:

```bash
for app in $(singularity apps metrics.img)
   do
      singularity run --app $app metrics.img
done
```

This particular container has several metrics to assess usage and timing of different resources (time), a complete trace of the call (strace), an example custom metric (custom), a static linter (linter), and a function to run the container’s runscript in parallel (parallel). Each of these SCI-F apps serves as an example use case that is discussed in the following sections.

### Metric Example 1: Evaluate software across different metrics
A system admin or researcher concerned about evaluation of different software
could add relevant metrics apps to the software containers, and then easily evaluate
each one with the equivalent command to the container. Importantly, since each
evaluation metric is a modular app, the container still serves its intended purposes. 
As an example, here is a simple app to return a table of system traces for the
runscript:

```
%apprun strace
    unset SINGULARITY_APPNAME
    exec strace -c -t /.singularity.d/actions/run
```

In the above example, since the main run command for the container looks for the
SINGULARITY_APPNAME, we need to unset it first. We then run strace and return
a table that assesses the runscript:

```bash
 singularity run --app strace metrics.img 
Hello-World!
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
  0.00    0.000000           0        15           read
  0.00    0.000000           0         1           write
  0.00    0.000000           0        35        24 open
  0.00    0.000000           0        17           close
  0.00    0.000000           0        25        12 stat
  0.00    0.000000           0         4           fstat
  0.00    0.000000           0        14           mmap
  0.00    0.000000           0         8           mprotect
  0.00    0.000000           0         2           munmap
  0.00    0.000000           0         6           brk
  0.00    0.000000           0        14           rt_sigaction
  0.00    0.000000           0         6         6 access
  0.00    0.000000           0         2           getpid
  0.00    0.000000           0         2           execve
  0.00    0.000000           0        14           fcntl
  0.00    0.000000           0         2           getdents
  0.00    0.000000           0         3           geteuid
  0.00    0.000000           0         2           getppid
  0.00    0.000000           0         2           arch_prctl
  0.00    0.000000           0         1           openat
  0.00    0.000000           0         1           faccessat
------ ----------- ----------- --------- --------- ----------------
100.00    0.000000                   176        42 total
```

Regardless of what the runscript does, this SCI-F app will provide a consistent way 
to produce this metric. Any user that added the small module to his or her container would immediately have this assessment for the software provided by the container.

### Example Metric 2: Custom Functions and Metrics
When a container is intended to only perform one function, this maps nicely to having a single runscript. As the number of possible functions increase, however, the user is forced to either:

 - have a runscript that can take command line options to call different executables
 - use the `exec` command with some known path (to the user)

SCI-F apps allow for an easy way to define custom helper metrics or functions for
the container without needing to write a complicated script or know the locations of executables in a container that was built by another. The app “custom” is an example of this, as it generates a fortune with a bit of surprise added:

```
singularity run --app custom metrics.img
The difference between the right word and the almost right word is the
difference between lightning and the lightning bug.
		-- Mark Twain
                 (__) 
                 (oo) 
           /------\/ 
          / |    ||   
         *  /\---/\ 
            ~~   ~~   
..."Have you mooed today?"...

```

Although this particular example is comical, the larger idea that individuals can specialize in general modules for assessing containers is a powerful one.

### Metrics Example 3: Code Quality and Linting
A SCI-F app can meet the needs to serve as a linter over a set of files,
or general tests. The example is provided here with the SCI-F app “linter,” which runs a linter over a script. 

```bash
singularity run --app linter metrics.img 

In /scif/apps/linter/lintme.sh line 2:
for f in  do;
^-- SC2034: f appears unused. Verify it or export it.
          ^-- SC1063: You need a line feed or semicolon before the 'do'.
            ^-- SC1059: No semicolons directly after 'do'.


In /scif/apps/linter/lintme.sh line 3:
grep -qi hq.*mp3  && echo -e 'Foo  bar'; done
         ^-- SC2062: Quote the grep pattern so the shell won't interpret it.
                          ^-- SC2039: #!/bin/sh was specified, but echo flags are not standard.

```

This example used a file provided in the container, but a linter app could also accept a command line argument to a file or folder. During building, we advise the researcher to still use the `%test` section to evaluate the outcome of the build process, and to use SCI-F apps for general tests that are generalizable to other containers.

### Metrics Example 4: Runtime Evaluation
In that a metric can call a runscript, it could be easy to evaluate running the main analysis under various levels or conditions. As a simple proof of concept, here we are creating an app to execute the same exact script in parallel.

```bash
%apprun parallel
    COMMAND="/.singularity.d/actions/run; "
    (printf "%0.s$COMMAND" {1..4}) | parallel

Singularity run --app parallel metrics.img
Hello World!
Hello World!
Hello World!
```

And you might imagine a similar loop to run an analysis, and modify a runtime
or system variable for each loop, and save the output (or print to console). 

This metrics implementation is available for use and documentation provided in entirety [on Github](https://github.com/containers-ftw/metrics-ftw). If you want to watch the asciicast in its home and original form, you can [see it here](https://asciinema.org/a/137434?speed=3).
