##Import in vitro interactions tsv to initial_data.json
##python importTicBaseInVitro.py origFile newDataFile outputFile additionalTransInfoFile


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
additionalTransFile = sys.argv[4]

infile = open(originalData)
data = json.load(infile)

transporters = set()
references = set()
referencesNonPubmed= {}
chemicals = set()
organismTransTable = {'Mus musculus': 'mouse',
        'Chlorocebus aethiops': 'grivet',
        'Rattus norvegicus': 'rat'}

transportersEnd = 0
referencesEnd = 0
numReferencesNonPubmed = 0
chemicalsEnd = 0
inhibitorsEnd = 0
numInhibitors = 0
numSubstrates = 0
substratesEnd = 0
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
    elif x['model'] == 'transporterDatabase.inhibitor':
        inhibitorsEnd = index
        numInhibitors += 1
    elif x['model'] == 'transporterDatabase.substrate':
        substratesEnd = index
        numSubstrates += 1

if inhibitorsEnd == 0:
    inhibitorsEnd = index
if substratesEnd == 0:
    substratesEnd = index

additionalTransInfo = {}
infile = open(additionalTransFile)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    additionalTransInfo[line['pk']] = line

infile = open(newData)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    if line['Organism (protein source)'] == 'Homo Sapiens':
        transporterName = line['Transporter Protein']
    else:
        transporterName = organismTransTable[line['Organism (protein source)']]+'_'+line['Transporter Protein']
    if not transporterName in transporters:
        trans = transporterName
        if trans in additionalTransInfo:
            syns = additionalTransInfo[trans]['synonyms']
            synsFull = additionalTransInfo[trans]['synonymFull']
            species = additionalTransInfo[trans]['species']
            ncbiid = additionalTransInfo[trans]['ncbiID']
            humanTransporter = additionalTransInfo[transporterName]['humanTransporter']
        else:
            syns = u''
            synsFull = u''
            species = u''
            ncbiid = u''
            humanTransporter = u''
        data.insert(transportersEnd+1,{u'pk': trans, u'model': u'transporterDatabase.transporter', u'fields': {u'synonymsFull': synsFull, u'synonyms': syns, u'species': species, u'ncbiID': ncbiid, u'humanTransporter': humanTransporter}})
        transporters.add(trans)
        transportersEnd += 1
        referencesEnd += 1
        chemicalsEnd += 1
        substratesEnd += 1
        inhibitorsEnd += 1
    if (not line['Pubmed ID'] in references) and (not line['Pubmed ID'] in referencesNonPubmed):
        temp = line['Reference'].split(", ")
        author = temp[0]
        year = temp[1]
        otherText = ''
        data.insert(referencesEnd+1,{u'pk': line['Pubmed ID'], u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': u'', u'otherText': otherText, u'year': year, u'authors': author}})
        references.add(line['Pubmed ID'])      
        referencesEnd += 1
        chemicalsEnd += 1
        substratesEnd += 1
        inhibitorsEnd += 1
    if not slugify(line['Chemical']) in chemicals:
        temp = line['Chemical']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        substratesEnd += 1
        inhibitorsEnd += 1
    temp = line['Reporter']
    if temp.startswith('[3H]'):
        temp = temp[4:].strip()
    if temp.startswith('[14C]'):
        temp = temp[5:].strip()
    if '(prestimulation)' in temp:
        temp = temp.split()[0]
    if not slugify(temp) in chemicals:
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        substratesEnd += 1
        inhibitorsEnd += 1
    if line['Substrate'] == 'Substrate':
        km = line['Km (uM)']
        ref = line['Pubmed ID']
        system = line['In vitro system']
        substrate = slugify(line['Chemical'])
        trans = transporterName
        data.insert(substratesEnd+1,{u'pk': numSubstrates+1, u'model': u'transporterDatabase.substrate', u'fields': {u'trans': trans, u'cmpnd': substrate, u'km': km, u'reference': ref, u'cellSystem': system, u'cmpndClinical': False}})
        numSubstrates += 1
        substratesEnd += 1
        inhibitorsEnd += 1
    elif line['Inhibitor'] == 'Inhibitor':
        affectChem = line['Reporter']
        if affectChem.startswith('[3H]'):
            affectChem = affectChem[4:].strip()
        if affectChem.startswith('[14C]'):
            affectChem = affectChem[5:].strip()
        if '(prestimulation)' in affectChem:
            affectChem = affectChem.split()[0]
        affectChem = slugify(affectChem)
        ic50 = line['IC50 (uM)']
        ec50 = line['EC50 (uM)']
        ki = line['Ki (uM)']
        if ic50 != '':
            inhibVal = ic50
        else:
            inhibVal = ec50
        ref = line['Pubmed ID']
        if not ref.isdigit():
            ref = referencesNonPubmed[ref]
        system = line['In vitro system']
        interactChem = slugify(line['Chemical'])
        trans = transporterName
        data.insert(inhibitorsEnd+1,{u'pk': numInhibitors+1, u'model': u'transporterDatabase.inhibitor', u'fields': {u'trans': trans, u'cmpnd': interactChem, u'ic50': inhibVal, u'ki': ki, u'reference': ref, u'cellSystem': system, u'substrate': affectChem, u'cmpndClinical': False, u'substrateClinical': False}})
        numInhibitors += 1
        inhibitorsEnd += 1
        
    

outfile= open(outputfilename, 'w')
json.dump(data, outfile, indent=1)
