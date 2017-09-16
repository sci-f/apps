%apprun perl
    exec perl6 $SINGULARITY_APPROOT/hello-world.pl
%appfiles perl
    hello-world.pl
%appinstall perl
    apt-get install -y perl6
