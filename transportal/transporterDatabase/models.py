from django.db import models

class Transporter(models.Model):
	symbol = models.CharField(max_length=10, primary_key=True)
	synonyms = models.CharField(max_length=100, verbose_name="limited list of synonyms")
	synonymsFull = models.CharField(max_length=100, verbose_name="all synonyms from NCBI database")
	ncbiID = models.CharField(max_length=10, null=True)
	species = models.CharField(max_length=20, null=True)
	def __unicode__(self):
		return self.symbol

class Organ(models.Model):
	name = models.CharField(max_length=30, primary_key=True)
	important = models.ManyToManyField(Transporter, verbose_name="transporters expressed highly in the tissue")
	def __unicode__(self):
		return self.name

class Reference(models.Model):
	authors = models.TextField(blank=True, null=True)
	year = models.CharField(max_length=4, blank=True, null=True)
	pmid = models.CharField(max_length=10, primary_key=True)
	otherText = models.CharField(max_length=200, blank=True, null=True, verbose_name="description for resource not in pubmed")
	otherLink = models.CharField(max_length=100, blank=True, null=True, verbose_name="http link to resource not in pubmed")
	def __unicode__(self):
		if self.pmid.is_int():
			return self.authors + '.' + self.year + '.PMID' + self.pmid
		else:
			return self.otherText

class Expression(models.Model):
	trans = models.ForeignKey(Transporter)
	organ = models.ForeignKey(Organ)
	experiment = models.CharField(max_length=50)
	value = models.FloatField(verbose_name="expression level")
	reference = models.ForeignKey(Reference, blank=True, null=True)
	def __unicode__(self):
		return ','.join([self.experiment, str(self.organ), str(self.trans), str(self.value)])

class Sample(models.Model):
	GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
	STATUS_CHOICES = (('N', 'Never Used'),('C', 'Current Use'),('P', 'Previous Use'),('O', 'Occasional Use'))
	age = models.IntegerField(null=True, blank=True)
	tissueSpec = models.CharField(max_length=50, blank=True)
	sex = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	ethnicity = models.CharField(max_length=20, blank=True)
	height = models.IntegerField(null=True, blank=True) #in cm
	weight = models.IntegerField(null=True, blank=True) #in kg
	bmi = models.IntegerField(null=True, blank=True)
	menopausalStatus = models.CharField(max_length=50, blank=True)
	numPregnancies = models.IntegerField(null=True, blank=True)
	numLiveBirths = models.IntegerField(null=True, blank=True)
	smokingStat = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True)
	cigarettesPerDay = models.IntegerField(null=True, blank=True)
	alcoholStatus = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True)
	clinicalDiagnosisSpecimen = models.CharField(max_length=100, blank=True, null=True)
	clinicalDiagnosisPatient = models.TextField(blank=True, null=True)
	medications = models.TextField(blank=True, null=True)
	recoveryType = models.CharField(max_length=100, blank=True, null=True)
	causeOfDeath = models.CharField(max_length=100, blank=True, null=True)
	organ = models.ForeignKey(Organ) 
	experiment = models.CharField(max_length=50)
	def __unicode__(self):
		return str(self.pk)

class Compound(models.Model):
	slugName = models.CharField(max_length=100, primary_key=True)
	name = models.CharField(max_length=100)
	clinicalUse = models.NullBooleanField()
	def __unicode__(self):
		return self.name

class Substrate(models.Model):
	trans = models.ForeignKey(Transporter)
	cmpnd = models.ForeignKey(Compound)
	cmpndClinical = models.BooleanField(verbose_name="can the substrate be used in clinical test")
	cellSystem = models.CharField(max_length=100, blank=True, null=True)
	km = models.CharField(max_length=10, blank=True, null=True)
	reference = models.ForeignKey(Reference, blank=True, null=True)
	def __unicode__(self):
		return ','.join([str(self.trans), str(self.cmpnd), self.cellSystem, str(self.km), str(self.reference)])

class Inhibitor(models.Model):
	trans = models.ForeignKey(Transporter)
	cmpnd = models.ForeignKey(Compound)
	cmpndClinical = models.BooleanField(verbose_name="can the inhibitor be used in clinical tests")
	cellSystem = models.CharField(max_length=100, blank=True, null=True)
	ic50 = models.CharField(max_length=10, blank=True, null=True)
	ki = models.CharField(max_length=10, blank=True, null=True)
	substrate = models.ForeignKey(Compound, blank=True, related_name='inhib_substrate', null=True)
	substrateClinical = models.BooleanField(verbose_name="can the substrate be used in clincial tests")
	reference = models.ForeignKey(Reference, blank=True, null=True)
	def __unicode__(self):
		return ','.join([str(self.trans), str(self.cmpnd), str(self.substrate), self.cellSystem, str(self.ic50), str(self.ki), str(self.reference)])

class DDI(models.Model):
	transName = models.CharField(max_length=10)
	transporters = models.ManyToManyField(Transporter)
	interactingDrug = models.ManyToManyField(Compound, related_name='interact_drug')
	interactingDrugDose = models.CharField(max_length=100, blank=True)
	affectedDrug = models.ManyToManyField(Compound, related_name='affect_drug', blank=True)
	affectedDrugDose = models.CharField(max_length=100, blank=True)
	studyDesign = models.CharField(max_length=50, blank=True, null=True)
	AUC = models.CharField(max_length=10, blank=True, null=True)
	Cmax = models.CharField(max_length=10, blank=True, null=True)
	CLr = models.CharField(max_length=10, blank=True, null=True)
	CLOverF = models.CharField(max_length=10, blank=True, null=True)
	t1Over2 = models.CharField(max_length=10, blank=True, null=True)
	PDEffect = models.CharField(max_length=5)
	reference = models.ManyToManyField(Reference, blank=True, null=True)
	def __unicode__(self):
		return 'pk=' + self.pk + ','.join([str(self.transName)])

class InVitroInhibitor(models.Model):
	trans = models.ForeignKey(Transporter)
	interactingChemical = models.ForeignKey(Compound, related_name='interact_chem')
	affectedSubstrate = models.ForeignKey(Compound, related_name='affect_sub')
	system = models.TextField(null=True)
	ic50 = models.CharField(max_length=10, blank=True, null=True)
	ki = models.CharField(max_length=10, blank=True, null=True)
	assayType = models.CharField(max_length=30, blank=True, default='')
	reference = models.ForeignKey(Reference, blank=True, null=True)
	def __unicode__(self):
		return 'pk=' + self.pk + ','.join([str(self.transName),self.get_type_display(),self.get_subtype_display()])

class InVitroSubstrate(models.Model):
	trans = models.ForeignKey(Transporter)
	substrate = models.ForeignKey(Compound)
	system = models.TextField(null=True)
	km = models.CharField(max_length=10, blank=True, null=True)
	assayType = models.CharField(max_length=30, blank=True, default='')
	reference = models.ForeignKey(Reference, blank=True, null=True)
	def __unicode__(self):
		return 'pk=' + self.pk + ','.join([str(self.transName),str(self.system)])


