import string, statistics, re
from django.shortcuts import render_to_response
from transportal.transporterDatabase.models import Transporter, Organ, Expression, Sample, Substrate, Inhibitor, DDI, Compound
from django.db.models import Q

def naturallysortedexpressionlist(L, reverse=False):
        convert = lambda text: ('', int(text)) if text.isdigit() else (text, 0)
        alphanum = lambda key: [ convert(c) for c in re.split('([0-9]+)', key.trans.symbol) ]
        return sorted(L, key=alphanum, reverse=reverse) 

def naturallysortedtransporterlist(L, reverse=False):
        convert = lambda text: ('', int(text)) if text.isdigit() else (text, 0)
        alphanum = lambda key: [ convert(c) for c in re.split('([0-9]+)', key.symbol) ]
        return sorted(L, key=alphanum, reverse=reverse) 

def quartiles(numericValues,quartile):
        theValues = sorted(numericValues)
        if (quartile*len(theValues)) % 4 == 0:
                lower = theValues[len(theValues)*quartile/4-1]
                upper = theValues[len(theValues)*quartile/4]
                return (float(lower + upper)) / 2  
        else:
                return theValues[(len(theValues)*quartile+1)/4-1]

def transporter(request, transporter_id):
        expressLevelsNishi = Expression.objects.filter(trans=transporter_id, experiment='Nishimura').order_by('organ')
        expressLevelsPMT = Expression.objects.filter(trans=transporter_id, experiment__startswith='PMT Sample').order_by('organ')
        substrates = Substrate.objects.filter(trans=transporter_id).order_by('cmpnd')
        inhibitors = Inhibitor.objects.filter(trans=transporter_id).order_by('cmpnd', 'substrate') 
        ddi = DDI.objects.filter(transporters__symbol=transporter_id)
#Build DDI table
        ddiInfo = {}
        for x in ddi:
                temp = str(x.pk)
                build = [x]
                build.append(Compound.objects.filter(interact_drug__pk=x.pk))
                build.append(Compound.objects.filter(affect_drug__pk=x.pk))
                ddiInfo[temp] = build
        ddiInfo = list(ddiInfo.values())
        ddiInfo.sort(key=lambda x: [x[1][0].slugName,x[2][0].slugName])
#Build expression level table
        transporter = Transporter.objects.get(pk=transporter_id)
        otherTrans = Transporter.objects.filter(humanTransporter=transporter_id).exclude(symbol=transporter_id)
        important = transporter.organ_set.all()
        importantNames = []
        for x in important:
                importantNames.append(str(x.name))
        pmt = {}
#For PMT data, calculate averages across all samples
        for x in expressLevelsPMT:
                temp = str(x.organ)
                if not temp in pmt:
                        pmt[temp] = [0,0.0]
                pmt[temp][0] += 1
                pmt[temp][1] += x.value
        for x in pmt.keys():
                pmt[x] = pmt[x][1]/pmt[x][0]
        buildExp = []
        if len(expressLevelsNishi) >0:
                for x in range(len(expressLevelsNishi)):
                        buildExp.append([expressLevelsNishi[x].organ, expressLevelsNishi[x].experiment, expressLevelsNishi[x].value, expressLevelsNishi[x].reference])
                temp = list(pmt.keys())
                temp.sort()
                for x in temp:
                        buildExp.append([x, 'Mean across all PMT Samples', pmt[x], expressLevelsPMT[0].reference])
        elif len(expressLevelsPMT) > 0:
                temp = list(pmt.keys())
                temp.sort(key=str)
                for x in temp:
                        buildExp.append([x, 'Mean across all PMT Samples', pmt[x], expressLevelsPMT[0].reference])
        cmpndList = {}
        cmpndSet = set()
        for x in ddi:
                temp = Compound.objects.filter(Q(interact_drug__pk=x.pk) | Q(affect_drug__pk=x.pk))
                for cmpnd in temp:
                        cmpndSet.add(cmpnd.slugName)
        for x in substrates:
                cmpndSet.add(x.cmpnd.slugName)
        for x in inhibitors:
                cmpndSet.add(x.cmpnd.slugName)
                cmpndSet.add(x.substrate.slugName)
        for cmpnd in transporter.inVitroSubstrate.all():
                cmpnd1 = cmpnd.slugName
                if not cmpnd1 in cmpndList:
                        cmpndList[cmpnd1] = ''
                cmpndList[cmpnd1] += '1'
        for cmpnd in transporter.inVitroInhibitor.all():
                cmpnd1 = cmpnd.slugName
                if not cmpnd1 in cmpndList:
                        cmpndList[cmpnd1] = ''
                cmpndList[cmpnd1] += '2'
        for cmpnd in transporter.clinicalSubstrate.all():
                cmpnd1 = cmpnd.slugName
                if not cmpnd1 in cmpndList:
                        cmpndList[cmpnd1] = ''
                cmpndList[cmpnd1] += '3'
        for cmpnd in transporter.clinicalInhibitor.all():
                cmpnd1 = cmpnd.slugName
                if not cmpnd1 in cmpndList:
                        cmpndList[cmpnd1] = ''
                cmpndList[cmpnd1] += '4'
        return render_to_response('transporter.html', {'expression': buildExp, 'transporter':transporter, 'important': importantNames, 'substrates': substrates, 'inhibitors':inhibitors, 'ddi':ddiInfo, 'otherTrans':otherTrans, 'fdaCmpnds':cmpndList})

