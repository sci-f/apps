%apprun R
    exec Rscript $SINGULARITY_APPROOT/hello-world.R
%appfiles R
    hello-world.R
%appinstall R
    apt-get install -y r-base
