from django import template

register = template.Library()
def showSigFigs(d, args):
	args = args.split(',')
	sigFigsLeft = int(args[0])
	numFrontDigits = int(args[1])
	front = ''
	for x in range(numFrontDigits-1,0,-1 ):
		if int(d)/(10**x) > 0:
			break
		front = front+'&nbsp;'
	if int(d)/1 == 0:
		temp = d
		while True:
			temp = 10 * temp
			if int(temp)/1 > 0:
				break
			sigFigsLeft += 1
	if sigFigsLeft < 0:
		sigFigsLeft = 0
	return front + '{0:.{1}f}'.format(d,sigFigsLeft) 
register.filter('showSigFigs', showSigFigs)
def showSigFigs1(d, args):
	args = args.split(',')
	sigFigsLeft = int(args[0])
	numFrontDigits = int(args[1])
	front = ''
	for x in range(numFrontDigits-1,0,-1 ):
		if int(d)/(10**x) > 0:
			sigFigsLeft = sigFigsLeft - x - 1
			break
		front = front+'&nbsp;'
	if int(d)/1 > 0 and int(d)/10 == 0:
		sigFigsLeft = sigFigsLeft - 1
	if int(d)/1 == 0:
		temp = d
		while True:
			temp = 10 * temp
			if int(temp)/1 > 0:
				break   
			sigFigsLeft += 1
	if sigFigsLeft < 0:
		sigFigsLeft = 0
	return front + '{0:.{1}f}'.format(d,sigFigsLeft)
register.filter('showSigFigs1', showSigFigs1)
