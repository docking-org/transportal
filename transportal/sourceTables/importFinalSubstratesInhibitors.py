##Import in vitro interactions tsv to initial_data.json
##python importTicBaseInVitro.py origFile newDataFile outputFile additionalTransInfoFile

errorTracking = open('missingEntries.txt','w')
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
outputfilename = sys.argv[4]
missingFlag = False

infile = open(originalData)
data = json.load(infile)

transporters = set()
references = set()
referencesNonPubmed= set()
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
            referencesNonPubmed.add(x['pk'])
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

infile = open(newSubstrates)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    transporterName = line['Transporter']
    if not transporterName in transporters:
        print "Unidentified Transporter", transporterName
        missingFlag = True
        continue
#        trans = transporterName
#        if trans in additionalTransInfo:
#            syns = additionalTransInfo[trans]['synonyms']
#            synsFull = additionalTransInfo[trans]['synonymFull']
#            species = additionalTransInfo[trans]['species']
#            ncbiid = additionalTransInfo[trans]['ncbiID']
#            humanTransporter = additionalTransInfo[transporterName]['humanTransporter']
#        else:
#            syns = u''
#            synsFull = u''
#            species = u''
#            ncbiid = u''
#            humanTransporter = u''
#        data.insert(transportersEnd+1,{u'pk': trans, u'model': u'transporterDatabase.transporter', u'fields': {u'synonymsFull': synsFull, u'synonyms': syns, u'species': species, u'ncbiID': ncbiid, u'humanTransporter': humanTransporter, u"inVitroSubstrate": [], u"inVitroInhibitor": [], u"clinicalSubstrate": [], u"clinicalInhibitor": []}})
#        transporters.add(trans)
#        transportersEnd += 1
#        referencesEnd += 1
#        chemicalsEnd += 1
#        substratesEnd += 1
#        inhibitorsEnd += 1
    if (not line['Reference'] in references) and (not line['Reference'] in referencesNonPubmed):
        print "Unidentified Publication", line['Reference']
        missingFlag = True
        continue
#        temp = line['Reference'].split(", ")
#        author = temp[0]
#        year = temp[1]
#        otherText = ''
#        data.insert(referencesEnd+1,{u'pk': line['Pubmed ID'], u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': u'', u'otherText': otherText, u'year': year, u'authors': author}})
#        references.add(line['Pubmed ID'])      
#        referencesEnd += 1
#        chemicalsEnd += 1
#        substratesEnd += 1
#        inhibitorsEnd += 1
    temp = line['Substrate']
    if temp.startswith('[3H]'):
        temp = temp[4:].strip()
    if temp.startswith('[14C]'):
        temp = temp[5:].strip()
    if not slugify(temp) in chemicals:
        print "Unidentified Substrate Chemical", slugify(temp)
        missingFlag = True
        continue
#        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
#        chemicals.add(slugify(temp))
#        chemicalsEnd += 1
#        substratesEnd += 1
#        inhibitorsEnd += 1
    km = line['Km']
    ref = line['Reference']
    system = line['CellSystem']
    substrate = slugify(line['Substrate'])
    trans = transporterName
    data.insert(substratesEnd+1,{u'pk': numSubstrates+1, u'model': u'transporterDatabase.substrate', u'fields': {u'trans': trans, u'cmpnd': substrate, u'km': km, u'reference': ref, u'cellSystem': system}})
    numSubstrates += 1
    substratesEnd += 1
    inhibitorsEnd += 1

infile = open(newInhibitors)
reader = csv.DictReader(infile,delimiter = '\t')
for line in reader:
    transporterName = line['Transporter']
    if not transporterName in transporters:
        print "Unidentified Transporter", transporterName
        missingFlag = True
        continue
