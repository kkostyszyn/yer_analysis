"""
First, create a script that has the shape of the paradigm as a class - logging morpho info, phono info, number of syllables before yer, etc.

Then, run statistical analyses on all paradigms to find significant features. 
"""
import re
import sys
from paradigm import Paradigm, Features
from translate_pol import Translate

def test_print(data):
    """
    Purely for testing purposes.
    """
    temp = 0
    for i in data:
        if temp % 5 == 0:
            print(i, data[i], end="\n\n")
    temp += 1

def save_as_text(save, data):
	"""
	Shortcut to write data to a file for later analysis.
	"""
	f = open(save, "w", encoding="utf8")
		
	if isinstance(data, dict):
		for x in data.keys():
			f.write(x+":")
			for text in data[x]:
				f.write("\t" + str(text))
				f.write("\n")
	else: 
		pass		
	f.close()

def root_without_final_vowels(txt: str) -> str:
	"""
	For any root, cut off any and all final vowels.
	"""
	vowels = ['a', 'i', 'u', 'e', 'o', 'y', 'ą', 'ę', 'ó', 'ɔ', 'ɛ', 'ɨ'] 
	
	#so long as the final character is a vowel, continue removing 
	while txt[-1] in vowels:
		txt = txt[:-1]
	return txt 
	
def domain(lst):
	"""
	Shortcut for range(len()), so I don't forget to remove the final position :)
	"""
	return (range(len(lst) - 1))
	
def vowel(ch) -> bool:
	"""
	Determines if a character is a vowel or not.
	"""
	vowels = ["a", "i", "ɔ", "u", "ɛ", "ɨ", "ɔ̃", "ɛ̃"]
	 
	if ch in vowels:
		return True
	return False 

def prefix(str, pos):
	"""
	Shortcut to return a substring, sliced up to an excluding a certain position.
	"""
	return str[:pos]

def strip_text(txt):
	"""
	Takes a line in the following format, from the 'SAVE.txt' list of bundles:
		(['a', 'a', 'l', 'ɛ', 'n', 'ɛ', 'm'], 'N;INS;SG')
		
	Re-format as a tuple of ([list of chars], 'inflection')
	"""
	
	txt = re.sub(r"[()\[']", "", txt) 
	txt = txt.split("]")
	
	txt[0] = re.sub("\t", "", txt[0])
	txt[0] = txt[0].split(', ')
	
	txt[1] = re.sub("\n", "", txt[1])
	
	return txt
	
def main(load = False):
	"""
	Based on previous Pynini script, do POL-->IPA transcription.
	Turn into function, so that it can be incorporated into MAIN code - when an N is found in the tagset, append the transcribed form, using lemma as key.

	Wikipron is being used to simplify the process, but only accounts for a fraction of the noted forms. 
	"""
	#the Translate class is a large transducer that carries out the translation from Polish to IPA 
	tr = Translate()
	
	if not load: #if i'm rebuilding the 'bundle' list 

		wp = open("data/pol_latn_broad.tsv", "r", encoding="utf8")
		wp = wp.readlines()

		pron_dict = {}

		for line in wp:
			temp = re.split(r"\t", line)
			pron_dict[temp[0]] = re.split(r"\n", temp[1])[0] #Remove trailing \n from wikipron document
		"""
		Open Polish morphological data compiled by Unimorph. 
			
		Then, for all inflected forms, compare to the lemma to find inserted/deleted vowels - sign of yer. 
			
		See if there is a way to generalize across resulting patterns.
		"""
		f = open("data/pol.txt", encoding="utf8")
		f = f.readlines()

		bundles = {}
		leftover = []
			
		for x in f:
			temp = re.split(r"\s+", x)
			tags = re.split(r";", temp[2])
			if tags[0] == 'N' and temp[0].lower() == temp[0]: #remove proper nouns - Zydow, Amerikanami
				if temp[0] not in bundles.keys():
					bundles[temp[0]] = []
				#Change this line when building for Paradigm object - revert to tuples
				#temp[1] is the inflected form, temp[2] is the inflectional information
				
				try:
					bundles[temp[0]].append(((tr.t(temp[1])).split(), temp[2]))
				except:
					#Strings that contain 'q' or punctuation (hyphenation, apostrophes, etc.) will be rejected by the transducer. 
					print(temp[1])
				#Original code for testing Transducer against WikiPron standard
				"""
				if temp[1] in pron_dict.keys():
					try:
						test = tr.t(temp[1])
						if test != pron_dict[temp[1]]:
							print(temp[1], "\n\t" + pron_dict[temp[1]], "\n\t"+ test)
					except:
						print("Failed: ", temp[1])
					bundles[temp[0]].append((pron_dict[temp[1]], temp[2]))
				else:
					try:	
						bundles[temp[0]].append((tr.t(temp[1]), temp[2]))
					except:
						pass
				"""		
		#Using this saved text, generate a new bundles dictionary 
		save_as_text("data/SAVE.txt", bundles)
	else: #if i'm using the saved bundle list 
		bun = open("data/SAVE.txt", "r")
		bun = bun.readlines()
		
		bundles = {}
		temp = ''
	
		for line in bun:
			line = line.split(":")
			if len(line) > 1:
				temp = line[0]
			bundles[temp] = strip_text(line[-1])
	
	#testing Paradigm data structure
	"""
	for x in bundles.keys():
		print(Paradigm(x, bundles[x]))
	"""

	#These are exceptional forms, with significantly different forms (czlowiek~ludzi, tydzien~tygodniu).
	#In the future, have the user upload a list of exceptions to pop from the bundles.
	try:
		bundles.pop('tydzień')
		bundles.pop('człowiek')
		
	yer_found = {}

	#For every item in the bundles dictionary, compare the 'lemma' (minus final vowels) to each root and find yer environment 
	for root in bundles.keys():
		try:
			temp = root_without_final_vowels(tr.t(root).split())
			for pair in bundles[root]:
				#First - decide how to treat unimorph vs wikipron data 
				if not isinstance(pair, str):
					for ch_pos in domain(temp):
						if vowel(temp[ch_pos]) != vowel(pair[ch_pos]):
							#print(ch_pos, temp , "\t", pair)
							#if, for any consonant in one form, the corresponding character in the other form is a vowel (or vice versa) - log this as the prefix, marking a yer.
							#ONLY look in the 'root'
							if vowel(temp[ch_pos]):
								pre = prefix(temp, ch_pos)
							else: 	
								pre = prefix(pair[0], ch_pos)
							yer_found[root] = pre 
								#find prefix 
		except:
			print(root)
						
	save_as_text("data/lemmas.txt", yer_found)

################################
if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()