def liver(request):
        expressLevelsNishi = naturallysortedexpressionlist(Expression.objects.filter(organ='Liver', experiment='Nishimura'))
        expressLevelsPMT = naturallysortedexpressionlist(Expression.objects.filter(organ='Liver', experiment__startswith='PMT Sample'))
        expressBiotroveTransporters = naturallysortedtransporterlist(Transporter.objects.filter(expression__organ='Liver',expression__experiment__startswith='PMT Biotrove').distinct())
        important = Transporter.objects.filter(organ__name='Liver')
        importantNames = []
        for x in important:
                importantNames.append(str(x.symbol))
        synquery = Transporter.objects.all()
        syns = {}
        for x in synquery:
                syns[x.symbol] = x.synonyms
#Calculate mean expression across all PMT samples
        pmtTableValues = []
        for x in range(len(expressLevelsPMT)/3):
                build = []
                for y in range(3):
                        build.append(expressLevelsPMT[x*3+y].value)
                avg = mean(build)
                stdev = stdev(build)
                id = expressLevelsPMT[x*3].trans
                pmtTableValues.append([id] + build + [avg, stdev])
#Calculate median and quartiles across biotrove samples
        biotroveTableValues = []
        for x in expressBiotroveTransporters:
                values = Expression.objects.filter(organ='Liver', experiment__startswith='PMT Biotrove', trans=x).values_list('value',flat='True').order_by('value')
                build = []
                build.append(x.symbol)
                build.append(quartiles(values,1))
                build.append(quartiles(values,2))
                build.append(quartiles(values,3))
                biotroveTableValues.append(build)
        return render_to_response('liver.html', {'expressionNishi': expressLevelsNishi, 'expressionPMT': pmtTableValues, 'organ': 'Liver', 'syns': syns, 'important': importantNames, 'expressionBiotrove': biotroveTableValues})

def kidney(request):
        expressLevelsNishi = naturallysortedexpressionlist(Expression.objects.filter(organ='Kidney', experiment='Nishimura'))
        expressLevelsPMT = naturallysortedexpressionlist(Expression.objects.filter(organ='Kidney', experiment__startswith='PMT Sample'))
        expressBiotroveTransporters = naturallysortedtransporterlist(Transporter.objects.filter(expression__organ='Kidney',expression__experiment__startswith='PMT Biotrove').distinct())
        important = Transporter.objects.filter(organ__name='Kidney')
        importantNames = []
        for x in important:
                importantNames.append(str(x.symbol))
        synquery = Transporter.objects.all()
        syns = {}
        for x in synquery:
                syns[x.symbol] = x.synonyms
#Calculate mean expression across all PMT samples
        pmtTableValues = []
        for x in range(len(expressLevelsPMT)/4):
                build = []
                for y in range(4):
                        build.append(expressLevelsPMT[x*4+y].value)
                avg = mean(build)
                stdev = stdev(build)
                id = expressLevelsPMT[x*4].trans
                pmtTableValues.append([id] + build + [avg, stdev])
#Calculate median and quartiles across biotrove samples
        biotroveTableValues = []
        for x in expressBiotroveTransporters:
                values = Expression.objects.filter(organ='Kidney', experiment__startswith='PMT Biotrove', trans=x).values_list('value',flat='True').order_by('value')
                build = []
                build.append(x.symbol)
                build.append(quartiles(values,1))
                build.append(quartiles(values,2))
                build.append(quartiles(values,3))
                biotroveTableValues.append(build)
        return render_to_response('kidney.html', {'expressionNishi': expressLevelsNishi, 'expressionPMT': pmtTableValues, 'organ': 'Kidney', 'syns': syns, 'important': importantNames, 'expressionBiotrove': biotroveTableValues})

