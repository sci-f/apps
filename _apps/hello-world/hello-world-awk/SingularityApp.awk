%apprun hello-world-awk
    exec awk -f $SINGULARITY_APPROOT/hello-world.awk
%appfiles hello-world-awk
    hello-world.awk
