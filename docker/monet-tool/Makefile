cat:
	cat Makefile


BASE=monet-runner-base

base:
	docker build -t ${BASE} -f Dockerfile.base .


run:
	docker run -it ${BASE} bash


IMAGE=tbutzer/monet-tool
build:
	docker build -t ${IMAGE} -f Dockerfile .



fix-docker:
	        sudo cp daemon.json /etc/docker/daemon.json
		sudo reboot
