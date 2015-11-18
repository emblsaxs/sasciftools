import collections
import re

from . import cifutils
cifutils.getSaxsDocLibPath()
import saxsdocument


class sasdata(object):
    def __init__(self, filename, sasCIFdict):
        self.sasfile = saxsdocument.read(filename)
        self.filename = filename
        self.sasCIFdict = sasCIFdict

    def addProp(self, propDict, propName, data_block_id, category, data_item, parentCategory='', pointerName=''):
        if propName in propDict:
            if category not in self.sasCIFdict[data_block_id]:
                self.sasCIFdict[data_block_id][category] = collections.OrderedDict()
                self.sasCIFdict[data_block_id][category]['id'] = 1
            try:
                self.sasCIFdict[data_block_id][category][data_item] = float(propDict[propName])
            except ValueError:
                self.sasCIFdict[data_block_id][category][data_item] = propDict[propName]
            if pointerName and parentCategory:
                self.sasCIFdict[data_block_id][parentCategory][pointerName] = \
                    self.sasCIFdict[data_block_id][category]['id']

    def addMeta(self, data_block_id=''):
        if not data_block_id:
            data_block_id = self.sasCIFdict.keys()[0]
        if data_block_id not in self.sasCIFdict.keys():
            self.sasCIFdict[data_block_id] = collections.OrderedDict()

        propDict = self.sasfile.property

        self.addProp(propDict, 'Wavelength [nm]', data_block_id, '_sas_beam', 'radiation_wavelength',
                     '_sas_scan', 'beam_id')
        self.addProp(propDict, 'Cell Temperature [C]', data_block_id, '_sas_scan', 'cell_temperature')
        self.addProp(propDict, 'Storage Temperature [C]', data_block_id, '_sas_scan', 'storage_temperature')
        self.addProp(propDict, 'Exposure time [s]', data_block_id, '_sas_scan', 'exposure_time')
        self.addProp(propDict, 'Timestamp (begin)', data_block_id, '_sas_scan', 'measurement_date')
        if 'measurement_date' in self.sasCIFdict[data_block_id]['_sas_scan'].keys():
            self.sasCIFdict[data_block_id]['_sas_scan']['measurement_date'] = \
                self.sasCIFdict[data_block_id]['_sas_scan']['measurement_date'].split()[0]
        self.addProp(propDict, 'beam-center-x', data_block_id, '_sas_detc', 'beam-position-x', '_sas_scan', 'detc_id')
        self.addProp(propDict, 'beam-center-y', data_block_id, '_sas_detc', 'beam-position-y', '_sas_scan', 'detc_id')
        self.addProp(propDict, 'sample-code', data_block_id, '_sas_sample', 'name', '_sas_scan', 'sample_id')
        self.addProp(propDict, 'sample-description', data_block_id, '_sas_sample', 'details', '_sas_scan', 'sample_id')
        self.addProp(propDict, 'sample-concentration', data_block_id, '_sas_sample', 'specimen_concentration',
                     '_sas_scan', 'sample_id')
        
    def addDat(self, unit='nanometer', data_block_id='', intensity_id='', result_id=1):
        curves = self.sasfile.curve
        sasCIFdict = self.sasCIFdict

        s = [str('%14E' % value) for value in list(zip(*curves[0])[0])]
        I = [str('%14E' % value) for value in list(zip(*curves[0])[1])]
        err = [str('%14E' % value) for value in list(zip(*curves[0])[2])]

        # If data_block is not specified, then write in the first one
        if not data_block_id:
            data_block_id = sasCIFdict.keys()[0]
        if data_block_id not in sasCIFdict.keys():
            sasCIFdict[data_block_id] = collections.OrderedDict()

        if not intensity_id:
            intensity_id = 1

        if '_sas_scan_intensity' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id]['_sas_scan_intensity'] = collections.OrderedDict()
        sasCIFdict[data_block_id]['_sas_scan_intensity']['id'] = range(1, len(s) + 1)
        sasCIFdict[data_block_id]['_sas_scan_intensity']['momentum_transfer'] = s
        sasCIFdict[data_block_id]['_sas_scan_intensity']['intensity'] = I
        sasCIFdict[data_block_id]['_sas_scan_intensity']['intensity_su_counting'] = err
        sasCIFdict[data_block_id]['_sas_scan_intensity']['scan_id'] = [intensity_id] * len(s)

        if '_sas_scan' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id]['_sas_scan'] = collections.OrderedDict()
        sasCIFdict[data_block_id]['_sas_scan']['id'] = intensity_id
        sasCIFdict[data_block_id]['_sas_scan']['result_id'] = result_id
        sasCIFdict[data_block_id]['_sas_scan']['unit'] = unit
        sasCIFdict[data_block_id]['_sas_scan']['qmin'] = str('%.4f' % float(s[0]))
        sasCIFdict[data_block_id]['_sas_scan']['qmax'] = str('%.4f' % float(s[-1]))

    def addFit(self, unit='nanometer', fitting_id=1, data_block_id='', result_id=1):
        sasCIFdict = self.sasCIFdict

        # Parse Chi^2
        chi = ''
        chifile = open(self.filename, "r")
        for line in chifile:
            if ('Chi' in line) or ('chi' in line):
                par = filter(None, re.split(' |:|=|\n|\r', line))
                chi_name = [p for p in par if ("Chi" in p) or ("chi" in p)][0]
                chi = par[par.index(chi_name) + 1]
                if '^2' not in chi_name:
                    try:
                        chi = float(chi) ** 2
                    except TypeError:
                        chi = "."
        chifile.close()

        # Read fit
        curves = self.sasfile.curve
        s = [str('%14E' % value) for value in list(zip(*curves[0])[0])]
        I = [str('%14E' % value) for value in list(zip(*curves[0])[1])]
        if len(curves) == 1:
            # very rare case
            fit = [str('%14E' % value) for value in list(zip(*curves[0])[-1])]
        else:
            fit = [str('%14E' % value) for value in list(zip(*curves[1])[1])]

        # If data_block is not specified, then write in the first one
        if not data_block_id:
            data_block_id = sasCIFdict.keys()[0]
        if data_block_id not in sasCIFdict.keys():
            sasCIFdict[data_block_id] = collections.OrderedDict()

        if '_sas_model_fitting_details' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id]['_sas_model_fitting_details'] = collections.OrderedDict()
        sasCIFdict[data_block_id]['_sas_model_fitting_details']['id'] = fitting_id
        sasCIFdict[data_block_id]['_sas_model_fitting_details']['result_id'] = result_id
        sasCIFdict[data_block_id]['_sas_model_fitting_details']['unit'] = unit
        sasCIFdict[data_block_id]['_sas_model_fitting_details']['chi_square'] = str(chi)

        if '_sas_model_fitting' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id]['_sas_model_fitting'] = collections.OrderedDict()
        sasCIFdict[data_block_id]['_sas_model_fitting']['id'] = [fitting_id] * len(s)
        sasCIFdict[data_block_id]['_sas_model_fitting']['ordinal'] = range(1, len(s) + 1)
        sasCIFdict[data_block_id]['_sas_model_fitting']['momentum_transfer'] = s
        sasCIFdict[data_block_id]['_sas_model_fitting']['intensity'] = I
        sasCIFdict[data_block_id]['_sas_model_fitting']['fit'] = fit

    def addOut(self, data_block_id='', pr_id=1, intensity_id=1):
        properties = self.sasfile.property
        curves = self.sasfile.curve
        sasCIFdict = self.sasCIFdict

        # Read intensities
        s_extrp = [str('%14E' % value) for value in list(zip(*curves[2])[0])]
        I_extrp = [str('%14E' % value) for value in list(zip(*curves[2])[1])]

        # Read p(r)
        r = [str('%14E' % value) for value in list(zip(*curves[3])[0])]
        p = [str('%14E' % value) for value in list(zip(*curves[3])[1])]
        err = [str('%14E' % value) for value in list(zip(*curves[3])[2])]

        # If data_block is not specified, then write in the first one
        if not data_block_id:
            data_block_id = sasCIFdict.keys()[0]
        if data_block_id not in sasCIFdict.keys():
            sasCIFdict[data_block_id] = collections.OrderedDict()

        if '_sas_p_of_R_details' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id][
                '_sas_p_of_R_details'] = collections.OrderedDict()
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['id'] = pr_id
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['intensity_id'] = intensity_id
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['software_p_of_R'] = \
            properties['creator'] + ' ' + properties['creator-version']
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['number_of_points'] = len(curves[0])
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['qmin'] = curves[0][0][0]
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['qmax'] = curves[0][-1][0]
        if 'leading-points-omitted' in properties.keys():
            leading_points_omitted = int(properties['leading-points-omitted'])
        else:
            leading_points_omitted = 0
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['p_of_R_point_min'] = \
            leading_points_omitted + 1
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['p_of_R_point_max'] = \
            leading_points_omitted + len(curves[0])
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['Rmin'] = str(curves[3][0][0])
        sasCIFdict[data_block_id]['_sas_p_of_R_details']['Rmax'] = str(curves[3][-1][0])

        if '_sas_p_of_R' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id]['_sas_p_of_R'] = collections.OrderedDict()
        sasCIFdict[data_block_id]['_sas_p_of_R']['id'] = [pr_id] * len(r)
        sasCIFdict[data_block_id]['_sas_p_of_R']['ordinal'] = range(1, len(r) + 1)
        sasCIFdict[data_block_id]['_sas_p_of_R']['r'] = r
        sasCIFdict[data_block_id]['_sas_p_of_R']['P'] = p
        sasCIFdict[data_block_id]['_sas_p_of_R']['P_error'] = err

        if '_sas_p_of_R_extrapolated_intensity' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated_intensity'] = collections.OrderedDict()
        sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated_intensity']['id'] = [pr_id] * len(s_extrp)
        sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated_intensity']['ordinal'] = range(1, len(s_extrp) + 1)
        sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated_intensity']['momentum_transfer'] = s_extrp
        sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated_intensity']['intensity_reg'] = I_extrp


