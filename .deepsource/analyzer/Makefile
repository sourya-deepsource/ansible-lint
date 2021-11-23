build:
	cp -r ../../. /app
	# Add custom build steps
	apk add python3 py3-pip
	mkdir /toolbox/venv
	pip3 install --target=/toolbox/venv "ansible-lint[community,yamllint]"
