"""
First, create a script that has the shape of the paradigm as a class - logging morpho info, phono info, number of syllables before yer, etc.

Then, run statistical analyses on all paradigms to find significant features. 
"""
import re
import sys
import random
from paradigm import Paradigm
from translate_pol import Translate

def concatenate(lst: list) -> str:
	out = ''
	for item in lst:
		if isinstance(item, str): out += item
		else: return False 

	return out
def consonant_seq_before(txt: list) -> str:
	"""
	Given some string, finds all consonants at the end of the string (until interrupted by vowel).
	Assumes that the string is the prefix for a yer.
	
	txt:	a list of phones
	"""
	
	#Base case - if a single phone, return either an empty list 
	if len(txt) <= 1:
		try:
			if not vowel(txt[0]):
				return txt[0]
		except:
			pass
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

def extract_syllable_no_yer(form: list) -> str:
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

def no_yer_statistics(d, path, features, pnt = False):
	"""
	A simplified version of the statistics() function.
	"""
	
	fle = open(path, "a")
	#Split inflectional info on ; ? 
	first_line = "FORM\tPREFIX\tINFLECT\tBEFORE_SEQ\tAFTER_SEQ\tBEFORE_SING\tAFTER_SING\tINFLEC\t"
	#this is honestly excessive, but i want to keep the features as arbitrary as possible
	temp_feat = random.choice(list(features.keys()))
	temp_feat = features[temp_feat]
	temp_feat = temp_feat.keys()
	
	return True 
		
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
	
def statistics(d, path, features, pnt = False):
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
	pnt:			Boolean to decide whether to print the help messages
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
	#Split inflectional info on ; ? 

	fle.write("%Polish yer prediction\n@relation polish_yer\n\n")

	
	first_line_attributes = {"FORM":"string", "PREFIX":"string", "CASE":"string", "PLURAL":"string",
			"BEFORE_SEQ":"string", "AFTER_SEQ" :"string", "BEFORE_SING":"string", "AFTER_SING":"string"}
	first_line = ""
	for att in first_line_attributes.keys():
		first_line += "@attribute " + att + " " + first_line_attributes[att] + "\n"
	#this is honestly excessive, but i want to keep the features as arbitrary as possible
	temp_feat = random.choice(list(features.keys()))
	temp_feat = features[temp_feat]
	temp_feat = temp_feat.keys()
	
	#Cluster before_ and after_ segments together
	for f in temp_feat:
		first_line += "@attribute LEFT_" + f.upper() + "{+, -, 0}\n"
	for f in temp_feat:
		first_line += "@attribute RIGHT_" + f.upper() + "{+, -, 0}\n"
		
	first_line += "@attribute PARADIGM_YER {TRUE,FALSE}\n"
	first_line += "@attribute FORM_YER {TRUE,FALSE}\n"
	fle.write(first_line)

	fle.write("\n\n")
	fle.write("@data\n")
	
	count = 0
		
	for i in d.keys():
		if pnt: print("---")
		for j in d[i].form_keys():
			try:
				
				#Remember that the items in d[i] are lists, not strings.
				count += 1
				if pnt: print("Processing:", i, j, "<"+str(d[i].f(j)[0]) +">", end="...")
				
				#Find environment BEFORE yer 
				try:
					b = consonant_seq_before(d[i].pre())
					if b == 'ʲ':
						print("Palatalized")
				except:
					print("Fail consonant_seq_before(",str(d[i].pre()),") - ",i)
						
				#Find environment AFTER yer 
				#first, remove prefix
				#then, remove any further vowels
				### THIS WILL NEED CHANGING, to apply to all forms associated with the lemma
				#temp = suffix(d[i].lemma())
				temp = suffix(d[i].pre(), d[i].f(j))
				if temp:
					e = consonant_seq_after(temp)
				else:
					e = ''

				#Break j (morphological inflection) along semicolon, and write 1st (case) and 2nd (plural) to line
				inflect_info = re.findall(r"\w+", j)
					
				#Update this so it's one line with the environmental info, plus the features
				#Then, write that variable to file.
				
				#Lemma - prefix - before_seq - after_seq - before_seg - after_seg - morph - feats
				it = [concatenate(d[i].f(j)[0]), concatenate(d[i].pre()), inflect_info[1], inflect_info[2], b, e, b[-1], temp[0]]
				stats_line = ''
				#Make it a loop to improve readability
				for e in it:
					stats_line += e + ","

				#then, for each feature for the before_seg and after_seg, add +/-
				for f in features[b[-1]].keys():
					#stats_line = stats_line + features[b[-1]].get(f, "") + ","
					if features.get(b[-1]):
						stats_line = stats_line + features[b[-1]].get(f, "PREFIX_FAILED") + ","
					elif 'ʲ' in b[-1]:
						tmp_p = re.sub(r'ʲ', r'', b[-1])
						if features.get(tmp_p):
							stats_line = stats_line + features[tmp_p].get(f, "PREFIX_FAILED") + ","
							#set markert for palatal here
					elif not b[-1]:
						#If prefix is empty for some reason:
						stats_line = stats_line + features['#'].get(f, "") + ","
					
				for f in features[e].keys():
					#stats_line = stats_line + features[e].get(f, "") + ","
					if features.get(e):
						stats_line = stats_line + features[e].get(f, "SUFFIX_FAILED") + ","
					elif 'ʲ' in e:
						tmp_p = re.sub(r'ʲ', r'', e)
						if features.get(tmp_p):
							stats_line = stats_line + features[tmp_p].get(f, "SUFFIX_FAILED") + ","
					elif not e:
						#If suffix is empty for some reason:
						stats_line = stats_line + features['#'].get(f, "") + ","


				if d[i].ind_yer(j)[1]:
					form_yer = "TRUE"
				else:
					form_yer = "FALSE"
				#Then, check for global yer
				fle.write(stats_line + "TRUE," + form_yer + "\n")
				#print(stats_line)
				if pnt: print("done!")
				#After building the base of the stats_line
			except:
				if pnt: print("ERROR ON <", i,">")
			
	#Now that I'm printing to a document, it may be unnecessary to return these values
	#return (env_before, env_after, immediate_before, immediate_after, count)
	if pnt: print("Stats for", path, "complete!")
	fle.close()

