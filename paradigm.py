#import re
#import pynini

class Paradigm:
	"""
		For forms that already have been determined to have yers, store the lemma and prefix, 
		whether the yer is in the lemma, and if not, store a dictionary of yer-bearing inflected
		forms and their inflectional info.
	"""
	def __init__(self, prefix: str lemma: str, lem_yer: bool) -> None:
		"""
		Compare the lemma form against all inflected forms to determine
		if there is a yer. If so, create Features.

		forms:		(dict) Morphological info : full form
		lemma: 		(string) lemma of the paradigm
		lem_yer:	(bool) If true, lemma has the yer; if false, yer only present in inflection
		prefix:		(string) prefix before the yer
		"""
		self.lemma = wrd
		self.lem_yer = lem_yer
		self.prefix = prefix
		
		self.forms = {}
		

	def __repr__(self):
		return True
		
	def __str__(self):
		s = self.lemma +":"
		for x in self.forms.keys():
			s += "\t" + x +"//" + self.forms[x]
		s += "\n"
		return s 
		
	def update(lem: str, inf: str):
		self.forms[lem] = inf

class Features:
	"""
		Given a word, make note of the 
		feature map, including phonological features, inflectional 
		information, and syllable information.
	"""
	def __init__(self, wrd: str, prefix: str, yer:bool, lemma=False) -> None:
		"""
		Given the word, its prefix (to mark where in the word the yer 
		occurs), log morphophonological features.
		"""
		
		#Morphology
		self.gender = wrd["gender"]
		self.case = wrd["case"]
		
		#Syllables
		self.syllable = count_syl(prefix)
		
		#Phonology
		
		return True

	def __repr__(self):
		return True
		
	def __str__(self):
		return True
		
	def count_syl(prefix: str) -> int:
		"""
		Counts the vowel/consonant alternations to determine number of syllables in prefix.
		"""
		return True
