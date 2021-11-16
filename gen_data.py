"""
First, create a script that has the shape of the paradigm as a class - logging morpho info, phono info, number of syllables before yer, etc.

Then, run statistical analyses on all paradigms to find significant features. 
"""
import re
import sys
from paradigm import Paradigm, Features
from translate_pol import Translate

def consonant_seq_before(txt: list) -> str:
	"""
	Given some string, finds all consonants at the end of the string (until interrupted by vowel).
	Assumes that the string is the prefix for a yer.
	
	txt:	a list of phones
	"""
	
	#Base case - if a single phone, return either an empty list 
	if len(txt) <= 1:
		if not vowel(txt[0]):
			return txt[0]
		return ''
		
	#Otherwise - Check if current last phone is a consonant, then repeat on next 
	#If vowel, end sequence
	if vowel(txt[-1]):
		return ''
	else:
		return consonant_seq_before(txt[:-1]) + txt[-1]

def consonant_seq_after(txt: list) -> str:
	"""
	Given some string, finds all consonants at beginning of a string (until interrupted by vowel).
	Assumes that the string is a suffix for a year.
	
	txt:	a list of phones
	"""
	
	if len(txt) <= 1:
		if not vowel(txt[0]):
			return txt[0]
		return ''
		
	if vowel(txt[0]):
		return ""
	else:
		return txt[0] + consonant_seq_after(txt[1:])

def domain(lst):
	"""
	Shortcut for range(len()), so I don't forget to remove the final position :)
	
	lst: an arbitrary list of some length
	"""
	return (range(len(lst) - 1))

def extract_syllable_no_yer(lem: list) -> str:
	"""
	For a word pair with no yer, take the lemma, and go backward finding the last syllable set of CVC.
	"""
	return True

def feature_dictionary(labels: list, values: list) -> dict:
	"""
	Takes the list of labels for features and correlates them with the values for a specific phone.
	"""
	rtn = {}
	for i in domain(values[1:]):
		rtn[labels[i]] = values[i]
	return rtn 
	
def prefix(st: str, pos: int):
	"""
	Shortcut to return a substring, sliced up to an excluding a certain position.
	
	st:	some string
	pos:	a position within that string
	"""
	return st[:pos]
	
def remove_items(d, suffix: str, after = False) -> dict:
	"""
	Removing items with substring from list.
	
	d:	the initial dictionary, where items will be removed based on their keys.
	suffix:		a substring of the key that must be removed (if after==False, may not strictly be a suffix)
	after:		a Boolean that tells if the suffix is necessarily word final   
	
	d_copy:	the dictionary, after keys containing suffix (and possibly after) are removed
	temp:	the division of the current string, where temp[0] is the information before the suffix and temp[-1] is the information after
	to_pop:	a Boolean - if true, an item is not copied from d to d_copy 
	"""
	d_copy = {}
	for i in d:
		if not after and suffix in i:
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

def remove_newline(txt: str) -> str:
	"""
	Takes some string, and if there is a trailing newline character '\n', removes it.
	
	txt: the line of text
	"""
	if txt[-1:] == "\n":
		txt = txt[:-1]
	return txt
	
def root_without_final_vowels(txt: str) -> str:
	"""
	For any root, cut off any and all final vowels.
	"""
	vowels = ['a', 'i', 'u', 'e', 'o', 'y', 'ą', 'ę', 'ó', 'ɔ', 'ɛ', 'ɨ'] 
	
	#so long as the final character is a vowel, continue removing 
	while txt[-1] in vowels:
		txt = txt[:-1]
	return txt 