def organ(request, organ_id):
        temp = string.capwords(' '.join(organ_id.split('-')))
        expressLevels = naturallysortedexpressionlist(Expression.objects.filter(organ=temp))
        important = Transporter.objects.filter(organ__name=temp)
        importantNames = []
        for x in important:
                importantNames.append(str(x.symbol))
        synquery = Transporter.objects.all()
        syns = {}
        for x in synquery:
                syns[x.symbol] = x.synonyms
        return render_to_response(organ_id + '.html', {'expression': expressLevels, 'organ': temp, 'syns': syns, 'important': importantNames})

def index(request):
        transporters = naturallysortedtransporterlist(Transporter.objects.all())
        organs = Organ.objects.all().order_by('name')
        compounds = Compound.objects.all().order_by('name')
        alph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        return render_to_response('dataIndex.html', {'transporters': transporters, 'organs': organs, 'compounds': compounds, 'alph':alph})

def home(request):
        return render_to_response('start.html')

def about(request):
        return render_to_response('about.html')

def contact(request):
        return render_to_response('contact.html')

def links(request):
        return render_to_response('links.html')

def glossary(request):
        return render_to_response('glossary.html')

def sitemap(request):
        return render_to_response('sitemap.xml')

def sample(request, organ_id):
        temp = string.capwords(' '.join(organ_id.split('-')))
        samples = Sample.objects.filter(organ__name=temp)
        dataTable = []
        numEntries = 18
        numSamples = len(samples)
        if numSamples == 0:
                return render_to_response('samples.html', {'organ': organ_id, 'samples':dataTable})
        build = ['Category']
        for x in range(numSamples):
                build.append('Donor ' + str(x + 1))
        dataTable.append(build)
        build = ['Tissue Specification']
        for x in range(numSamples):
                build.append(samples[x].tissueSpec)
        dataTable.append(build)        
        build = ['Age at Excision']
        for x in range(numSamples):
                build.append(samples[x].age)
        dataTable.append(build)
        build = ['Sex']
        for x in range(numSamples):
                build.append(samples[x].sex)
        dataTable.append(build)
        build = ['Ethnicity']
        for x in range(numSamples):
                build.append(samples[x].ethnicity)
        dataTable.append(build)
        build = ['Height (cm)']
        for x in range(numSamples):
                build.append(samples[x].height)
        dataTable.append(build)
        build = ['Weight (kg)']
        for x in range(numSamples):
                build.append(samples[x].weight)
        dataTable.append(build)
        build = ['BMI']
        for x in range(numSamples):
                build.append(samples[x].bmi)
        dataTable.append(build)
        build = ['Menopausal Status']
        for x in range(numSamples):
                build.append(samples[x].menopausalStatus)
        dataTable.append(build)
        build = ['Number of Pregnancies']
        for x in range(numSamples):
                build.append(samples[x].numPregnancies)
        dataTable.append(build)
        build = ['Number Live Births']
        for x in range(numSamples):
                build.append(samples[x].numLiveBirths)
        dataTable.append(build)
        build = ['Smoking Status']
        for x in range(numSamples):
                build.append(samples[x].smokingStat)
        dataTable.append(build)
        build = ['Cigarettes/Day']
        for x in range(numSamples):
                build.append(samples[x].cigarettesPerDay)
        dataTable.append(build)
        build = ['Alcohol Status']
        for x in range(numSamples):
                build.append(samples[x].alcoholStatus)
        dataTable.append(build)
        build = ['Clinical Diagnosis (Specimen)']
        for x in range(numSamples):
                build.append(samples[x].clinicalDiagnosisSpecimen)
        dataTable.append(build)
        build = ['Clinical Diagnosis (Patient)']
        for x in range(numSamples):
                build.append(samples[x].clinicalDiagnosisPatient)
        dataTable.append(build)
        build = ['Medications']
        for x in range(numSamples):
                build.append(samples[x].medications)
        dataTable.append(build)
        build = ['Recovery Type']
        for x in range(numSamples):
                build.append(samples[x].recoveryType)
        dataTable.append(build)
        build = ['Cause of Death']
        for x in range(numSamples):
                build.append(samples[x].causeOfDeath)
        dataTable.append(build)
        return render_to_response('samples.html', {'organ': organ_id, 'samples':dataTable})

