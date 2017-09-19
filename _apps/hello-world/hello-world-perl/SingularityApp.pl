%apprun hello-world-perl
    exec perl6 $SINGULARITY_APPROOT/hello-world.pl
%appfiles hello-world-perl
    hello-world.pl
%appinstall hello-world-perl
    apt-get install -y perl6
