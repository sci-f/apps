---
title:  "Metrics time-it"
date: 2017-09-18 05:25:00
author: Vanessa Sochat
tags: 
- metric
- debian
- ubuntu
- scif
- singularity
---

```yaml
%appinstall metrics-timeit
    apt-get install -y time
%apprun metrics-timeit
    TIME="%C    %E    %K    %I    %M    %O    %P    %U    %W    %X    %e    %k    %p    %r    %s    %t    %w"
    unset SINGULARITY_APPNAME
    export TIME
    echo "COMMAND    ELAPSED_TIME_HMS    AVERAGE_MEM    FS_INPUTS    MAX_RES_SIZE_KB    FS_OUTPUTS    PERC_CPU_ALLOCATED    CPU_SECONDS_USED    W_TIMES_SWAPPED    SHARED_TEXT_KB    ELAPSED_TIME_SECONDS    NUMBER_SIGNALS_DELIVERED    AVG_UNSHARED_STACK_SIZE    SOCKET_MSG_RECEIVED    SOCKET_MSG_SENT    AVG_RESIDENT_SET_SIZE    CONTEXT_SWITCHES"
    exec /usr/bin/time /.singularity.d/actions/run >> /dev/null
```
