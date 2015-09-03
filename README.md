# sasCIFtools
**sasCIFtools** is a set of python scripts designed to process sasCIF files. The main purpose of the tools is to convert file formats traditionally used for SAS data analysis to sasCIF and *vice versa*. sasCIFtools reuqire installed [ATSAS package 2.6.1](http://www.embl-hamburg.de/biosaxs/software.html) and [python 2.7.6](https://www.python.org/downloads/).

## About sasCIF
**sasCIF** is a format for storage and exchange small angle scattering (SAS) data, that includes different types of data used during data analysis and modelling. The sasCIF format is a part of Crystallographic Information Framework (CIF), which is a system of standards and specifications for the exchange and archiving for structural biology data. Single sasCIF file typically contains a scattering curve, pair-distance distribution *p*(*r*), model(s) built using the scattering data and corresponding fit(s) as well as various metainformation about sample, experimental conditions, beamline, etc. The full description of all categories used in current version of sasCIF can be found at http://mmcif.wwpdb.org/dictionaries/mmcif_sas.dic/Index/index.html

### How to view models stored in sasCIF with molecular visualization software

To view the models in sasCIF files you can use programs **RasMol/RasWin** (only the first model will be displayed) or **Jmol** and **PyMOL** (each model is opened as a separate state). 

Currently, PyMOL does not natively support sasCIF, so to correctly open sasCIF files you can either use load command in PyMOl specifying file and format:

```load <FILENAME>.sascif, format = cif```

or run PyMOL from command line with -d option using with the string above:

```pymol -d "load <FILENAME>.sascif, format = cif"``` 

## Structure and content of sasCIF tools
sasCIFtools consist of three parts:

1. [Standalone python scripts](#standalone-tools) command line tools, which convert sasCIF files.

2. [sasCIFtoolbox Package](#sasciftoolbox), which contains python classes and methods for processing sasCIF and traditional SAS data files.

3. Modifed [mmCIF library](https://github.com/glenveegee/PDBeCIF) to read and write CIF files developed at EMBL-EBI by Glen van Ginkel. The library was modified for sasCIFtools to use Ordered Dictionaries instead of generic ones to preserve the order of items and data blocks in sasCIF files.

### Standalone tools

There are two kinds of standalone tools to add data to sasCIF files (import tools) and to extract data form them (export tools). The tools are named according to the following convention: `format_a2format_b`, where the format_a is the original format and format_b is destination format, e.g. `cif2dat` extracts scattering curve from the sasCIF file in the .dat format.

#### Import tools

All import tools have similar interface:

```
    ./format2cif.py [-i <INPUT sasCIF FILE>] [-o <OUTPUT sasCIF FILE>] <DATAFILE>
```

* `dat2cif.py` adds scattering curve from .dat file
* `out2cif.py` adds distance distribution function *p*(*r*) with extrapolated and regularized scattering curve from GNOM generated .out file
* `pdb2cif.py` adds PDB model to a sasCIF file
* `fit2cif.py` adds calculated cattering from PDB model to a sasCIF file from .fit or .fir file


#### Export tools

All export tools except for `cif2all` have similar interface:

```
    ./cif2format.py <DATAFILE>
```

* `cif2dat.py` extracts scattering curve as three-column .dat file
* `cif2out.py` extracts distance distribution function *p*(*r*) as standard GNOM .out file
* `cif2pdb.py` extracts PDB model. A sasCIF file may contain several models, each in its own data block, the individual models are saved onto separate files that have more complex filename templates reflecting the correspondence between the models extracted from sasCIF and the model fits: `<sascif_filename>_FIT_<fit_id>_MODEL_<model_id>.pdb`.
* `cif2fit.py` extracts fit to experimental data as three-column .fit file. As a sasCIF file may include several fits and the models are written into individual separate files with the following naming convention: `<sascif_filename>_FIT_<fit_id>.fit`.
* `cif2sub.py` extracts metadata as .txt file

* `cif2all.py` extracts all types of data mentioned above. The tool has following interface:

	```
	./cif2all.py [-o <output folder>] <input file>
	```

	If no output folder is specified, then the the output data files are written to the current directory. **cif2all** names output files according to the file structure: if file has only one *MAIN* data block (the one with the scattering curve), then the .dat and .out files have name of the input sasCIF file. Otherwise for each *MAIN* data block separate files are created with names containing both filename and data block name. The .fit and .pdb files are named following the conventions described above for **cif2pdb** and **cif2fit** tools.

###sasCIFtoolbox

**sasCIFtoolbox** module include four python modules and one .ini file. Here only the general information about the models and their content is provided, the details are presented in the docstrings of the corresponding files.   

* `import_tools.py`: contains two classes **sasdata** and **pdbdata**, the former is used to add small angle scattering data from .dat, .out and .fit files and the latter to add atomic coordinates from .pdb files to sasCIF files

* `export_tools.py`: contains one class **sasCIFsource** to extract all types of data from the sasCIF files to corresponding data files

* `cifutils.py`: contains functions to facilitate processing of sasCIF files and operation of standalone tools

* `writesaxsdoc.py`: contains one class **saxsdocout** to write SAS data files in ATSAS format
    
* `sasCIFtools.ini`: contains path to the ATSAS python libraries if ATSAS is not installed to default location. The default location is `/usr/lib/x86_64-linux-gnu/atsas/python2.7/dist-packages/`.

More details about the components of sasCIFtoolbox can be found in the scripts source code.
