## Adjust initial data to add on species field to transporters


import json
import sys

originalData = sys.argv[1]
outputfilename = sys.argv[2]

infile = open(originalData)
data = json.load(infile)

for index in range(len(data)):
    x = data[index]
    if x['model'] == 'transporterDatabase.transporter':
        data[index]['fields']['species'] = 'Homo sapiens'

outfile= open(outputfilename, 'w')
json.dump(data, outfile, indent = 1)