def statistics_no_yer(d, path, features, pnt = False):
	"""
	Like the previous statistics() function, except for words with no yer present, so some generalizations are made.

	d:			list of words where yer was not found, where d: (inflected form, inflectional info)
	path:		file path for saving data
	features:	dictionary of featural information 
	"""
	fle = open(path, "a+")
	#Split inflectional info on ; ? 
	#first_line = "FORM,PREFIX,CASE,PLURAL,BEFORE_SEQ,AFTER_SEQ,BEFORE_SING,AFTER_SING,"
	#this is honestly excessive, but i want to keep the features as arbitrary as possible
	temp_feat = random.choice(list(features.keys()))
	temp_feat = features[temp_feat]
	temp_feat = temp_feat.keys()
	
	#Cluster before_ and after_ segments together
	#for f in temp_feat:
	#	first_line += "LEFT_" + f.upper() + ","
	#for f in temp_feat:
	#	first_line += "RIGHT_" + f.upper() + ","
		
	#first_line += "PARADIGM_YER,FORM_YER\n"
	#fle.write(first_line)

	count = 0
		
	for i in d:
		if pnt: print("---")

		count += 1
		if pnt: print("Processing:", i, "<"+str(d[1]) + ">", end="...")
		
		
		temp_root = root_without_final_vowels(i[0])
		#Find next consonant, then replicate prefix function (since no positional marker)
		temp_prefix = temp_root
		temp_suffix = ''
		prefix_found = False
		vowel_found = False

		while not prefix_found:
			if not vowel_found:
				temp_suffix = temp_prefix[-1] + temp_suffix
				temp_prefix = temp_prefix[:-1]
				try:
					if vowel(temp_prefix[-1]):
						vowel_found = True
				except:
					prefix_found = True
			else:
				temp_prefix = temp_prefix[:-1]
				try:
					if len(temp_prefix) > 1:
						if not vowel(temp_prefix[-1]):
							prefix_found = True
					else:
						prefix_found = True
				except:
					prefix_found = True

		inflect_info = re.findall(r"\w+", i[1])

		#Lemma - prefix - case - plural - before_seq - after_seq - before_sing - after_sing
		if len(temp_prefix) > 1: prefix_sing = temp_prefix[-1]
		elif len(temp_prefix) == 0: prefix_sing = ''
		it = [concatenate(temp_root), concatenate(temp_prefix), inflect_info[1], inflect_info[2], consonant_seq_before(temp_prefix), temp_suffix, prefix_sing, temp_suffix[0]]
		#print(it)
		stats_line = ''
		#Make it a loop to improve readability
		for e in it:
			if e == '': e = '#'
			stats_line += e + ","

		#then, for each feature for the before_seg and after_seg, add +/-
		if features.get(prefix_sing):
			for f in features[prefix_sing].keys():
				stats_line = stats_line + features[prefix_sing].get(f, "PREFIX_FAILED") + ","
		elif 'ʲ' in prefix_sing:
			tmp_p = re.sub(r'ʲ', r'', prefix_sing)
			if features.get(tmp_p):
				for f in features[tmp_p].keys():
					stats_line = stats_line + features[tmp_p].get(f, "PREFIX_FAILED") + ","
				#set markert for palatal here
		elif not prefix_sing:
			#If prefix is empty for some reason:
			for f in features['#'].keys():
				stats_line = stats_line + features['#'].get(f, "FAILED") + ","

		if features.get(temp_suffix[0]):
			for f in features[temp_suffix[0]].keys():
				stats_line = stats_line + features[temp_suffix[0]].get(f, "SUFFIX_FAILED") + ","
		elif 'ʲ' in temp_suffix[0]:
			tmp_p = re.sub(r'ʲ', r'', temp_suffix[0])
			if features.get(tmp_p):
				for f in features[tmp_p].keys():
					stats_line = stats_line + features[tmp_p].get(f, "SUFFIX_FAILED") + ","
		elif not temp_suffix:
			#If suffix is empty for some reason:
			for f in features['#'].keys():
				stats_line = stats_line + features['#'].get(f, "FAILED") + ","

		fle.write(stats_line + "FALSE,FALSE\n")
			
	#Now that I'm printing to a document, it may be unnecessary to return these values
	#return (env_before, env_after, immediate_before, immediate_after, count)
	if pnt: print("Stats for", path, "complete!")
	fle.close()
	
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

