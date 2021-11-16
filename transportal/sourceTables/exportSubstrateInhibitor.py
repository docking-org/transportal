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
outputsubstratefilename = sys.argv[2]
outputinhibitorfilename = sys.argv[3]

infile = open(originalData)
data = json.load(infile)

transporters = set()
references = set()
referencesNonPubmed= {}
chemicals = set()
outfileSub = open(outputsubstratefilename, 'w')
outfileSub.write('Transporter\tSubstrate\tKm\tCellSystem\tReference\n')
outfileInhib = open(outputinhibitorfilename, 'w')
outfileInhib.write('Transporter\tInhibitor\tKi\tIC50\tCellSystem\tSubstrate\tReference\n')


for index in range(len(data)):
    x = data[index]
    if x['model'] == 'transporterDatabase.inhibitor':
        temp = x['fields']
        if temp['ki']:
            ki = temp['ki']
        else:
            ki = ''
        if temp['ic50']:
            ic50 = temp['ic50']
        else:
            ic50 = ''
        build = [temp['trans'],temp['cmpnd'],ki,ic50,temp['cellSystem'],temp['substrate'],temp['reference']]
        outfileInhib.write('\t'.join(build)+'\n')
    elif x['model'] == 'transporterDatabase.substrate':
        temp = x['fields']
        build = [temp['trans'],temp['cmpnd'],temp['km'],temp['cellSystem'],temp['reference']]
        outfileSub.write('\t'.join(build)+'\n')
