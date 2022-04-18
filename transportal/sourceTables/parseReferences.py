from lxml import etree
import unicodedata
import csv

outfile = open('additionalTransportalRefs.txt','w')
outfile.write('PUBMEDID\tAuthor\tYear\tOtherLink\tOtherText\n')
tree = etree.parse('pubmedReferenceSummary.xml')
root = tree.getroot()
for child in root:
	id = child[0].text
	year = child[1].text.split()[0]
	author = unicode(child[4][0].text.split()[0])
	author = unicodedata.normalize('NFKD',author).encode('ascii','ignore')
	outfile.write('\t'.join([id,author,year,'',''])+'\n')

infile =open('nonPubmedReference.txt')
reader = csv.DictReader(infile,delimiter='\t')
for line in reader:
	outfile.write('\t'.join(['','','',line['OtherLink'],line['OtherText']])+'\n')
outfile.close()
