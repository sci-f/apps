%apprun python
    exec python $SINGULARITY_APPROOT/hello-world.py
%appfiles python
    hello-world.py
%appinstall python
    apt-get install -y python python-dev
