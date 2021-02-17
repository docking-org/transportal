##Import in vitro interaction tsv to initial_data.json


import json
import sys
import csv

non_url_safe = ['"', '#', '$', '%', '&', '+',
            ',', '/', ':', ';', '=', '?',
            '@', '[', '\\', ']', '^', '`',
            '{', '|', '}', '~', "'"]

def slugify(text):
    """
    Turn the text content of a header into a slug for use in an ID and capitalize the first letter
    """
    non_safe = [c for c in text if c in non_url_safe]
    if non_safe:
        for c in non_safe:
            text = text.replace(c, '')
    # Strip leading, trailing and multiple whitespace, convert remaining whitespace to _
    text = u'_'.join(text.split())
    return text.lower()


originalData = sys.argv[1]
newData = sys.argv[2]
outputfilename = sys.argv[3]

infile = open(originalData)
data = json.load(infile)

transporters = set()
references = set()
referencesNonPubmed= {}
chemicals = set()

transporterTransTable = {'P-gp':'ABCB1',
        'MRP1':'ABCC1',
        'MRP2':'ABCC2',
        'MRP4':'ABCC4',
        'BCRP':'ABCG2',
        'Oct1':'SLC22A1',
        'Oct2':'SLC22A2',
        'hOCT1':'SLC22A1',
        'OCT1':'SLC22A1',
        'hOCT2':'SLC22A2',
        'OCT2':'SLC22A2',
        'hOCT3':'SLC22A3',
        'hOAT1':'SLC22A6',
        'OAT1':'SLC22A6',
        'hOAT2':'SLC22A7',
        'hOAT3':'SLC22A8',
        'OAT3':'SLC22A8',
        'hOAT4':'SLC22A11',
        'URAT1':'SLC22A12',
        'hMATE1':'SLC47A1',
        'MATE1':'SLC47A1',
        'MATE2-K':'SLC47A2',
        'OATP1A2':'SLCO1A2',
        'OATP1B1':'SLCO1B1',
        'OATP1B3':'SLCO1B3',
        'OATP2B1':'SLCO2B1',
        'rOAT1':'rat Slc22a6',
        'rOAT2':'rat Slc22a7',
        'rOAT3':'rat Slc22a8',
        'rMATE1':'rat Slc47a1',
        'OATP1a1':'rat Slco1a1',
        'BCRP1':'mouse Abcg2',
        'OATP1A4':'mouse Slco1a4',
        'MRP1-4':'',
        'P-gp like':''}

transportersEnd = 0
referencesEnd = 0
numReferencesNonPubmed = 0
chemicalsEnd = 0
inVitroInteractionsEnd = 0
numInVitroInteractions = 0
numInVitroSubstrates = 0
inVitroSubstratesEnd = 0
for index in range(len(data)):
    x = data[index]
    if x['model'] == 'transporterDatabase.transporter':
        transporters.add(x['pk'])
        transportersEnd = index
    elif x['model'] == 'transporterDatabase.reference':
        if x['pk'].startswith('NA'):
            temp = x['pk'][2:]
            referencesNonPubmed[x['fields']['otherLink']] = temp
            numReferencesNonPubmed += 1
        else:
            references.add(x['pk'])
        referencesEnd = index
    elif x['model'] == 'transporterDatabase.compound':
        chemicals.add(x['pk'])
        chemicalsEnd = index
    elif x['model'] == 'transporterDatabase.invitrointeraction':
        inVitroInteractionsEnd = index
        numInVitroInteractions += 1
    elif x['model'] == 'transporterDatabase.invitrosubstrate':
        inVitroSubstratesEnd = index
        numInVitroSubstrates += 1

if inVitroInteractionsEnd == 0:
    inVitroInteractionsEnd = index
if inVitroSubstratesEnd == 0:
    inVitroSubstratesEnd = index

