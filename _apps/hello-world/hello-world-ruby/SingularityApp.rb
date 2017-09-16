%apprun ruby
    exec ruby $SINGULARITY_APPROOT/hello-world.rb
%appfiles ruby
    hello-world.rb
%appinstall ruby
    apt-get install -y ruby
