from setuptools import setup

setup(
    name='sasciftools',
    description='Package for reading and writing files in sascif format',
    url='https://github.com/mkachala/sasciftools',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=[
        'sasciftools',
        'sasciftools.mmCif',
        'sasciftools.sasCIFtoolbox',
    ],
    entry_points={
        'console_scripts': [
            'cif2all=scripts.cif2all:main',
            'cif2dat=scripts.cif2dat:main',
            'cif2fit=scripts.cif2fit:main',
            'cif2out=scripts.cif2out:main',
            'cif2pdb=scripts.cif2pdb:main',
            'cif2sub=scripts.cif2sub:main',
            'dat2cif=scripts.dat2cif:main',
            'fit2cif=scripts.fit2cif:main',
            'out2cif=scripts.out2cif:main',
            'pdb2cif=scripts.pdb2cif:main',
        ],
    },
)
