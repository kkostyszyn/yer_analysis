#import re
#import pynini
import sys

def main(f):
    """
    First, open Polish morphological data compiled by Unimorph. 
    
    Then, for all inflected forms, compare to the lemma to find inserted/deleted vowels - sign of yer. 
    
    See if there is a way to generalize across resulting patterns.
    """
    f = open(f)
    f = f.readlines()
    
    for x in f:
        temp = re.split("\s", x)
        if not cur:
            if lst:
                paradigm(lst)
                pass 
            cur = temp[0]
            lst = []
        lst.append(temp[1])
    #[0] = lemma
    #[1] = inflected form 
    return True

def paradigm(lst):
    """
    For a list of inflected forms, find possible yers. 
    """
    return True 

if __name__=="__main__":
    main(sys.argv[-1])