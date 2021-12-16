#import re
#import pynini

class Paradigm:
	"""
		For forms that already have been determined to have yers, store the lemma and prefix, 
		whether the yer is in the lemma, and if not, store a dictionary of yer-bearing inflected
		forms and their inflectional info.
	"""
	
	def __init__(self, lemma: str, prefix: list) -> None:
		"""
		Compare the lemma form against all inflected forms to determine
		if there is a yer. If so, create Features.

		forms:		(dict) Morphological info : full form
		is_yer:		(bool) is this a form with a yer or not??
		lemma: 		(string) lemma of the paradigm
		lem_yer:	(bool) If true, lemma has the yer; if false, yer only present in inflection
		prefix:		(string) prefix before the yer
		"""
		self.lemma = lemma
		self.prefix = prefix
		self.global_yer = False
		
		self.forms = {}
		

	def __repr__(self):
		return True
		
	def __str__(self):
		s = self.lemma +":\n"
		for x in self.forms.keys():
			s += "\t" + x +" --> " + str(self.forms[x]) + "\n"
		#s += "\n"
		return s 

	def f(self, i):
		if (self.forms).get(i):
			return self.forms[i]
		else:
			return False
	
	def form_keys(self):
		x = self.forms 
		return x.keys()
		
	def lem(self):
		return self.lemma 
		
	def lem_yer(self):
		"""
		Returns True if the yer is found in the lemma, False if only found in inflected forms.

		Main should be updated so that if a Paradigm item exists and the yer is in the lemma, saves the inflectional information of info that FAILS the vowel check. 
		"""
		return self.lem_yer

	def ind_yer(self, inf):
		"""
		For a specific form, returns the tuple of inflected form and yer presence (bool).
		"""
		return self.forms[inf]
		
	def pre(self):
		return self.prefix
		
	def update(self, lem: list, inf: str, has_yer: bool):
		self.forms[inf] = (lem, has_yer)
		
	def update_all_yers(self) -> None:
		self.global_yer = True