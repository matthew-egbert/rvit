from setuptools import setup

setup(name='rvit',
      version='0.1',
      description='Realtime interaction and visualization toolkit for scientists',
      url='http://matthewegbert.com',
      author='Matthew Egbert',
      author_email='mde@matthewegbert.com',
      license='GPLv3',
      packages=['rvit'],
      install_requires=['kivy', 'cython', 'jinja2'],
      zip_safe=False)