def suffix(p: str, txt: list):
	"""
	When finding the environment after the yer, strip initial vowels. 
	
	p:		the prefix preceding the yer
	txt:	a list of the characters in the word form 
	"""
	
	#First, remove the prefix from the IPA form 
	#p = d['prefix']
	txt = txt[0]
	#print(p, txt)
	
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
		
	no_yer_count = 0
		
	yer_found = {}
	yer_found_par = {}
	yer_not_found = []
	#For every item in the bundles dictionary, compare the 'lemma' (minus final vowels) to each 
	#root and find yer environment 
	for root in bundles.keys():

		try:
			temp = root_without_final_vowels(tr.t(root).split())
			
			for inflected_form in bundles[root]:
				yer_bool = False 

				for ch_pos in domain(temp):
					#if root and not inflected
					if vowel(temp[ch_pos]) != vowel(bundles[root][inflected_form][ch_pos]):
						yer_bool = True
						#if, for any consonant in one form, the corresponding character in the 
						#other form is a vowel (or vice versa) - log this as the prefix, marking a yer.
						
						yer_found[root] = {'IPA': temp, 'prefix': prefix(temp, ch_pos)}

						#If the paradigm oesn't already exist, add it to the dictionary
						#In all cases, update to map inflected form to inflectional info 
						if not yer_found_par.get(root):
							yer_found_par[root] = Paradigm(root, yer_found[root]['prefix'])
						yer_found_par[root].update(bundles[root][inflected_form], re.sub(r"[,\s]", r"", inflected_form), False)
					#elif inflected and not root
					
				if not yer_bool:
					#If there is no yer found, will write the items to a list to mark as yer_free
					#Move this back so it only runs after a paradigm is deemed to have no yer, but 
					#it adds all the forms to the list.
					no_yer_count +=1
					try:
						yer_not_found.append((bundles[root].get(inflected_form), inflected_form))
					except:
						print("No yer found in:", root, inflected_form)
				else: 
					#Make sure all items in paradigm are marked for a global yer
					yer_found_par[root].update_all_yers()

					#Add forms that have no vowel-based differences - yer found globally, but no difference from lemma here
					for inflected_form in bundles[root]:
						if not yer_found_par[root].f(inflected_form):
							yer_found_par[root].update(bundles[root][inflected_form], re.sub(r"[,\s]", r"", inflected_form), True)

		except: 
			print("Translation failure:", root)
			pass
		
	save_as_text("data/lemmas.txt", yer_found)
	print("Found:", len(yer_found_par), "; No yer:", no_yer_count)
	
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
			
	statistics(yer_found_par, "data/stats_before_ek.arff", features)
	statistics_no_yer(yer_not_found, "data/stats_before_ek.arff", features)
	#repeat stats on non-yers words, appending to same path	
	
	#repeat above without diminutives
	
	yer_found = remove_items(yer_found, "eczek", True)
	yer_found = remove_items(yer_found, "ek", True)

	#print(yer_found)
	
	
	
	

################################
if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()
