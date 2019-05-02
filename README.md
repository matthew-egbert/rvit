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

Then import it as needed.

The core functionality is provided through the package `rvit.core`, with widgets in `rvit.core.widgets`. Rvit builds upon kivy, but does not needlessly wrap this functionality - you can access it through kivy packages as if you were building a kivy project. The quickstart project demonstrates how to set up an application and use a `.kv` file to arrange a gui. Further documentation about the Kv file format can be found in the kivy documentation: [https://kivy.org/doc/stable/guide/lang.html](https://kivy.org/doc/stable/guide/lang.html)

## Install

If you want a base project to build from, you can install a quickstart project plus all the dependencies using cookiecutter.

You will need Python 3.5 or later first. If you do not already have this on your system, you can get it from [python.org](https://python.org), or by using your system's package manager.

Next, install pip and virtualenv - you can do this through a package manager such as apt, emerge, or brew, if you have one. For example, with emerge:

```bash
sudo emerge --ask dev-python/pip virtualenv
```

Alternatively, there are complete instructions for installing virtualenv and pip here: [https://virtualenv.pypa.io/en/stable/installation/](https://virtualenv.pypa.io/en/stable/installation/)


Create a virtualenv and install dependencies:

```bash
virtualenv env && source ./env/bin/activate && pip install cookiecutter
```

If you have already activated a virtualenv, and you need to reinstall a fresh virtualenv and example code, you can run this command instead:

```bash
deactivate && rm -rf rvit_example env && virtualenv env && source ./env/bin/activate && pip install cookiecutter
```

Create, install, and run an example application:

```bash
cookiecutter -f --no-input gh:flaviusb/rvit-template && pip install -U --upgrade-strategy eager -e rvit_example && rvit_example
```
