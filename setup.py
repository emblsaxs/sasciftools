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
