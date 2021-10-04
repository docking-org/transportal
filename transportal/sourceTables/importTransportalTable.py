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
newSubstrates = sys.argv[2]
newInhibitors = sys.argv[3]
newDDI = sys.argv[4]
outputfilename = sys.argv[5]
additionalRefsFile = sys.argv[6]

infile = open(originalData)
data = json.load(infile)

transporters = set()
references = set()
referencesNonPubmed= {}
chemicals = set()
organismTransTable = {'Mus musculus': 'mouse',
        'Chlorocebus aethiops': 'grivet',
        'Rattus norvegicus': 'rat'}
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
inhibitorsEnd = 0
numInhibitors = 0
numSubstrates = 0
substratesEnd = 0
numDDI = 0
ddiEnd = 0
prevSubstrates = {}
prevInhibitors = {}
prevDDI = set()
for index in range(len(data)):
    x = data[index]
    if x['model'] == 'transporterDatabase.transporter':
        transporters.add(x['pk'])
        transportersEnd = index
    elif x['model'] == 'transporterDatabase.reference':
        if x['pk'].startswith('NA'):
            temp = x['pk']
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
        if not x['fields']['trans'] in prevInhibitors:
            prevInhibitors[x['fields']['trans']] = set()
        prevInhibitors[x['fields']['trans']].add(x['fields']['reference'])
    elif x['model'] == 'transporterDatabase.substrate':
        substratesEnd = index
        numSubstrates += 1
        if not x['fields']['trans'] in prevSubstrates:
            prevSubstrates[x['fields']['trans']] = set()
        prevSubstrates[x['fields']['trans']].add(x['fields']['reference'])
    elif x['model'] == 'transporterDatabase.ddi':
        ddiEnd = index
        numDDI += 1
        for ref in x['fields']['reference']:
            prevDDI.add(ref)

if inhibitorsEnd == 0:
    inhibitorsEnd = index
    
if substratesEnd == 0:
    substratesEnd = index
    
if ddiEnd == 0:
    ddiEnd = index

additionalRefsInfo = {}
infile = open(additionalRefsFile)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    if line['PUBMEDID'] != '':
        additionalRefsInfo[line['PUBMEDID']] = line
    else:
        additionalRefsInfo[line['OtherLink']] = line

infile = open(newSubstrates)
reader = csv.DictReader(infile,delimiter = '\t')

