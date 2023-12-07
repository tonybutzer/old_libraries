cat:
	cat Makefile

down:
	wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
	mv Mamba* /tmp

install:
	bash /tmp/Mambaforge-Linux-x86_64.sh


cenv:
	mamba env create -f environment.yml


nuke:
	conda env remove -n libTest7