#        trans = transporterName
#        if trans in additionalTransInfo:
#            syns = additionalTransInfo[trans]['synonyms']
#            synsFull = additionalTransInfo[trans]['synonymFull']
#            species = additionalTransInfo[trans]['species']
#            ncbiid = additionalTransInfo[trans]['ncbiID']
#            humanTransporter = additionalTransInfo[transporterName]['humanTransporter']
#        else:
#            syns = u''
#            synsFull = u''
#            species = u''
#            ncbiid = u''
#            humanTransporter = u''
#        data.insert(transportersEnd+1,{u'pk': trans, u'model': u'transporterDatabase.transporter', u'fields': {u'synonymsFull': synsFull, u'synonyms': syns, u'species': species, u'ncbiID': ncbiid, u'humanTransporter': humanTransporter, u"inVitroSubstrate": [], u"inVitroInhibitor": [], u"clinicalSubstrate": [], u"clinicalInhibitor": []}})
#        transporters.add(trans)
#        transportersEnd += 1
#        referencesEnd += 1
#        chemicalsEnd += 1
#        substratesEnd += 1
#        inhibitorsEnd += 1
    if (not line['Reference'] in references) and (not line['Reference'] in referencesNonPubmed):
        print "Unidentified Publication", line['Reference']
        missingFlag = True
        continue
#        temp = line['Reference'].split(", ")
#        author = temp[0]
#        year = temp[1]
#        otherText = ''
#        data.insert(referencesEnd+1,{u'pk': line['Pubmed ID'], u'model': u'transporterDatabase.reference', u'fields': {u'otherLink': u'', u'otherText': otherText, u'year': year, u'authors': author}})
#        references.add(line['Pubmed ID'])      
#        referencesEnd += 1
#        chemicalsEnd += 1
#        substratesEnd += 1
#        inhibitorsEnd += 1
    if not slugify(line['Inhibitor']) in chemicals:
        print "Unidentified Inhibitor Chemical", line['Inhibitor'], slugify(line['Inhibitor'])
        errorTracking.write("Unidentified Inhibitor Chemical\t"+line['Inhibitor']+'\t'+slugify(line['Inhibitor'])+'\n')
        missingFlag = True
        temp = line['Inhibitor']
        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp.capitalize()}})
        chemicals.add(slugify(temp))
        chemicalsEnd += 1
        substratesEnd += 1
        inhibitorsEnd += 1
    temp = line['Substrate']
    if temp.startswith('[3H]'):
        temp = temp[4:].strip()
    if temp.startswith('[14C]'):
        temp = temp[5:].strip()
    if not slugify(temp) in chemicals:
        print "Unidentified Substrate Chemical", temp, slugify(temp)
        errorTracking.write("Unidentified Substrate Chemical\t"+temp+'\t'+slugify(temp)+'\n')
        missingFlag = True
        continue
#        data.insert(chemicalsEnd+1,{u'pk': slugify(temp), u'model': u'transporterDatabase.compound', u'fields': {u'name': temp}})
#        chemicals.add(slugify(temp))
#        chemicalsEnd += 1
#        substratesEnd += 1
#        inhibitorsEnd += 1
    affectChem = line['Substrate']
    if affectChem.startswith('[3H]'):
        affectChem = affectChem[4:].strip()
    if affectChem.startswith('[14C]'):
        affectChem = affectChem[5:].strip()
    affectChem = slugify(affectChem)
    ic50 = line['IC50']
    ki = line['Ki']
    ref = line['Reference']
    system = line['CellSystem']
    interactChem = slugify(line['Inhibitor'])
    trans = transporterName
    data.insert(inhibitorsEnd+1,{u'pk': numInhibitors+1, u'model': u'transporterDatabase.inhibitor', u'fields': {u'trans': trans, u'cmpnd': interactChem, u'ic50': ic50, u'ki': ki, u'reference': ref, u'cellSystem': system, u'substrate': affectChem}})
    numInhibitors += 1
    inhibitorsEnd += 1

outfile= open(outputfilename, 'w')
json.dump(data, outfile, indent=1)
