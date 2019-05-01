# rvit

rvit is a python package that provides a Realtime Visualization and Interaction Toolkit.

## Use

This is a standard python package, so you can use it through the normal dependancy toolchain, by adding `'rvit @ git+https://github.com/matthew-egbert/rvit.git',` as a dependancy to your `install_requires` in `setup.py`. The sample `setup.py` used by the quickstart project has:
```python
  setup(
    #...
    install_requires=[
        'rvit @ git+https://github.com/matthew-egbert/rvit.git',
        'kivy @ git+https://github.com/kivy/kivy.git',
        'cython',
        'jinja2',
        'numpy',
        'pygame',
    ],
    #...
  )
```

The quickstart project demonstrates how to...

## Install

You can install a quickstart project plus all the dependencies by...

You will need Python 3.5 or later first. If you do not already have this on your system, you can get it from [python.org](https://python.org), or by using your system's package manager.

Install pip and virtualenv - you can do this through a package manager such as apt, emerge, or brew, if you have one. For example, with emerge:

`sudo emerge --ask dev-python/pip virtualenv`

Create a virtualenv and install dependencies:
`virtualenv env && source ./env/bin/activate && pip install cookiecutter`

If you have already activated a virtualenv, and you need to reinstall a fresh virtualenv and example code, you can run this command instead:
`deactivate && rm -rf rvit_example env && virtualenv env && source ./env/bin/activate && pip install cookiecutter`

Create, install, and run an example application:
`cookiecutter -f --no-input gh:flaviusb/rvit-template && pip install -U --upgrade-strategy eager -e rvit_example && rvit_example
