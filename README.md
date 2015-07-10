# sasCIFtools
Tools for processing sasCIF files

## About sasCIF
**sasCIF** is a format for storage and exchange small angle scattering (SAS) data, that includes different types of data used during data analysis and modelling. The sasCIF format is a part of Crystallographic Information Framework (CIF), which is a system of standards and specifications for the exchange and archiving for structural biology data. Single sasCIF file typically contains a scattering curve, pair-distance distribution p(r), model(s) built using the scattering data and corresponding fit(s) as well as various metainformation about sample, experimental conditions, beamline, etc. The full description of all categories used in current version of sasCIF can be found at http://mmcif.wwpdb.org/dictionaries/mmcif_sas.dic/Index/index.html

## About sasCIFtools
**sasCIFtools** is a set of python scripts designed to process sasCIF files. The main purpose of the tools is to covert traditionally used SAS data files to sasCIF and *vice versa*