class pdbdata(object):
    def __init__(self, filename, sasCIFdict):
        self.pdbfile = open(filename)
        self.sasCIFdict = sasCIFdict

    def addAtoms(self, data_block_id='', sas_model_id='', fitting_id=''):
        sasCIFdict = self.sasCIFdict
        # Create model
        if not data_block_id:
            data_block_id = "MODEL_1"
        if data_block_id not in sasCIFdict.keys():
            sasCIFdict[data_block_id] = collections.OrderedDict()

        if not sas_model_id:
            sas_model_id = 1

        if '_sas_model' not in sasCIFdict[data_block_id].keys():
            sasCIFdict[data_block_id]['_sas_model'] = collections.OrderedDict()
            sasCIFdict[data_block_id]['_sas_model']['id'] = sas_model_id
            sasCIFdict[data_block_id]['_sas_model']['fitting_id'] = fitting_id

        # Create empty lists for categories
        group_PDB = []
        atom_id = []
        auth_atom_id = []
        label_alt_id = []
        auth_comp_id = []
        auth_asym_id = []
        auth_seq_id = []
        pdbx_PDB_ins_code = []
        Cartn_x = []
        Cartn_y = []
        Cartn_z = []
        occupancy = []
        B_iso_or_equiv = []
        type_symbol = []
        pdbx_formal_charge = []

        model_list = []

        for line in self.pdbfile:
            if line[0:4] == 'ATOM':
                group_PDB.append(line[0:4].strip())
                atom_id.append(line[6:11].strip())
                auth_atom_id.append(line[12:16].strip())
                label_alt_id.append(line[16].strip())
                auth_comp_id.append(line[17:20].strip())
                auth_asym_id.append(line[21].strip())
                auth_seq_id.append(line[22:26].strip())
                pdbx_PDB_ins_code.append(line[26].strip())
                Cartn_x.append(line[30:38].strip())
                Cartn_y.append(line[38:46].strip())
                Cartn_z.append(line[46:54].strip())
                occupancy.append(line[54:60].strip())
                B_iso_or_equiv.append(line[60:66].strip())
                type_symbol.append(line[76:78].strip())
                pdbx_formal_charge.append(line[78:80].strip())
                model_list.append(sas_model_id)

        empty_column = ['?'] * len(group_PDB)

        if group_PDB:
            if '_atom_site' not in sasCIFdict[data_block_id].keys():
                sasCIFdict[data_block_id]['_atom_site'] = collections.OrderedDict()
            sasCIFdict[data_block_id]['_atom_site']['group_PDB'] = group_PDB
            sasCIFdict[data_block_id]['_atom_site']['id'] = atom_id
            sasCIFdict[data_block_id]['_atom_site']['type_symbol'] = type_symbol
            sasCIFdict[data_block_id]['_atom_site']['label_atom_id'] = auth_atom_id
            sasCIFdict[data_block_id]['_atom_site']['label_alt_id'] = label_alt_id
            sasCIFdict[data_block_id]['_atom_site']['label_comp_id'] = auth_comp_id
            sasCIFdict[data_block_id]['_atom_site']['label_asym_id'] = auth_asym_id
            sasCIFdict[data_block_id]['_atom_site']['label_entity_id'] = model_list
            sasCIFdict[data_block_id]['_atom_site']['label_seq_id'] = auth_seq_id
            sasCIFdict[data_block_id]['_atom_site']['pdbx_PDB_ins_code'] = pdbx_PDB_ins_code
            sasCIFdict[data_block_id]['_atom_site']['Cartn_x'] = Cartn_x
            sasCIFdict[data_block_id]['_atom_site']['Cartn_y'] = Cartn_y
            sasCIFdict[data_block_id]['_atom_site']['Cartn_z'] = Cartn_z
            sasCIFdict[data_block_id]['_atom_site']['occupancy'] = occupancy
            sasCIFdict[data_block_id]['_atom_site']['B_iso_or_equiv'] = B_iso_or_equiv
            sasCIFdict[data_block_id]['_atom_site']['Cartn_x_esd'] = empty_column
            sasCIFdict[data_block_id]['_atom_site']['Cartn_y_esd'] = empty_column
            sasCIFdict[data_block_id]['_atom_site']['Cartn_z_esd'] = empty_column
            sasCIFdict[data_block_id]['_atom_site']['occupancy_esd'] = empty_column
            sasCIFdict[data_block_id]['_atom_site']['B_iso_or_equiv_esd'] = empty_column 
            sasCIFdict[data_block_id]['_atom_site']['pdbx_formal_charge'] = pdbx_formal_charge
            sasCIFdict[data_block_id]['_atom_site']['auth_seq_id'] = auth_seq_id
            sasCIFdict[data_block_id]['_atom_site']['auth_comp_id'] = auth_comp_id
            sasCIFdict[data_block_id]['_atom_site']['auth_asym_id'] = auth_asym_id
            sasCIFdict[data_block_id]['_atom_site']['auth_atom_id'] = auth_atom_id
            sasCIFdict[data_block_id]['_atom_site']['pdbx_PDB_model_num'] = [sas_model_id] * len(group_PDB) 