def sampleT(request, organ_id, transporter_id):
        temp = string.capwords(' '.join(organ_id.split('-')))
        samples = Sample.objects.filter(organ__name=temp)
        dataTable = [] 
        numEntries = 18
        numSamples = len(samples)
        if numSamples == 0:
                return render_to_response('samples.html', {'organ': organ_id, 'samples':dataTable})
        build = ['Category']
        for x in range(numSamples):
                build.append('Donor ' + str(x + 1))
        dataTable.append(build) 
        build = ['Tissue Specification']
        for x in range(numSamples):
                build.append(samples[x].tissueSpec)
        dataTable.append(build)
        build = ['Age at Excision']
        for x in range(numSamples):
                build.append(samples[x].age)
        dataTable.append(build)
        build = ['Sex']
        for x in range(numSamples):
                build.append(samples[x].sex)
        dataTable.append(build)
        build = ['Ethnicity']
        for x in range(numSamples):
                build.append(samples[x].ethnicity)
        dataTable.append(build)
        build = ['Height (cm)']
        for x in range(numSamples):
                build.append(samples[x].height)
        dataTable.append(build)
        build = ['Weight (kg)']
        for x in range(numSamples):
                build.append(samples[x].weight)
        dataTable.append(build)
        build = ['BMI']
        for x in range(numSamples):
                build.append(samples[x].bmi)
        dataTable.append(build)
        build = ['Menopausal Status']
        for x in range(numSamples):
                build.append(samples[x].menopausalStatus)
        dataTable.append(build)
        build = ['Number of Pregnancies']
        for x in range(numSamples):
                build.append(samples[x].numPregnancies)
        dataTable.append(build)
        build = ['Number Live Births']
        for x in range(numSamples):
                build.append(samples[x].numLiveBirths)
        dataTable.append(build)
        build = ['Smoking Status']
        for x in range(numSamples):
                build.append(samples[x].smokingStat)
        dataTable.append(build)
        build = ['Cigarettes/Day']
        for x in range(numSamples):
                build.append(samples[x].cigarettesPerDay)
        dataTable.append(build)
        build = ['Alcohol Status']
        for x in range(numSamples):
                build.append(samples[x].alcoholStatus)
        dataTable.append(build)
        build = ['Clinical Diagnosis (Specimen)']
        for x in range(numSamples):
                build.append(samples[x].clinicalDiagnosisSpecimen)
        dataTable.append(build)
        build = ['Clinical Diagnosis (Patient)']
        for x in range(numSamples):
                build.append(samples[x].clinicalDiagnosisPatient)
        dataTable.append(build)
        build = ['Medications']
        for x in range(numSamples):
                build.append(samples[x].medications)
        dataTable.append(build)
        build = ['Recovery Type']
        for x in range(numSamples):
                build.append(samples[x].recoveryType)
        dataTable.append(build)
        build = ['Cause of Death']
        for x in range(numSamples):
                build.append(samples[x].causeOfDeath)
        dataTable.append(build)
        return render_to_response('samples.html', {'organ': organ_id, 'samples':dataTable, 'transporter': transporter_id})

def compound(request, compound_id):
        substrates = Substrate.objects.filter(cmpnd=compound_id).order_by('cmpnd')
        inhibitors = Inhibitor.objects.filter(cmpnd=compound_id).order_by('cmpnd', 'substrate')
        ddi = DDI.objects.filter(Q(interactingDrug=compound_id)|Q(affectedDrug=compound_id)).order_by('interactingDrug', 'affectedDrug')
        ddiInfo = {}
        for x in ddi:
                temp = x.pk
                build = [x]
                build.append(Compound.objects.filter(interact_drug__pk=x.pk))
                build.append(Compound.objects.filter(affect_drug__pk=x.pk))
                ddiInfo[x.pk] = build
        ddiInfo = list(ddiInfo.values())
        ddiInfo.sort(key=lambda x: [x[1][0].slugName,x[2][0].slugName])
        compound = Compound.objects.get(slugName=compound_id)
        return render_to_response('compound.html', {'compound': compound, 'substrates': substrates, 'inhibitors':inhibitors, 'ddi':ddiInfo})

def ddi(request, ddi_id):
        ddi = DDI.objects.get(pk=int(ddi_id))
        interDrug = Compound.objects.filter(interact_drug__pk=ddi.pk)
        affectDrug = Compound.objects.filter(affect_drug__pk=ddi.pk)
        return render_to_response('moreDDIInfo.html', {'ddi': ddi, 'interDrug': interDrug, 'affectDrug': affectDrug})

