%apprun julia
    exec julia $SINGULARITY_APPROOT/hello-world.jl
%appfiles julia
    hello-world.jl
%appinstall julia
    apt-get install -y julia
