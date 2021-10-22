"""
First, create a script that has the shape of the paradigm as a class - logging morpho info, phono info, number of syllables before yer, etc.

Then, run statistical analyses on all paradigms to find significant features. 
"""
import re
import sys
from paradigm import Paradigm, Features
from translate_pol import Translate

<<<<<<< HEAD
=======
def statistics(d):
	"""
	Takes the yer-found dictionary and uses the prefix to save the environment before and after for stats.
	"""
	env_before = {}
	env_after = {}
	count = 0
	for i in d.keys():
		#Remember that the items in d[i] are lists, not strings.
		count += 1
		
		#Find environment BEFORE yer 
		#change to using 'consonant_seq' function 
		b = consonant_seq_before(d[i])
		#print("before:", b)
		
		#Find environment AFTER yer 
		e = consonant_seq_after(d[i])
		#print("after:", e)
		
		#Add to env dictionaries 
		try:
			env_before[b] += 1
		except:
			env_before[b] = 1
			
		try:
			env_after[e] += 1
		except:
			env_after[e] = 1
			
	return (env_before, env_after, count)
	
def remove_items(d, suffix, after = False) -> dict:
	d_copy = {}
	for i in d:
		if after and suffix in i:
			#allow for consonants (but not vowels) to follow the suffix to be removed
			temp = i.split(suffix)
			to_pop = False 
			
			for letter in temp[-1]:
				if vowel(letter):
					to_pop = True
					
			if not to_pop:
				d_copy[i] = d[i]
		else:
			#suffix has to be at end of word 
			if (suffix not in i) or (suffix in i and i.endswith(suffix) and re.sub(suffix, r"", i) not in d.keys()):
				d_copy[i] = d[i]
		
	return d_copy

>>>>>>> Fixing statistics
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
			if isinstance(data[x], int):
				f.write(str(data[x]) + "\n")
			else:
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

def consonant_seq_before(txt) -> str:
	"""
	Given some string, finds all consonants at the end of the string (until interrupted by vowel).
	Assumes that the string is the prefix for a yer.
	"""
	if len(txt) == 1:
		if vowel(txt):
			return ""
		return txt
	if vowel(txt[-1]):
		return ""
	else:
		try:
			return consonant_seq_before(txt[:-1]) + txt[-1]
		except: 
			print(consonant_seq_before(txt[:-1]), txt[-1])
			return ""
		
def consonant_seq_after(txt) -> str:
	"""
	Given some string, finds all consonants at beginning of a string (until interrupted by vowel).
	Assumes that the string is a suffix for a year.
	"""
	if len(txt) == 1:
		if vowel(txt):
			return ""
		return txt
	if vowel(txt[0]):
		return ""
	else:
		try:
			return txt[0] + consonant_seq_after(txt[1:]) 
		except:
			print(txt[0], consonant_seq_after(txt[1:]))
			return ""
			
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
<<<<<<< HEAD
=======
	before, after, count = statistics(yer_found)
	#save_as_text("data/stats_with_ek_before.txt", before)
	#save_as_text("data/stats_with_ek_after.txt", after)
	print("BEFORE:")
	print(before)
	print("AFTER:")
	print(after)
	print(count)
	
	#yer_found = remove_items(yer_found, "eczek")
	yer_found = remove_items(yer_found, "ek")
	save_as_text("data/lemmas_minus_ek.txt", yer_found)
	before, after, count  = statistics(yer_found)
	#save_as_text("data/stats_without_ek_before.txt", before)
	#save_as_text("data/stats_without_ek_after.txt", after)
	print("BEFORE:")
	print(before)
	print("AFTER:")
	print(after)
	print(count)
	
	
	#get stats
	#remove 'ek'
	#repeat
>>>>>>> Fixing statistics

################################
if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()