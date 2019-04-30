Install python 3.5+. Go to python.org for details of how to do this on your platform.

Install pip and virtualenv - you can do this through a package manager such as apt, emerge, or brew, if you have one. For example, with emerge:

`sudo emerge --ask dev-python/pip virtualenv`

Create a virtualenv and install dependencies:
`virtualenv env && source ./env/bin/activate && pip install cookiecutter`

If you have already activated a virtualenv, and you need to reinstall a fresh virtualenv and example code, you can run this command instead:
`deactivate && rm -rf rvit_example env && virtualenv env && source ./env/bin/activate && pip install cookiecutter`

Create, install, and run an example application:
`cookiecutter -f --no-input gh:flaviusb/rvit-template && pip install -U --upgrade-strategy eager -e rvit_example && rvit_example`
