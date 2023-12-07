# the_libs
#### Useful libs at a git clone fingertip

# custom kernel in pangeo.chs.usgs.gov

## How to Add a Python 3 Kernel to Jupyter IPython

    Prerequisites.
    Step 1: Create a local Conda Env.
    Step 2: Activate the Conda Environment.
    Step 3: Install the IPython Kernel Package.
    Step 4: Register the Kernel with Jupyter.
    Step 5: Verify and Use the New Kernel.

## Create a local persistent conda env - example nlcd2
```

 582  conda create --prefix ~/nlcd2 -f environment
  583  conda deactivate
  584  conda activate base
  587  conda create --prefix ~/nlcd2 
  588  conda activate /home/jovyan/nlcd2
  589  conda install mamba
  594  mamba env update --file environment.yml 

```

#### python -m ipykernel install --user --name=my-python3-kernel
