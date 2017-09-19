%apprun hello-world-julia
    exec julia $SINGULARITY_APPROOT/hello-world.jl
%appfiles hello-world-julia
    hello-world.jl
%appinstall hello-world-julia
    apt-get install -y julia
