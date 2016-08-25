from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pytex',
    version='0.1.0',
    description='''A mixed language to automate compilation/scripting of Tex
    files''',
    url='https://github.com/legbt/pytex',
    author='LeGBT',
    author_email='cauchyunderground@gmail.com',
    license='GPLv3',
    classifiers=[
        #  1 - Planning
        #  2 - Pre-Alpha
        #  3 - Alpha
        #  4 - Beta
        #  5 - Production/Stable
        #  6 - Mature
        #  7 - Inactive
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Topic :: LaTeX',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='tex latex',
    py_modules=["pytex"],
    install_requires=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