def save_as_text(save, data):
	"""
	Shortcut to write data to a file for later analysis.
	
	save: the location of the file
	data:	the information to be saved in the file
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
	
def statistics(d, path, features):
	"""
	!! REWRITE THIS TO USE THE PARADIGM CLASS, and to write to a file in TSV format so values are 
	still linked 
	
	Takes the yer-found dictionary and uses the prefix to save the environment before and after for
	stats.
	
	d: a dictionary, where the key is the orthographic word, and the value is a Paradigm object 
	features:	a dictionary where a phone is the key is a single phone, and the value is a second 
						dictionary - the key is a feature label and its value is the corresponding 
						feature value for the current phone.
	path:		the name of the file where statistics will be saved
	---	
	count:		the number of words considered when building dictionaries 
	env_after:	a dictionary, where the key is the consonant sequence after the yer and the value 
						is the number of instances
	env_before:		a dictionary, where the key is the consonant sequence before the yer and the 
						value is the number of instances
	immediate_after:	a dictionary, where the key is the singular consonant after the yer and the
						value is the number of instances
	immediate_before:	a dictionary, where the key is the singular consonant before the yer and 
						the value is the number of instances
	prefix_align:	a dictionary, where the key is the orthographic word and the value is a tuple 
						of the environment before the yer (b) and the environment after the yer (e)
	"""
	
	fle = open(path, "w+")
	fle.write("LEMMA\tPREFIX\tBEFORE_SEQ\tAFTER_SEQ\tBEFORE_SING\tAFTER_SING\tINFLEC")
	#what other featural information to include? palatals & sonorants primarily
	
	env_before = {}
	immediate_before = {}
	env_after = {}
	immediate_after = {}
	count = 0
	
	prefix_align = {}
	
	for i in d.keys():
		for j in d.forms.keys():
			#Remember that the items in d[i] are lists, not strings.
			count += 1
			
			#Find environment BEFORE yer 
			try:
				b = consonant_seq_before(d[i][j].prefix())
			except:
				print("Fail consonant_seq_before(",d[i][j].prefix(),") - ",i)
					
			#Find environment AFTER yer 
			#first, remove prefix
			#then, remove any further vowels
			### THIS WILL NEED CHANGING, to apply to all forms associated with the lemma
			temp = suffix(d[i][j].lemma())
			if temp:
				e = consonant_seq_after(temp)
			else:
				e = ''
				
			#should i only add one form to the document?
			#Determine if yer in lemma vs. yer in inflected form
			fle.write(d[i][j].lemma() + "\t" + 
									d[i][j].prefix() + "\t" +
									b + "\t" +
									e + "\t" +
									b[-1] + "\t" + 
									temp[0] + "\t" +
									j + "\n") #should be the morphological information, which right now is the key to the Paradigm.forms dictionary

			#Add to env dictionaries 
			try:
				env_before[b] += 1
			except:
				env_before[b] = 1
			
			try:
				env_after[e] += 1
			except:
				env_after[e] = 1
				
			#Add to immediate dictionaries
			try:
				immediate_before[d[i][j].prefix()[-1]] += 1
			except:
				immediate_before[d[i][j].prefix()[-1]] = 1
				
			try:
				immediate_after[temp[0]] += 1
			except:
				immediate_after[temp[0]] = 1
				
			#prefix_align[i] = (b, e)
		
	#print("AFFIXES PER WORD:", prefix_align)
	#Now that I'm printing to a document, it may be unnecessary to return these values
	return (env_before, env_after, immediate_before, immediate_after, count)
	
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
	txt[1] = re.sub("[,\s]", "", txt[1])
	
	return txt

def suffix(d: dict):
	"""
	When finding the environment after the yer, strip initial vowels. 
	
	txt: a dictionary with 'IPA' and 'prefix' as the keys.
	"""
	
	#First, remove the prefix from the IPA form 
	print(d)
	p = d['prefix']
	txt = d['IPA']
	
	while p:
		p = p[1:]
		txt = txt[1:]
	
	while vowel(txt[0]):
		txt = txt[1:]
	return txt
		
def test_print(data):
    """
    Purely for testing purposes.
    """
    temp = 0
    for i in data:
        if temp % 5 == 0:
            print(i, data[i], end="\n\n")
    temp += 1

def to_str(lst: list) -> str:
	x = ''
	if isinstance(lst, list):
		for item in lst:
			x = x + item
	return x
	
def vowel(ch) -> bool:
	"""
	Determines if a character is a vowel or not.
	"""
	vowels = ["a", "i", "ɔ", "u", "ɛ", "ɨ", "ɔ̃", "ɛ̃"]
	 
	if ch in vowels:
		return True
	return False 
	
def word_boundary(word1: list, word2: list, position: int) -> bool:
	"""
	Given two words, determine if the end word boundary has been reached for either of them.
	"""
	if position >= len(word1):
		return True
	elif position >= len(word1):
		return True
	return False
	
def main(load = False):
	"""
	Based on previous Pynini script, do POL-->IPA transcription.
	Turn into function, so that it can be incorporated into MAIN code - when an N is found in the 
	tagset, append the transcribed form, using lemma as key.

	Wikipron is being used to simplify the process, but only accounts for a fraction of the noted 
	forms. 
	"""
	#the Translate class is a large transducer that carries out the translation from Polish to IPA 
	tr = Translate()
	
	if not load: #if i'm rebuilding the 'bundle' list 

		wp = open("input/pol_latn_broad.tsv", "r", encoding="utf8")
		wp = wp.readlines()

		pron_dict = {}
		morph_info = {}

		for line in wp:
			temp = re.split(r"\t", line)
			pron_dict[temp[0]] = re.split(r"\n", temp[1])[0] #Remove trailing \n from wikipron document
		"""
		Open Polish morphological data compiled by Unimorph. 
			
		Then, for all inflected forms, compare to the lemma to find inserted/deleted vowels - sign of yer. 
			
		See if there is a way to generalize across resulting patterns.
		"""
		f = open("input/pol.txt", encoding="utf8")
		f = f.readlines()

		bundles = {}
		leftover = []
			
		for x in f:
			temp = re.split(r"\s+", x)
			tags = re.split(r";", temp[2])
			if tags[0] == 'N' and temp[0].lower() == temp[0]: #remove proper nouns - Zydow, Amerikanami
				#add dictionary of inflectional information to add to the paradigms 
				if temp[0] not in bundles.keys():
					bundles[temp[0]] = []
				#Change this line when building for Paradigm object - revert to tuples
				#temp[1] is the inflected form, temp[2] is the inflectional information
				
				try:
					bundles[temp[0]].append(((tr.t(temp[1])).split(), temp[2]))
				except:
					#Strings that contain 'q' or punctuation (hyphenation, apostrophes, etc.) will be rejected by the transducer. 
					print(temp[1])
		#Using this saved text, generate a new bundles dictionary 
		save_as_text("data/SAVE.txt", bundles)
	else: #if i'm using the saved bundle list 
		#bun = open("data/SAVE.txt", "r")
		bun = open(load, "r")
		bun = bun.readlines()
		
		bundles = {}
		temp = ''
	
		for line in bun:
			line = line.split(":")
			if len(line) > 1:
				temp = line[0]
			ipa, inf = strip_text(line[-1])
			
			if bundles.get(temp):
				bundles[temp][inf] = ipa
			else:
				bundles[temp] = {inf: ipa}

	#Remove exceptional forms, with significantly different forms (czlowiek~ludzi, tydzien~tygodniu).
	ex = open("input/exceptions.txt", "r")
	ex = ex.readlines()
	for word in ex:
		word = re.sub(r"\s", r"", word)
		if bundles.get(word):
			bundles.pop(word)
		
	yer_found = {}
	yer_found_par = {}
	#For every item in the bundles dictionary, compare the 'lemma' (minus final vowels) to each 
	#root and find yer environment 
	for root in bundles.keys():
		try:
			temp = root_without_final_vowels(tr.t(root).split())
			
			for inflected_form in bundles[root]:
				for ch_pos in domain(temp):
					if vowel(temp[ch_pos]) != vowel(bundles[root][inflected_form][ch_pos]):
						#if, for any consonant in one form, the corresponding character in the 
						#other form is a vowel (or vice versa) - log this as the prefix, marking a yer.
						
						#ONLY look in the 'root'
						if vowel(temp[ch_pos]):
							pre = prefix(temp, ch_pos)
							in_lem = False
						else: 	
							pre = prefix(bundles[root][inflected_form], ch_pos)
							in_lem = True 
						
						yer_found[root] = {'IPA': temp, 'prefix': prefix(temp, ch_pos)}
						
						#If the paradigm oesn't already exist, add it to the dictionary
						#In all cases, update to map inflected form to inflectional info 
						if not yer_found_par.get(root):
							yer_found_par[root] = Paradigm(root, yer_found[root]['prefix'])
						yer_found_par[root].update(bundles[root][inflected_form], re.sub(r"[,\s]", r"", inflected_form), in_lem)

					#elif we've found the word boundary in either word, store as No Yer 			
					elif word_boundary(temp, bundles[root][inflected_form], ch_pos):
						extract_syllable_no_yer()
		except: 
			print("Translation failure:", root)
						
	save_as_text("data/lemmas.txt", yer_found)
	print(len(yer_found_par))
	
	#create a Feature dictionary to feed into statistics, so all stats are written at once
	feat = open("input/Features.ascii.tsv", "r")
	feat = feat.readlines()
	features = {}
	feature_columns = {}
	
	#Extract possible features from first line
	#Remove trailing \n
	feat[0] = (remove_newline(feat[0])).split("\t")
	
	#correlate the feature to the column number for later use 
	for pos in domain(feat[0]):
		if feat[0][pos]:
			feature_columns[pos] = feat[0][pos]
	#for every remaining phone in the list, save first element (phone) as the key, with the value
	#a dictionary that maps each feature to +, -, or 0
	for phone in feat[1:]:
		phone = phone.split("\t")
		vals = {}
		for pos in domain(phone):
			#first item in lists is an empty string, which is retained for positional alignment
			if feature_columns.get(pos):
				vals[feature_columns[pos]] = phone[pos]
		features[phone[0]] = vals
		
	print(features)
	
	before, after, immediate_before, immediate_after, count = statistics(yer_found_par, "data/stats_before_ek.tsv", features)
	#save_as_text("data/stats_with_ek_before.txt", before)
	#save_as_text("data/stats_with_ek_after.txt", after)
	print("BEFORE:", end="")
	print(before)
	print("AFTER:", end="")
	print(after)
	print("IMMEDIATE BEFORE:", end="")
	print(immediate_before)
	print("IMMEDIATE AFTER:", end="")
	print(immediate_after)
	print(count)
	
	
	
	#repeat above without diminutives
	"""
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
	"""
	
	
	

################################
if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()