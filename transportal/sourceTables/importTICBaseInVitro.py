##Import in vitro interactions tsv to initial_data.json


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
additionalReferenceFile = sys.argv[5]

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
        'rOAT1':'rat_Slc22a6',
        'rOAT2':'rat_Slc22a7',
        'rOAT3':'rat_Slc22a8',
        'rMATE1':'rat_Slc47a1',
        'OATP1a1':'rat_Slco1a1',
        'BCRP1':'mouse_Abcg2',
        'OATP1A4':'mouse_Slco1a4',
        'MRP1-4':'',
        'P-gp like':''}

transportersEnd = 0
referencesEnd = 0
numReferencesNonPubmed = 0
chemicalsEnd = 0
inVitroInhibitorsEnd = 0
numInVitroInhibitors = 0
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
    elif x['model'] == 'transporterDatabase.invitroinhibitor':
        inVitroInhibitorsEnd = index
        numInVitroInhibitors += 1
    elif x['model'] == 'transporterDatabase.invitrosubstrate':
        inVitroSubstratesEnd = index
        numInVitroSubstrates += 1

if inVitroInhibitorsEnd == 0:
    inVitroInhibitorsEnd = index
if inVitroSubstratesEnd == 0:
    inVitroSubstratesEnd = index

additionalTransInfo = {}
infile = open(additionalTransFile)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    additionalTransInfo[line['pk']] = line

additionalRefsInfo = {}
infile = open(additionalReferenceFile)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    additionalRefsInfo[line['pubmed']] = line

infile = open(newData)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    if not line['Transporter Protein'] in transporters:
        trans = line['Transporter Protein']
        if trans in additionalTransInfo:
            syns = additionalTransInfo[trans]['synonyms']
            synsFull = additionalTransInfo[trans]['synonymFull']
            species = additionalTransInfo[trans]['species']
            ncbiid = additionalTransInfo[trans]['ncbiID']
        else:
            syns = u''
            synsFull = u''
            species = u''
            ncbiid = u''
        data.insert(transportersEnd+1,{u'pk': trans, u'model': u'transporterDatabase.transporter', u'fields': {u'synonymsFull': synsFull, u'synonyms': syns, u'species': species, u'ncbiID': ncbiid}})
        transporters.add(trans)
        transportersEnd += 1
        referencesEnd += 1
        chemicalsEnd += 1
        inVitroInhibitorsEnd += 1
        inVitroSubstratesEnd += 1
    if (not line['Pubmed ID'] in references) and (not line['Pubmed ID'] in referencesNonPubmed):
        temp = line['Pubmed ID']
        if temp in additionalRefsInfo:
            author = additionalRefsInfo[temp]['author']
            year = additionalRefsInfo[temp]['year']
            otherText = additionalRefsInfo[temp]['otherText']
        else:
            author = u''
            year = u''
            otherText = u''
        if temp.isdigit():
            data.insert(referencesEnd+1,{u'pk': temp, u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': u'', u'otherText': otherText, u'year': year, u'authors': author}})
            references.add(temp)
        else:
            numReferencesNonPubmed += 1
            data.insert(referencesEnd+1,{u'pk': 'NA'+str(numReferencesNonPubmed), u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': temp, u'otherText': otherText, u'year': year, u'authors': author}})
            referencesNonPubmed[temp] = 'NA'+str(numReferencesNonPubmed)        
        referencesEnd += 1
        chemicalsEnd += 1
        inVitroInhibitorsEnd += 1
        inVitroSubstratesEnd += 1
    if not slugify(line['Chemical']) in chemicals:
        temp = line['Chemical']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inVitroInhibitorsEnd += 1
        inVitroSubstratesEnd += 1
    temp = line['Reporter molecule']
    if temp.startswith('[3H]'):
        temp = temp[4:].strip()
    if not slugify(temp) in chemicals:
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inVitroInhibitorsEnd += 1
        inVitroSubstratesEnd += 1
    if line['Interaction Type'] == 'Inhibitor':
        affectChem = line['Reporter molecule']
        if affectChem.startswith('[3H]'):
            affectChem = affectChem[4:].strip()	
        ic50 = line['IC50 (uM)']
        ec50 = line['EC 50 (uM)']
        ki = line['Ki (uM)']
        if ic50 != '':
            inhibVal = ic50
        else:
            inhibVal = ec50
        ref = line['Pubmed ID']
        if not ref.isdigit():
            ref = referencesNonPubmed[ref]
        system = line['In Vitro System']
        interactChem = line['Chemical']
        trans = line['Transporter Protein']
        assayType = line['Assay type']
        data.insert(inVitroInhibitorsEnd+1,{u'pk': numInVitroInhibitors+1, u'model': u'transporterDatabase.invitroinhibitor', u'fields': {u'trans': trans, u'interactingChemical': slugify(interactChem), u'ic50': inhibVal, u'ki': ki, u'reference': ref, u'system': system, u'affectedSubstrate': slugify(affectChem), u'assayType': assayType}})
        numInVitroInhibitors += 1
        inVitroInhibitorsEnd += 1
        inVitroSubstratesEnd += 1
        
    elif line['Interaction Type'] == '' and line['Substrate / Nonsubstrate'] == 'Substrate':
        km = line['Km (uM)']
        ref = line['Pubmed ID']
        system = line['In Vitro System']
        substrate = line['Chemical']
        assayType = line['Assay type']
        trans = line['Transporter Protein']
        data.insert(inVitroSubstratesEnd+1,{u'pk': numInVitroSubstrates+1, u'model': u'transporterDatabase.invitrosubstrate', u'fields': {u'trans': trans, u'substrate': slugify(substrate), u'km': km, u'reference': ref, u'system': system, u'assayType': assayType}})
        numInVitroSubstrates += 1
        inVitroSubstratesEnd += 1

outfile= open(outputfilename, 'w')
json.dump(data, outfile, indent=1)
