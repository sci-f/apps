---
layout: post
title:  "An Introduction to SCI-F Apps"
date:   2018-01-29 09:15:01 -0600
author: Vanessasaurus
github: https://github.com/sci-f/sci-f.github.io/blob/master/_posts/tutorials
categories:
 - Examples
 - Tutorials
---


In this tutorial, we are going to get started with the Scientific Filesystem (SCIF), which is a specification for a filesystem organizational, a set of environment variables, and functions that control the two in order to optimize the usability and discoverability of scientific applications. Specifically, we will build a "foobar" container, and a "cowsay" container that prints colored fortunes.</a>. We don't even have to make containers (we can install on the host) but we will for this tutorial to keep the applications isolated from the host. 

<!--more--> 

## Why do we need SCIF?
A Scientific Filesystem (SCIF) provides entrypoints, metadata, and environments that are separate from the traditional host filesystem. When used in the context of containers, SCIF provides internal modularity. For example, installing a set of libraries, defining environment variables, or adding lables that belong to application `foo` in the SCIF makes a strong assertion that those dependencies belong to `foo`. When I run `foo`, I can be confident that the container is running in this context, meaning with `foo`'s custom environment, and with `foo`'s libraries and executables on the path. This is drastically different from serving many executables in a single container, because there is no way to know which are associated with which of the container's intended functions. For example, let's take a look at this series of steps to install dependencies for software foo and bar.

```
%post

# install dependencies 1
# install software A (foo)
# install software B (bar)
# install software C (foo)
# install software D (bar)
```

The creator may know that A and C were installed for `foo` and B and D for `bar`, but down the road, when someone discovers the container, if they can find the software at all, the intention of the container creator would be lost. As many are now, containers without any form of internal organization and predictibility are black boxes. We don't know if some software installed to `/opt`, or to `/usr/local/bin`, or to their custom favorite folder `/code`. We could assume that the creator added important software to the path and look in these locations, but that approach is still akin to fishing in a swamp. We might only hope that the container's main entry point is enough to make the container perform as intended. 

### Mixed up Modules
If your container truly runs one script, the traditional model of having a single entry point works well. Even in the case of having two functions like `foo` and `bar` you probably have something like this.

```
%runscript

if some logic to choose foo:
   check arguments for foo
   run foo
else if some logic to choose bar:
   run bar
```

and maybe your environment looks like this:

```
%environment
    BEST_GUY=foo
    export BEST_GUY
```

but what if you run into this issue, with foo and bar?

```
%environment
    BEST_GUY=foo
    BEST_GUY=bar
    export BEST_GUY
```

You obviously can't have them at separate times. You'd have to source some custom environment file (that you make on your own) and it gets hard easily with issues of using shell and sourcing. We don't know who the best guy is! You probably get the general idea. Without internal organization and modularity:


 - You have to do a lot of manual work to expose the different software to the user via a custom runscript (and be a generally decent programmer). 
 - All software must share the same metadata, environment, and labels. 


Under these conditions, containers are at best block boxes with unclear delineation between software provided, and only one context of running anything. The container creator shouldn't need to spend inordinate amounts of time writing custom runscripts to support multiple functions and inputs. Each of `foo` and `bar` should be easy to define, and have it's own runscript, environment, labels, tests, and help section.


### Container Transparency
Using a SCIF makes `foo` and `bar` transparent, and solve this problem of mixed up modules. Our simple issue of mixed up modules could be solved if we could separate them like this:

```
%appenv foo
    BEST_GUY=foo
    export BEST_GUY

%appenv bar
    BEST_GUY=bar
    export BEST_GUY

%apprun foo
    echo The best guy is $BEST_GUY

%apprun bar
    echo The best guy is $BEST_GUY
```

In the above, each chunk that starts with `%app` delineates a particular section. The section `%appenv` is for environment variables, and `%apprun` is the entrypoint for the application of interest. Which application do they belong to? The name comes after the section name, (`%apprun foo`).  Importantly, each application has its own modular location. When you do an `%appinstall foo`, the commands are all done in context of that base. The organization looks like this:

```
/scif/apps/

     foo/
        bin/
        lib/
        scif/
            runscript.help
            runscript
            environment.sh

     bar/

     ....
```

The bin and lib are also automatically generated. The really cool thing is that we can define an application with many different strategies. An application could be...


A single file to run! If I just add a file to a bin, make it executable, and then make it the entrypoint, I'm done.

```
%appfiles foo
    runfoo.sh   bin/runfoo.sh

%appinstall foo
    chmod u+x bin/runfoo.sh

%apprun foo
    exec foo
```

You don't even need files! You could just do this.

```
%appinstall foo
    echo 'echo "Hello Foo."' >> bin/runfoo.sh
    chmod u+x bin/runfoo.sh
```

An application might just be a particular environment, to be predominantly used with shell

