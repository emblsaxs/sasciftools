# Copyright (C) 2014-2015 European Molecular Biology Laboratory (EMBL)
#
# EMBL licenses this file to you under the Apache License,
# Version 2.0 ("the License"); you may not use this file
# except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


from setuptools import setup

setup(
    name='sasciftools',
    description='Package for reading and writing files in sascif format',
    url='https://github.com/mkachala/sasciftools',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        # Licence is "Apache License, Version 2.0" but the PyPI classifers
        # do not give a way to distinguish versions of the Apache License
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=[
        'sasciftools',
        'sasciftools.mmCif',
        'sasciftools.sasCIFtoolbox',
        'sasciftools.scripts',
    ],
    entry_points={
        'console_scripts': [
            'cif2all=sasciftools.scripts.cif2all:main',
            'cif2dat=sasciftools.scripts.cif2dat:main',
            'cif2fit=sasciftools.scripts.cif2fit:main',
            'cif2out=sasciftools.scripts.cif2out:main',
            'cif2pdb=sasciftools.scripts.cif2pdb:main',
            'cif2sub=sasciftools.scripts.cif2sub:main',
            'dat2cif=sasciftools.scripts.dat2cif:main',
            'fit2cif=sasciftools.scripts.fit2cif:main',
            'out2cif=sasciftools.scripts.out2cif:main',
            'pdb2cif=sasciftools.scripts.pdb2cif:main',
        ],
    },
)
