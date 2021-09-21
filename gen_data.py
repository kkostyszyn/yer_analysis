"""
First, create a script that has the shape of the paradigm as a class - logging morpho info, phono info, number of syllables before yer, etc.

Then, run statistical analyses on all paradigms to find significant features. 
"""
import re
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
    f = open(save, "w", encoding="utf8")
    
    if isinstance(data, dict):
        for x in data.keys():
            f.write(x+":")
            for text in data[x]:
                f.write("\t" + text)
            f.write("\n")
    else: 
        pass		
    f.close()
	
def main():
	"""
	Based on previous Pynini script, do POL-->IPA transcription.
	Turn into function, so that it can be incorporated into MAIN code - when an N is found in the tagset, append the transcribed form, using lemma as key.

	Wikipron is being used to simplify the process, but only accounts for a fraction of the noted forms. 
	"""

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
		if tags[0] == 'N':
			if temp[0] not in bundles.keys():
				bundles[temp[0]] = []
			#Change this line when building for Paradigm object - revert to tuples
			#temp[1] is the inflected form, temp[2] is the inflectional information
			#bundles[temp[0]].append(temp[1] + "//" + temp[2]) #for save_as_text
			if temp[1] in pron_dict.keys():
				bundles[temp[0]].append((pron_dict[temp[1]], temp[2]))
			else:
				bundles[temp[0]].append(("NO PRONUNCIATION: " + temp[1], temp[2]))
					
	#save_as_text("data/SAVE.txt", bundles)
	test_print(bundles)
	"""
	for x in bundles.keys():
		print(Paradigm(x, bundles[x]))"""
################################
if __name__ == "__main__":
	main()