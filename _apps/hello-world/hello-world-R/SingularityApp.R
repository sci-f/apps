%apprun hello-world-R
    exec Rscript $SINGULARITY_APPROOT/hello-world.R
%appfiles hello-world-R
    hello-world.R
%appinstall hello-world-R
    apt-get install -y r-base