infile = open(newData)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    if line['Interaction Type'] not in['Substrate','Inhibitor']:
        continue
    if line['Substrate used/ATPase assay/Cell-viability assay'] == 'Cell-viability assay':
        continue
    line['Transporter'] = transporterTransTable[line['Transporter']]
    if line['Transporter'] == '':
        continue
    if not line['Transporter'] in transporters:
        data.insert(transportersEnd+1,{u'pk': line['Transporter'], u'model': u'transporterDatabase.transporter', u'fields': {u'synonymsFull': u'', u'synonyms': u'', u'species': u'', u'ncbiID': u''}})
        transporters.add(line['Transporter'])
        transportersEnd += 1
        referencesEnd += 1
        chemicalsEnd += 1
        inVitroInteractionsEnd += 1
        inVitroSubstratesEnd += 1
    if (not line['Reference (Pubmed ID)'] in references) and (not line['Reference (Pubmed ID)'] in referencesNonPubmed):
        temp = line['Reference (Pubmed ID)']
        if temp.isdigit():
            data.insert(referencesEnd+1,{u'pk': temp, u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': None, u'otherText': None, u'year': u'', u'authors': u''}})
            references.add(temp)
        else:
            numReferencesNonPubmed += 1
            data.insert(referencesEnd+1,{u'pk': 'NA'+str(numReferencesNonPubmed), u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': temp, u'otherText': None, u'year': None, u'authors': None}})
            referencesNonPubmed[temp] = 'NA'+str(numReferencesNonPubmed)        
        referencesEnd += 1
        chemicalsEnd += 1
        inVitroInteractionsEnd += 1
        inVitroSubstratesEnd += 1
    if not slugify(line['Chemical']) in chemicals:
        temp = line['Chemical']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inVitroInteractionsEnd += 1
        inVitroSubstratesEnd += 1
    temp = line['Substrate used/ATPase assay/Cell-viability assay']
    if temp != 'ATPase assay' and temp != 'ATPase assay/Calcein' and not slugify(temp) in chemicals:
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inVitroInteractionsEnd += 1
        inVitroSubstratesEnd += 1
    temp = line['ATPase stimulation']
    if temp != '':
        if temp == 'Not listed':
            temp = 'Not_listed'
        else:
            temp = temp.split()[-1]
        if not slugify(temp) in chemicals:
            data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
            chemicals.add(slugify(temp))
            chemicalsEnd += 1
            inVitroInteractionsEnd += 1
            inVitroSubstratesEnd += 1
    
    if line['Interaction Type'] == 'Inhibitor':
        temp = line['Substrate used/ATPase assay/Cell-viability assay']
        if temp== 'ATPase assay' or temp == 'ATPase assay/Calcein':
            expType = 'A'
            atpinfo = line['ATPase stimulation']
            if atpinfo == 'Not listed':
                stimConc = 'Not listed'
                affectChem = 'Not_listed'
            else:
                affectChem = slugify(atpinfo.split()[-1])
                stimConc = atpinfo.split()[0][:-2]
        else:
            expType = 'V'
            affectChem = slugify(line['Substrate used/ATPase assay/Cell-viability assay'])
            stimConc = None
        intConc = line['Chemical Concentration (uM)']            
        ic50 = line['IC50 (uM)']
        ec50 = line['EC 50 (uM)']
        km = line['Km (uM)']
        ref = line['Reference (Pubmed ID)']
        if not ref.isdigit():
            ref = referencesNonPubmed[ref]
        system = line['Cell/in vitro System']
        interactChem = slugify(line['Chemical'])
        trans = line['Transporter']
        data.insert(inVitroInteractionsEnd+1,{u'pk': numInVitroInteractions+1, u'model': u'transporterDatabase.invitrointeraction', u'fields': {u'interactingConcentration': intConc, u'stimConcentration': stimConc, u'ic50': ic50, u'ec50': ec50, u'km': km, u'reference': ref, u'system': system, u'affectedSubstrate': affectChem, u'subtype': u'P', u'interactingChemical': interactChem, u'trans': trans, u'type': expType}})
        numInVitroInteractions += 1
        inVitroInteractionsEnd += 1
        inVitroSubstratesEnd += 1
        
    elif line['Interaction Type'] == 'Substrate':
        temp = line['Substrate used/ATPase assay/Cell-viability assay']
        if temp== 'ATPase assay':
            atpinfo = line['ATPase stimulation']
            if atpinfo == 'Not listed':
                stimConc = 'Not listed'
                affectChem = 'Not_listed'
            else:
                affectChem = slugify(atpinfo.split()[-1])
                stimConc = atpinfo.split()[0][:-2]
        else:
            affectChem = slugify(line['Substrate used/ATPase assay/Cell-viability assay'])
            stimConc = None
        conc = line['Chemical Concentration (uM)']            
        ic50 = line['IC50 (uM)']
        km = line['Km (uM)']
        ref = line['Reference (Pubmed ID)']
        system = line['Cell/in vitro System']
        substrate = slugify(line['Chemical'])
        trans = line['Transporter']
        data.insert(inVitroSubstratesEnd+1,{u'pk': numInVitroSubstrates+1, u'model': u'transporterDatabase.invitrosubstrate', u'fields': {u'concentration': conc, u'ic50': ic50, u'km': km, u'reference': ref, u'system': system, u'substrate': interactChem, u'trans': trans,}})
        numInVitroSubstrates += 1
        inVitroSubstratesEnd += 1

outfile= open(outputfilename, 'w')
json.dump(data, outfile, indent=1)
