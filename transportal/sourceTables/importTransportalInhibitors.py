##Import 
##python 

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
newInhibitors = sys.argv[2]
outputfilename = sys.argv[3]
additionalRefsFile = sys.argv[4]

infile = open(originalData)
data = json.load(infile)

transporters = set()
references = set()
referencesNonPubmed= {}
chemicals = set()

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
    if line['pubmed'] != '':
        additionalRefsInfo[line['pubmed']] = line
    else:
        additionalRefsInfo[line['OtherLink']] = line

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
        author = additionalRefsInfo[refID]['author']
        year = additionalRefsInfo[refID]['year']
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
    data.insert(inhibitorsEnd+1,{u'pk': numInhibitors+1, u'model': u'transporterDatabase.inhibitor', u'fields': {u'trans': trans, u'cmpnd': inhib, u'ic50': ic50, u'ki': ki, u'reference': ref, u'cellSystem': system, u'substrate': substrate}})
    numInhibitors += 1
    inhibitorsEnd += 1

outfile= open(outputfilename, 'w')
json.dump(data, outfile, indent=1)
