build:
	apk update
	cp -r ../../. /app
	# Add custom build steps
	apk add python3 python3-dev py3-pip build-base libffi-dev libressl-dev rust cargo
	mkdir /toolbox/venv
	pip3 install wheel
	pip3 install --target=/toolbox/venv "ansible-lint[community,yamllint]"