def search(request):
        keywords = request.GET['keyword']
        keywords = keywords.split()
        build = Q(name__icontains=keywords[0])
        for x in keywords[1:]:
                build = build|Q(name__icontains=x)
        organs = Organ.objects.filter(build).order_by('name')
        build = Q(symbol__icontains=keywords[0])|Q(synonyms__icontains=keywords[0])|Q(synonymsFull__icontains=keywords[0])
        for x in keywords[1:]:
                build = build|Q(symbol__icontains=x)|Q(synonyms__icontains=x)|Q(synonymsFull__icontains=x)
        trans = Transporter.objects.filter(build).order_by('symbol')
        build = Q(name__icontains=keywords[0])|Q(slugName__icontains=keywords[0])
        for x in keywords[1:]:
                build = build|Q(name__icontains=x)|Q(slugName__icontains=x)
        comps = Compound.objects.filter(build).order_by('name')
        return render_to_response('search.html', {'organs':organs, 'trans':trans, 'comps':comps})

def testticbase(request, transporter_id):
        inVitroInhibitor = InVitroInhibitor.objects.filter(trans=transporter_id).order_by('interactingChemical','affectedSubstrate')
        inVitroSubstrate = InVitroSubstrate.objects.filter(trans=transporter_id).order_by('substrate')
        transporter = Transporter.objects.get(pk=transporter_id)
        otherTrans = Transporter.objects.filter(humanTransporter=transporter_id).exclude(symbol=transporter_id)
        return render_to_response('testticbase.html', {'transporter':transporter, 'inVitroInhibitor':inVitroInhibitor, 'inVitroSubstrate':inVitroSubstrate,'otherTrans':otherTrans})

def testticbase1(request, transporter_id):
        inVitroInhibitor = InVitroInhibitor.objects.filter(trans__humanTransporter=transporter_id).order_by('interactingChemical','affectedSubstrate')
        inVitroSubstrate = InVitroSubstrate.objects.filter(trans__humanTransporter=transporter_id).order_by('substrate')
        transporter = Transporter.objects.get(pk=transporter_id)
        return render_to_response('testticbase1.html', {'transporter':transporter, 'inVitroInhibitor':inVitroInhibitor, 'inVitroSubstrate':inVitroSubstrate})

def testticbase2(request, transporter_id):
        inVitroInhibitor = InVitroInhibitor.objects.filter(trans=transporter_id).order_by('interactingChemical','affectedSubstrate')
        inVitroSubstrate = InVitroSubstrate.objects.filter(trans=transporter_id).order_by('substrate')
        transporter = Transporter.objects.get(pk=transporter_id)
        mouseInhibitor = InVitroInhibitor.objects.filter(trans__species='Mus musculus').filter(trans__humanTransporter=transporter_id).order_by('interactingChemical','affectedSubstrate')
        mouseSubstrate = InVitroSubstrate.objects.filter(trans__species='Mus musculus').filter(trans__humanTransporter=transporter_id).order_by('substrate')
        mouseTrans = Transporter.objects.filter(species='Mus musculus').filter(humanTransporter=transporter_id)
        if mouseTrans:
                mouseTrans = mouseTrans.get()
        ratInhibitor = InVitroInhibitor.objects.filter(trans__species='Rattus norvegicus').filter(trans__humanTransporter=transporter_id).order_by('interactingChemical','affectedSubstrate')
        ratSubstrate = InVitroSubstrate.objects.filter(trans__species='Rattus norvegicus').filter(trans__humanTransporter=transporter_id).order_by('substrate')
        ratTrans = Transporter.objects.filter(species='Rattus norvegicus').filter(humanTransporter=transporter_id)
        if ratTrans:
                ratTrans = ratTrans.get()
        grivetInhibitor = InVitroInhibitor.objects.filter(trans__species='Chlorocebus aethiops').filter(trans__humanTransporter=transporter_id).order_by('interactingChemical','affectedSubstrate')
        grivetSubstrate = InVitroSubstrate.objects.filter(trans__species='Chlorocebus aethiops').filter(trans__humanTransporter=transporter_id).order_by('substrate')
        grivetTrans = Transporter.objects.filter(species='Chlorocebus aethiops').filter(humanTransporter=transporter_id)
        if grivetTrans:
                grivetTrans = grivetTrans.get()
        return render_to_response('testticbase2.html', {'transporter':transporter, 'inVitroInhibitor':inVitroInhibitor, 'inVitroSubstrate':inVitroSubstrate,'mouseInhibitor':mouseInhibitor, 'mouseSubstrate':mouseSubstrate, 'ratInhibitor':ratInhibitor, 'ratSubstrate':ratSubstrate, 'grivetInhibitor':grivetInhibitor, 'grivetSubstrate':grivetSubstrate, 'mouseTrans':mouseTrans, 'ratTrans':ratTrans, 'grivetTrans':grivetTrans})
