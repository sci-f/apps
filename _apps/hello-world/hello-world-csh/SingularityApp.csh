%apprun hello-world-csh
    exec csh $SINGULARITY_APPROOT/hello-world.csh
%appfiles hello-world-csh
    hello-world.csh
%appinstall hello-world-csh
    apt-get install -y csh