for line in reader:
    line = reader.next()
    if line['References'] != '' and (not line['References'] in references):
        refID = line['References']
        author = additionalRefsInfo[refID]['Author']
        year = additionalRefsInfo[refID]['Author']
        otherText = ''
        data.insert(referencesEnd+1,{u'pk': refID, u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': u'', u'otherText': otherText, u'year': year, u'authors': author}})
        references.add(refID)      
        referencesEnd += 1
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    if not slugify(line['Substrate']) in chemicals:
        temp = line['Substrate']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    km = line['Km (uM)']
    ref = line['References']
    system = line['Cell System']
    substrate = slugify(line['Substrate'])
    trans = line['Transporter']
    #    if ref in prevSubstrates[trans]:
    #        print 'Warning, potential repeat substrate:', trans, ref, substrate, km
    data.insert(substratesEnd+1,{u'pk': numSubstrates+1, u'model': u'transporterDatabase.substrate', u'fields': {u'trans': trans, u'cmpnd': substrate, u'km': km, u'reference': ref, u'cellSystem': system, u'cmpndClinical': 'false'}})
    numSubstrates += 1
    substratesEnd += 1
    inhibitorsEnd += 1
    ddiEnd += 1

infile = open(newInhibitors)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    if line['References'] == '' and (not line['OtherLink'] in referencesNonPubmed):
        otherLink = line['OtherLink']
        otherText = additionalRefsInfo[otherLink]['OtherText']
        numReferencesNonPubmed += 1
        data.insert(referencesEnd+1,{u'pk': 'NA'+str(numReferencesNonPubmed), u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': otherLink, u'otherText': otherText, u'year': u'', u'authors': u''}})
        referencesNonPubmed[otherLink] = 'NA'+str(numReferencesNonPubmed)
        referencesEnd += 1
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    elif not line['References'] in references:
        refID = line['References']
        author = additionalRefsInfo[refID]['Author']
        year = additionalRefsInfo[refID]['Author']
        otherText = ''
        data.insert(referencesEnd+1,{u'pk': refID, u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': u'', u'otherText': otherText, u'year': year, u'authors': author}})
        references.add(refID)      
        referencesEnd += 1
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    if not slugify(line['Substrate used']) in chemicals:
        temp = line['Substrate used']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    if not slugify(line['Inhibitor']) in chemicals:
        temp = line['Inhibitor']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    substrate = slugify(line['Substrate used'])
    ic50 = line['IC50 (uM)']
    ki = line['KI (uM)']
    if line['References'] != '':
        ref = line['References']
    else:
        ref = referencesNonPubmed[line['OtherLink']]
    system = line['Cell system']
    inhib = slugify(line['Inhibitor'])
    trans = line['Transporter']
#    if ref in prevInhibitors[trans]:
#        print 'Warning, potential repeat inhibitor:', trans, ref, inhib, substrate, ic50, ki
    data.insert(inhibitorsEnd+1,{u'pk': numInhibitors+1, u'model': u'transporterDatabase.inhibitor', u'fields': {u'trans': trans, u'cmpnd': inhib, u'ic50': ic50, u'ki': ki, u'reference': ref, u'cellSystem': system, u'substrate': substrate, u'substrateClinical': 'false', u'cmpndClinical': 'false'}})
    numInhibitors += 1
    inhibitorsEnd += 1
    ddiEnd += 1

infile = open(newDDI)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    if line['References'] == '':
        if (not line['OtherLink'] in referencesNonPubmed):
            otherLink = line['OtherLink']
            otherText = additionalRefsInfo[otherLink]['OtherText']
            numReferencesNonPubmed += 1
            data.insert(referencesEnd+1,{u'pk': 'NA'+str(numReferencesNonPubmed), u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': otherLink, u'otherText': otherText, u'year': u'', u'authors': u''}})
            referencesNonPubmed[otherLink] = 'NA'+str(numReferencesNonPubmed)
            referencesEnd += 1
            chemicalsEnd += 1
            inhibitorsEnd += 1
            substratesEnd += 1
            ddiEnd += 1
    elif not line['References'] in references:
        refID = line['References']
        author = additionalRefsInfo[refID]['Author']
        year = additionalRefsInfo[refID]['Author']
        otherText = ''
        data.insert(referencesEnd+1,{u'pk': refID, u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': u'', u'otherText': otherText, u'year': year, u'authors': author}})
        references.add(refID)      
        referencesEnd += 1
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    if not slugify(line['Interacting Drug']) in chemicals:
        temp = line['Interacting Drug']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    if not slugify(line['Affected Drug']) in chemicals:
        temp = line['Affected Drug']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        inhibitorsEnd += 1
        substratesEnd += 1
        ddiEnd += 1
    substrate = slugify(line['Affected Drug'])
    if line['References'] != '':
        ref = line['References']
    else:
        ref = referencesNonPubmed[line['OtherLink']]
    inhib = slugify(line['Interacting Drug'])
    trans = line['Transporter']
    impTrans = line['Implicated Transporter']
    auc = line['AUC']
    cmax = line['Cmax']
    clr = line['CLR']
    clf = line['CL/F']
    t12 = line['t1/2']
    pd = line['Effect on PD']
    intDose = line['Interacting Dose Information']
    affDose = line['Affected Dose Information']
    design = line['Study Design']
#    if ref in prevDDI:
#        print 'Warning, potential repeat ddi:', trans, ref, inhib, substrate
    data.insert(ddiEnd+1,{u'pk': numDDI+1, u'model': u'transporterDatabase.ddi', u'fields': {u'affectedDrugDose': affDose, u'transName': impTrans, u'reference': [ref], u'interactingDrugDose': intDose, u'transporters': trans.split(';'), u'AUC': auc, u'affectedDrug':[substrate], u'interactingDrug': [inhib], u'PDEffect': pd, u't1Over2': t12, u'CLOverF': clf, u'studyDesign': design, u'Cmax': cmax, u'CLr': clr}})
    numDDI += 1
    ddiEnd += 1

outfile= open(outputfilename, 'w')
json.dump(data, outfile, indent=1)
