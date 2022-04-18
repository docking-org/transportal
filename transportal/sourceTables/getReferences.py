import urllib2

infile = open('referencesList.txt')
refs = []
for line in infile:
	refs.append(line.strip())
build = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id='
for ref in refs:
	build = build+ref+','
build = build[:-1]
file = urllib2.urlopen(build)
data = file.read()
file.close()
outfile = open('pubmedReferenceSummary.xml','w')
outfile.write(data)
outfile.close()
