import os
import collections

import cifutils
cifutils.getSaxsDocLibPath()
import writesaxsdoc as wsd
from subprocess import call
import saxsdocument


class sasCIFsource(object):

    def extractDat(self, sasCIFdict, sasCIFfile, data_block_id=''):
        
        sasCIFfile = os.path.split(sasCIFfile)[-1]
        
        if data_block_id:
            data_block_list = [data_block_id]
        else:
            data_block_list = sasCIFdict.keys()

        for data_block_id in data_block_list:
            if '_sas_scan_intensity' in sasCIFdict[data_block_id]:
                datfile = open(sasCIFfile[0:-7] + '.dat', 'w')
                table = [sasCIFdict[data_block_id]['_sas_scan_intensity']['momentum_transfer'],
                         sasCIFdict[data_block_id]['_sas_scan_intensity']['intensity'],
                         sasCIFdict[data_block_id]['_sas_scan_intensity']['intensity_su_counting']]

                writeDatFile = wsd.saxsdocout()
                writeDatFile.writeCurves(table, datfile)

                propList = ['unit', 'storage_temperature',
                            'cell_temperature', 'number_of_frames']

                propDict = collections.OrderedDict()
                for prop in propList:
                    if prop in sasCIFdict[data_block_id]['_sas_scan'].keys():
                        propDict[prop] = sasCIFdict[data_block_id]['_sas_scan'][prop]
                writeDatFile.writeProperties(propDict, datfile)
                datfile.close()

    def extractOut(self, sasCIFdict, sasCIFfile, data_block_id=''):
        
        sasCIFfile = os.path.split(sasCIFfile)[-1]
        
        if data_block_id:
            data_block_list = [data_block_id]
        else:
            data_block_list = sasCIFdict.keys()

        for data_block_id in data_block_list:
            if '_sas_p_of_R' in sasCIFdict[data_block_id]:
                outfile = open(sasCIFfile[0:-7] + '.out', 'w')

                intensityTable = [sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated']['momentum_transfer'],
                                  sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated']['intensity_reg']]
                intensityHeader = ['S', 'I REG']

                # Alignment of experimental and extrapolated intensities
                if '_sas_scan_intensity' in sasCIFdict[data_block_id]:
                    qmin = float(sasCIFdict[data_block_id]['_sas_p_of_R_details']['qmin'])
                    qmax = float(sasCIFdict[data_block_id]['_sas_p_of_R_details']['qmax'])
                    sIntensity = \
                        [float(x) for x in sasCIFdict[data_block_id]['_sas_scan_intensity']['momentum_transfer']]
                    firstPointIntensity = min(range(len(sIntensity)), key=lambda i: abs(sIntensity[i] - qmin))
                    lastPointIntensity = min(range(len(sIntensity)), key=lambda i: abs(sIntensity[i] - qmax)) + 1
                    sExtrapolated = [float(x) for x in intensityTable[0]]
                    firstPointExtrapolated = \
                        min(range(len(sExtrapolated)), key=lambda i: abs(sExtrapolated[i] - qmin))
                    lastPointExtrapolated = \
                        min(range(len(sExtrapolated)), key=lambda i: abs(sExtrapolated[i] - qmax)) + 1

                    # If the number of points were reduced by GNOM, then regrid
                    # the curve with DATREGRID
                    if not (lastPointIntensity - firstPointIntensity) \
                            == (lastPointExtrapolated - firstPointExtrapolated):
                        datFileInt = open('int.dat', 'w')
                        table = [sasCIFdict[data_block_id]['_sas_scan_intensity']['momentum_transfer'],
                                 sasCIFdict[data_block_id]['_sas_scan_intensity']['intensity'],
                                 sasCIFdict[data_block_id]['_sas_scan_intensity']['intensity_su_counting']]
                        writeDatFile = wsd.saxsdocout()
                        writeDatFile.writeCurves(table, datFileInt)
                        datFileInt.close()
                        datFileExt = open('ext.dat', 'w')
                        writeDatFile = wsd.saxsdocout()
                        writeDatFile.writeCurves(intensityTable, datFileExt)
                        datFileExt.close()
                        call(['datregrid', '-t', 'ext.dat', 'int.dat', '-o', 'intExt.dat'])
                        datFileIntExt = saxsdocument.read('intExt.dat').curve
                        call(['rm', 'ext.dat', 'int.dat', 'intExt.dat'])
                        scatVect = [float('%14E' % value)
                                    for value in list(zip(*datFileIntExt[0])[0])]
                        intensity = [str('%14E' % value)
                                     for value in list(zip(*datFileIntExt[0])[1])]
                        error = [str('%14E' % value)
                                 for value in list(zip(*datFileIntExt[0])[2])]
                        firstPointIntensity = \
                            min(range(len(scatVect)), key=lambda i: abs(scatVect[i] - qmin))
                        lastPointIntensity = \
                            min(range(len(scatVect)), key=lambda i: abs(scatVect[i] - qmax)) + 1
                    else:
                        intensity = sasCIFdict[data_block_id][
                            '_sas_scan_intensity']['intensity']
                        error = sasCIFdict[data_block_id][
                            '_sas_scan_intensity']['intensity_su_counting']

                    tailPoints = (lastPointExtrapolated - firstPointExtrapolated) - \
                        len(intensity[firstPointIntensity:lastPointIntensity])
                    Jexp = [' '] * firstPointExtrapolated + \
                        intensity[firstPointIntensity:lastPointIntensity] + [' '] * tailPoints
                    Error = [' '] * firstPointExtrapolated + \
                        error[firstPointIntensity:lastPointIntensity] + [' '] * tailPoints

                    Jreg = [' '] * firstPointExtrapolated + \
                        sasCIFdict[data_block_id]['_sas_p_of_R_extrapolated'][
                            'intensity_reg'][firstPointExtrapolated:]

                    intensityTable.insert(1, Jexp)
                    intensityTable.insert(2, Error)
                    intensityTable.insert(3, Jreg)
                    intensityHeader = ['S', 'J EXP', 'ERROR', 'J REG', 'I REG']

                pRTable = [sasCIFdict[data_block_id]['_sas_p_of_R']['r'],
                           sasCIFdict[data_block_id]['_sas_p_of_R']['P'],
                           sasCIFdict[data_block_id]['_sas_p_of_R']['P_error']]

                writeoutfile = wsd.saxsdocout()
                # Write creator&version
                creator, version = sasCIFdict[data_block_id]['_sas_p_of_R_details']['software_p_of_R'].split()
                writeoutfile.writeText(' '.join(creator) + ' Version ' + version + '\n', outfile)
                # Write curves
                writeoutfile.writeCurves(
                    intensityTable, outfile, intensityHeader)
                writeoutfile.writeText('           Distance distribution function of particle  \n', outfile)
                writeoutfile.writeCurves(
                    pRTable, outfile, ['R', 'P(R)', 'ERROR'])
                # Write properties
                propList = [
                    'Rg_from_Guinier', 'I0_from_Guinier', 'Rg_from_PR', 'I0_from_PR']
                propDict = collections.OrderedDict()
                for prop in propList:
                    if prop in sasCIFdict[data_block_id]['_sas_result'].keys():
                        propDict[prop] = sasCIFdict[data_block_id]['_sas_result'][prop]
                writeoutfile.writeProperties(propDict, outfile)
                outfile.close()

    def extractFit(self, sasCIFdict, sasCIFfile, data_block_id=''):

        sasCIFfile = os.path.split(sasCIFfile)[-1]
        
        if data_block_id:
            data_block_list = [data_block_id]
        else:
            data_block_list = sasCIFdict.keys()

        for data_block_id in data_block_list:
            if '_sas_model_fitting_details' in sasCIFdict[data_block_id]:
                writefitfile = wsd.saxsdocout()
                fit_id = sasCIFdict[data_block_id]['_sas_model_fitting_details']['id']
                fitfile = open(sasCIFfile[0:-7] + '_FIT_' + fit_id + '.fit', 'w')
                if 'chi_square' in sasCIFdict[data_block_id]['_sas_model_fitting_details'].keys() and \
                        sasCIFdict[data_block_id]['_sas_model_fitting_details']['chi_square'] != '.':
                    chi_sq = {'Chi^2': sasCIFdict[data_block_id]['_sas_model_fitting_details']['chi_square']}
                    writefitfile.writeProperties(chi_sq, fitfile)
                if 'p_value' in sasCIFdict[data_block_id]['_sas_model_fitting_details'].keys() and \
                        sasCIFdict[data_block_id]['_sas_model_fitting_details']['p_value'] != '.':
                    p_val = {'p_value': sasCIFdict[data_block_id]['_sas_model_fitting_details']['p_value']}
                    writefitfile.writeProperties(p_val, fitfile)
                table = [sasCIFdict[data_block_id]['_sas_model_fitting']['momentum_transfer'],
                         sasCIFdict[data_block_id]['_sas_model_fitting']['intensity'],
                         sasCIFdict[data_block_id]['_sas_model_fitting']['fit']]
                writefitfile.writeCurves(table, fitfile)
                fitfile.close()

    def extractAtoms(self, sasCIFdict, sasCIFfile, data_block_id=''):
        
        sasCIFfile = os.path.split(sasCIFfile)[-1]
        
        if data_block_id:
            data_block_list = [data_block_id]
        else:
            data_block_list = sasCIFdict.keys()

        pdbTemplateDict = collections.OrderedDict()
        pdbTemplateDict['group_PDB'] = 6
        pdbTemplateDict['id'] = 5
        pdbTemplateDict['auth_atom_id'] = 5
        pdbTemplateDict['label_alt_id'] = 1
        pdbTemplateDict['auth_comp_id'] = 3
        pdbTemplateDict['auth_asym_id'] = 2
        pdbTemplateDict['auth_seq_id'] = 4
        pdbTemplateDict['pdbx_PDB_ins_code'] = 1
        pdbTemplateDict['Cartn_x'] = 11
        pdbTemplateDict['Cartn_y'] = 8
        pdbTemplateDict['Cartn_z'] = 8
        pdbTemplateDict['occupancy'] = 6
        pdbTemplateDict['B_iso_or_equiv'] = 6
        pdbTemplateDict['type_symbol'] = 2
        pdbTemplateDict['pdbx_formal_charge'] = 2

        for data_block_id in data_block_list:
            if '_atom_site' in sasCIFdict[data_block_id]:
                if '_sas_model' in sasCIFdict[data_block_id]:
                    fit_id = sasCIFdict[data_block_id]['_sas_model']['fitting_id']
                    model_id = sasCIFdict[data_block_id]['_sas_model']['id']
                else:
                    fit_id = '1'
                    model_id = '1'
                pdbfile = open(sasCIFfile[0:-7] + '_FIT_' + fit_id + '_MODEL_' + model_id + '.pdb', 'w')
                for i in range(len(sasCIFdict[data_block_id]['_atom_site']['group_PDB'])):
                    pdbLine = ''
                    for category in pdbTemplateDict.keys():
                        pdbLen = pdbTemplateDict[category]
                        if sasCIFdict[data_block_id]['_atom_site'][category][i] == '.':
                            sasCIFdict[data_block_id]['_atom_site'][category][i] = ''
                        if category == 'group_PDB':
                            pdbCat = 'ATOM  '
                        else:
                            pdbCat = str(sasCIFdict[data_block_id]['_atom_site'][category][i]).rjust(pdbLen)
                        pdbLine += pdbCat
                    pdbLine += '\n'
                    pdbfile.write(pdbLine)

    def getValue(self, subfile, field, sasCIFdict, data_block_id, category, item):
        if category in sasCIFdict[data_block_id] and item in sasCIFdict[data_block_id][category]:
            if isinstance(sasCIFdict[data_block_id][category][item], list):
                for element in list(enumerate(sasCIFdict[data_block_id][category][item], start=1)):
                    subfile.write(
                        field + ' ' + str(element[0]) + ': ' + str(element[1]) + '\n')
            else:
                subfile.write(
                    field + ': ' + str(sasCIFdict[data_block_id][category][item]) + '\n')
        else:
            subfile.write(field + ': .\n')

    def getContributors(self, subfile, sasCIFdict, data_block_id):
        if '_pdbx_contact_author' in sasCIFdict[data_block_id] and \
                'name_first' in sasCIFdict[data_block_id]['_pdbx_contact_author'] and \
                'name_last' in sasCIFdict[data_block_id]['_pdbx_contact_author']:
            if isinstance(sasCIFdict[data_block_id]['_pdbx_contact_author']['name_first'], list):
                for first, last \
                    in zip(sasCIFdict[data_block_id]['_pdbx_contact_author']['name_first'],
                           sasCIFdict[data_block_id]['_pdbx_contact_author']['name_last']):
                    subfile.write(
                        "Contributor's name: " + str(first) + ' ' + str(last) + '\n')
            else:
                subfile.write("Contributor's name: "
                              + str(sasCIFdict[data_block_id]['_pdbx_contact_author']['name_first']) +
                              ' ' + str(sasCIFdict[data_block_id]['_pdbx_contact_author']['name_last']) + '\n')
        else:
            subfile.write("Contributor's name: .\n")

    def extractMetadata(self, sasCIFdict, sasCIFfile, data_block_id=''):
        
        sasCIFfile = os.path.split(sasCIFfile)[-1]
        
        if data_block_id:
            data_block_list = [data_block_id]
        else:
            # Use only MAIN datablock
            data_block_list = [x for x in sasCIFdict.keys() if 'MAIN' in x]

        subfile = open(sasCIFfile[0:-7] + '_submission' + '.txt', 'w')
        for data_block_id in data_block_list:
            self.getValue(subfile, 'Title', sasCIFdict, data_block_id, '_sas_scan', 'title')
            self.getValue(subfile, 'Sample', sasCIFdict, data_block_id, '_sas_sample', 'name')
            self.getContributors(subfile, sasCIFdict, data_block_id)
            self.getValue(subfile, 'Short description', sasCIFdict, data_block_id, '_sas_result', 'comments')
            self.getValue(subfile, 'PubMed ID', sasCIFdict, data_block_id, '_citation', 'pdbx_database_id_PubMed')
            self.getValue(subfile, 'Molecule short name', sasCIFdict, data_block_id, '_entity_name_com', 'name')
            self.getValue(subfile, 'Molecule long name', sasCIFdict, data_block_id, '_entity', 'pdbx_description')
            self.getValue(subfile, 'Type', sasCIFdict, data_block_id, '_entity', 'type')
            # self.getValue(subfile,'Fragment',sasCIFdict,data_block_id,'_pdbx_contact_author','name_first')
            self.getValue(subfile, 'FASTA sequence', sasCIFdict, data_block_id, '_entity_poly',
                          'pdbx_seq_one_letter_code')
            self.getValue(subfile, 'Organism', sasCIFdict, data_block_id, '_entity_src_gen', 'gene_src_common_name')
            self.getValue(subfile, 'UniProt ID', sasCIFdict, data_block_id, '_struct_ref', 'db_code')
            self.getValue(subfile, 'Oligomeric state', sasCIFdict, data_block_id, '_entity', 'pdbx_number_of_molecules')
            self.getValue(subfile, 'Monomer mol. weight', sasCIFdict, data_block_id, '_entity', 'formula_weight')
            self.getValue(subfile, 'Experiment date', sasCIFdict, data_block_id, '_sas_scan', 'measurement_date')
            # self.getValue(subfile,'Type of experiment',sasCIFdict,data_block_id,'_entity','pdbx_number_of_molecules')
            self.getValue(subfile, 'Beamline name', sasCIFdict, data_block_id, '_sas_beam', 'instrument_name')
            self.getValue(subfile, 'Beamline city', sasCIFdict, data_block_id, '_sas_beam', 'instrument_city')
            self.getValue(subfile, 'Beamline country', sasCIFdict, data_block_id, '_sas_beam', 'instrument_country')
            self.getValue(subfile, 'X-ray wavelength', sasCIFdict, data_block_id, '_sas_beam', 'radiation_wavelength')
            self.getValue(subfile, 'Number of frames', sasCIFdict, data_block_id, '_sas_scan', 'number_of_frames')
            self.getValue(subfile, 'Exposure time per frame', sasCIFdict, data_block_id, '_sas_scan', 'exposure_time')
            self.getValue(subfile, 'Detector', sasCIFdict, data_block_id, '_sas_detc', 'name')
            self.getValue(subfile, 'Cell temperature', sasCIFdict, data_block_id, '_sas_scan', 'cell_temperature')
            self.getValue(subfile, 'Storage temperature', sasCIFdict, data_block_id, '_sas_scan', 'storage_temperature')
            self.getValue(subfile, 'Sample-detector distance', sasCIFdict, data_block_id, '_sas_beam',
                          'dist_spec_to_detc')
            self.getValue(subfile, 'Type of curve', sasCIFdict, data_block_id, '_sas_result', 'type_of_curve')
            self.getValue(subfile, 'Concentration range', sasCIFdict, data_block_id, '_sas_sample',
                          'specimen_concentration')
            self.getValue(subfile, 'Buffer', sasCIFdict, data_block_id, '_sas_buffer', 'name')
            self.getValue(subfile, 'Buffer concentration', sasCIFdict, data_block_id, '_sas_buffer', 'concentration')
            self.getValue(subfile, 'Buffer composition', sasCIFdict, data_block_id, '_sas_buffer', 'composition')
            self.getValue(subfile, 'I(0) Guinier', sasCIFdict, data_block_id, '_sas_result', 'I0_from_Guinier')
            self.getValue(subfile, 'Rg Guinier', sasCIFdict, data_block_id, '_sas_result', 'Rg_from_Guinier')
            self.getValue(subfile, 'Molecular weight estimated from Guinier I(0)', sasCIFdict, data_block_id,
                          '_sas_result', 'MW_standard')
            self.getValue(subfile, 'Molecular weight estimated from Porod Volume', sasCIFdict, data_block_id,
                          '_sas_result', 'MW_Porod')
            self.getValue(subfile, 'I(0) p(r)', sasCIFdict, data_block_id, '_sas_result', 'I0_from_PR')
            self.getValue(subfile, 'Rg p(r)', sasCIFdict, data_block_id, '_sas_result', 'Rg_from_PR')
            self.getValue(subfile, 'Dmax', sasCIFdict, data_block_id, '_sas_result', 'D_max')
            self.getValue(subfile, 'Porod volume', sasCIFdict, data_block_id, '_sas_result', 'Porod_volume')

    def extractAll(self, sasCIFdict, sasCIFfile):
        print 'Processing ' + sasCIFfile
        self.extractDat(sasCIFdict, sasCIFfile)
        self.extractFit(sasCIFdict, sasCIFfile)
        self.extractOut(sasCIFdict, sasCIFfile)
        self.extractAtoms(sasCIFdict, sasCIFfile)
        self.extractMetadata(sasCIFdict, sasCIFfile)
