#import re
#import pynini

class Paradigm:
	"""
		Given a list of words, scan to determine if a yer is present. If
		so, make the paradigm a pair of Feature objects to compare.
	"""
	def __init__(self, wrd: str, forms) -> None:
		"""
		Compare the lemma form against all inflected forms to determine
		if there is a yer. If so, create Features.
		"""
		self.lemma = wrd
		self.forms = {}
		for x in forms:
			self.forms[x[0]] = x[1]
		#if is_yer(A, B):
		#	#Check has_yer, how to negate value.
		#	has_yer, prefix = find_prefix(A, B)
		#	self.lemma = Features(A, prefix, has_yer, True)
		#	self.inf = Features(B, prefix, not has_yer)

	def __repr__(self):
		return True
		
	def __str__(self):
		s = self.lemma +":"
		for x in self.forms.keys():
			s += "\t" + x +"//" + self.forms[x]
		s += "\n"
		return s 
		
	def is_yer(lem, inf) -> bool:
		"""
		Take two forms to compare place-by-place to determine if a yet.
		Must except suffixes. 
		"""
		return True 
		
	def find_prefix(lem: str, inf: str) -> (bool, str):
		"""
		Given two strings, find the longest common prefix to mark where the yer occurs.
		"""
	
		#return triple of whether A is yer-bearing and the prefix
		#if A is not yer-bearing, 
		return True

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