```
%appenv foo
    BEST_APP=foo
    export BEST_APP
```
For a complete list of the sections defined, see the <a href="https://sci-f.github.io/spec-v1#environment-variables" target="_blank">full specification</a>. You can define any number of the sections for an application.

Containers are already reproducible in that they package dependencies. This basic format adds to that by making the software inside of them modular, predictable, and programmatically accessible. We can say confidently that some set of steps, labels, or variables in one of the entry points is associated with a particular action of the container. We can better reveal how dependencies relate to each step in a scientific workflow. And the scientific workflow doesn't necessary have to be in a container - with SCIF this recipe is host agnostic. I can install `foo` and `bar` on my host, or in a Docker or Singularity container. Let's do this for two containers, so we don't muck with our personal machines.

#### Docker
You can start with a [Docker base that has scif installed](https://github.com/vsoch/scif/blob/master/Dockerfile), and then has the `scif` executable as the entrypoint and added to the path. With this base, all you need to do to build your recipe is add the file to the container, and install it with `scif`:

```
FROM vanessa/scif
ADD foobar.scif /
RUN scif install /foobar.scif
```

and then build normally:

```
docker build -t vanessa/foobar .
```

You can do the exact same thing with Singularity, and even use the same base!

#### Singularity

```
Bootstrap:docker
From: vanessa/scif

%files
    foo-bar.scif

%post
    /opt/conda/bin/scif install /cowsay.scif install /foo-bar.scif
```

and build

```
sudo singularity build foobar.simg Singularity.foobar
```


#### Commands
Now we can run the containers side by side, and see the SCIF respond consistently regardless of the technology wrapping it. Using SCIF "apps", a user can easily discover both `foo` and `bar` without knowing anything about the container:


```
# The following two are equivalent for Singularity
$ singularity run foobar.img apps
$ ./foobar.simg apps

# Docker
$ docker run -it vanessa/foobar apps
bar
foo
```

and inspect each one:

```
$ ./foobar.simg inspect foo
$ docker run -it vanessa/foobar inspect foo
{
    "foo": {
        "appenv": [
            "BEST_GUY=foo",
            "export BEST_GUY"
        ],
        "apprun": [
            "BEST_GUY=foo",
            "export BEST_GUY",
            "BEST_GUY=foo",
            "export BEST_GUY",
            "    echo The best guy is $BEST_GUY"
        ]
    }
}
```

and of course, run them!

```
$ docker run -it vanessa/foobar run foo
[foo] executing /bin/bash /scif/apps/foo/scif/runscript
The best guy is foo

$ ./foobar.simg run foo
[foo] executing /bin/bash /scif/apps/foo/scif/runscript
The best guy is foo

$ ./foobar.simg --quiet run foo
The best guy is foo
```


### Container Modularity
The next goal is container modularity! For this example, we are going to switch to a more fun build recipe - cowsay!  If you want to grab the recipe to follow along, you can <a href='https://github.com/sci-f/sci-f.github.io/blob/master/_posts/tutorials/cowsay.scif' target='_blank'>get it here. Let's again build a Docker and Singularity container.

```
FROM vanessa/scif
ADD cowsay.scif /
RUN scif install /cowsay.scif
```
```
docker build -f Dockerfile.cowsay -t vanessa/cowsay .
```

and Singularity

```
Bootstrap:docker
From: vanessa/scif

%files
    cowsay.scif

%post
    /opt/conda/bin/scif install /cowsay.scif install /cowsay.scif
```

and build

```
sudo singularity build cowsay Singularity.cowsay
```

So how is it that the different SCIF apps find one another? They discover each other by way of environment variables. For the filesystem, the name and base `scif` is chosen intentionally to be something short, and likely to be unique. The same is true for the environment namespace. You can always find the "active" application with the variables prefixed with `SCIF_` (without ending in an application name) and any (sleeping / not active) application via the same variables, but ending in the application name. If you needed to discover all applications with labels, for example, you would search the list of environment names to find those that start with `SCIF_APPLABELS_`

```
 ./cowsay exec lolcat env | grep SCIF_APPLABELS_
SCIF_APPLABELS_fortune=/scif/apps/fortune/scif/labels.json
SCIF_APPLABELS_cowsay=/scif/apps/cowsay/scif/labels.json
SCIF_APPLABELS_lolcat=/scif/apps/lolcat/scif/labels.json
```

And here we are looking at **all** the environment active for lolcat:

```
 ./cowsay exec lolcat env | grep lolcat
[lolcat] executing /usr/bin/env 
SCIF_APPDATA=/scif/data/lolcat
SCIF_APPNAME_lolcat=lolcat
SCIF_APPRUN=/scif/apps/lolcat/scif/runscript
SCIF_APPRECIPE=/scif/apps/lolcat/scif/lolcat.scif
SCIF_APPROOT=/scif/apps/lolcat
SCIF_APPLIB_lolcat=/scif/apps/lolcat/lib
SCIF_APPMETA_lolcat=/scif/apps/lolcat/scif
SCIF_APPBIN_lolcat=/scif/apps/lolcat/bin
SCIF_APPNAME=lolcat
SCIF_APPHELP_lolcat=/scif/apps/lolcat/scif/runscript.help
SCIF_APPLIB=/scif/apps/lolcat/lib
SCIF_APPMETA=/scif/apps/lolcat/scif
SCIF_APPBIN=/scif/apps/lolcat/bin
SCIF_APPHELP=/scif/apps/lolcat/scif/runscript.help
SCIF_APPENV_lolcat=/scif/apps/lolcat/scif/environment.sh
SCIF_APPENV=/scif/apps/lolcat/scif/environment.sh
SCIF_APPLABELS_lolcat=/scif/apps/lolcat/scif/labels.json
SCIF_APPTEST_lolcat=/scif/apps/lolcat/scif/test.sh
SCIF_APPDATA_lolcat=/scif/data/lolcat
SCIF_APPRUN_lolcat=/scif/apps/lolcat/scif/runscript
SCIF_APPRECIPE_lolcat=/scif/apps/lolcat/scif/lolcat.scif
SCIF_APPROOT_lolcat=/scif/apps/lolcat
SCIF_APPLABELS=/scif/apps/lolcat/scif/labels.json
SCIF_APPTEST=/scif/apps/lolcat/scif/test.sh
...
PATH=/scif/apps/lolcat/bin:/opt/conda/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PWD=/scif/apps/lolcat
LD_LIBRARY_PATH=/scif/apps/lolcat/lib:/.singularity.d/libs
BEST_APP=lolcat
```

Notice a few things!

 - the specific environment (`%appenv lolcat`) is active because `BEST_APP` is lolcat
 - the lib folder in lolcat's base is added to the LD_LIBRARY_PATH
 - the bin folder is added to the path
 - locations for lolcat data are exposed. It's up to you how you use these, but you can predictably know that a well made app will look for it's data in it's specific folder.
 - environment variables are provided for the applications's root, it's data, and it's name

As mentioned previously, if you need to interact with other application's during the execution of an application, the base and data folders are provided too (note that below we are filtering to "fortune" when lolcat is active):

```
./cowsay exec lolcat env | grep fortune
SCIF_APPLABELS_fortune=/scif/apps/fortune/scif/labels.json
SCIF_APPTEST_fortune=/scif/apps/fortune/scif/test.sh
SCIF_APPDATA_fortune=/scif/data/fortune
SCIF_APPRUN_fortune=/scif/apps/fortune/scif/runscript
SCIF_APPRECIPE_fortune=/scif/apps/fortune/scif/fortune.scif
SCIF_APPROOT_fortune=/scif/apps/fortune
SCIF_APPNAME_fortune=fortune
SCIF_APPLIB_fortune=/scif/apps/fortune/lib
SCIF_APPMETA_fortune=/scif/apps/fortune/scif
SCIF_APPBIN_fortune=/scif/apps/fortune/bin
SCIF_APPHELP_fortune=/scif/apps/fortune/scif/runscript.help
SCIF_APPENV_fortune=/scif/apps/fortune/scif/environment.sh
```

Also provided are more global paths for data and apps:

```
SCIF_APPS=/scif/apps
SCIF_DATA=/scif/data
```


## Cowsay Container
Now let's go through the tutorial to use our cowsay container! We will show the equivalent commands for Docker and Singularity, using a Scientific Filesystem entrypoint.

```
$ ./cowsay apps
$ docker run vanessa/cowsay apps
  cowsay
  fortune
  lolcat
```

Ask for help for a specific app!

```
$ ./cowsay help fortune
$ docker run vanessa/cowsay help fortune
fortune is the best app
```

Ask for help for all apps, without knowing in advance what they are:

```
for app in $(./cowsay apps)
   do
     ./cowsay help $app
done
    cowsay is the best app
    fortune is the best app
    lolcat is the best app
```

Run a particular app

```
$ ./cowsay run fortune
$ docker run vanessa/cowsay run fortune
[fortune] executing /bin/bash /scif/apps/fortune/scif/runscript
	My dear People.
	My dear Bagginses and Boffins, and my dear Tooks and Brandybucks,
and Grubbs, and Chubbs, and Burrowses, and Hornblowers, and Bolgers,
Bracegirdles, Goodbodies, Brockhouses and Proudfoots.  Also my good
Sackville Bagginses that I welcome back at last to Bag End.  Today is my
one hundred and eleventh birthday: I am eleventy-one today!"
		-- J. R. R. Tolkien

```
You can add `--quiet` to suppress verbosity from scif.

```
$ ./cowsay --quiet run fortune
$ docker run vanessa/cowsay --quiet run fortune
```

Advanced running - pipes!

```
echo "Moo Moo Milk, it's the best" | ./cowsay run cowsay

[cowsay] executing /bin/bash /scif/apps/cowsay/scif/runscript
 _____________________________
< Moo Moo Milk, it's the best >
 -----------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
