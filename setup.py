from setuptools import setup

classifiers = """
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Operating System :: OS Independent
Programming Language :: Python :: 3
""".strip().splitlines()


setup(
    name='rvit',
    version='0.1',
    classifiers=classifiers,
    description='Realtime interaction and visualization toolkit for scientists',
    url='http://matthewegbert.com',
    author='Matthew Egbert',
    author_email='mde@matthewegbert.com',
    # packages=find_packages('src', exclude=['ez_setup']),
    # package_dir={'': 'src'},
    namespace_packages=['rvit'],
    license='GPLv3',
    packages=['rvit.core', 'rvit.core.widgets', 'rvit.core.shaders', 'rvit.core.fonts'],
    install_requires=[
        'kivy @ git+https://github.com/kivy/kivy.git',
        'cython',
        'jinja2',
        'numpy',
        'pygame',
    ],
    include_package_data=True,
    zip_safe=False,
)
