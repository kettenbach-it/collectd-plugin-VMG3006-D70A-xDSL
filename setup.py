from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='collectd-plugin-VMG3006-xDSL',
    version='1.0.2',
    packages=['VMG3006_xDSL'],
    url='https://github.com/kettenbach-it/collectd-plugin-VMG3006-D70A-xDSL',
    license='GPL v3',
    author='Volker Kettenbach',
    author_email='volker@ktnbch.de',
    description='A collectd module written in Python for getting the xDSL status of Zyxel VMG3006 VDSL2 supervectoring modems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages',
        'Source': 'https://github.com/kettenbach-it/collectd-plugin-VMG3006-D70A-xDSL',
    },
    install_requires=[
        "beautifulsoup4==4.9.3",
        "requests"
    ],
    classifiers=[
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: System :: Monitoring"
    ],
    keywords='Zyxel VMG3006 xDSL collectd'
)
