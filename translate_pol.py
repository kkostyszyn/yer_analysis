import pynini
import functools
import re

class Translate:

	"""
		A single class that will build all then requisite FSTs for translation.
		
		In __init__ I have to update the output chars to match those of WikiPron. Then, translate() should actually translate the strings. 
	"""
	
	def __init__(self) -> None:
		A = functools.partial(pynini.acceptor, token_type="utf8")
		T = functools.partial(pynini.transducer, input_token_type="utf8", output_token_type="utf8")
		epsilon = pynini.epsilon_machine()

		#DEFINE POLISH INVENTORY - INPUT VS. OUTPUT
		vowels_in = (A("a") | A("ą") | A("e") | A("ę") | A("i") | A("o") | A("ó") | A("u") | A("y"))
		vowels_out =(A("a") | A("i") | A("ɔ") | A("u") | A("ɛ") | A("ɨ") | A("ɔ̃"))
		
		cons_in = (A("b") | 
					A("c") | 
					A("ć") |    
					A("d") | 
					A("f") |    
					A("g") |    
					A("h") |    
					A("j") |    
					A("k") |    
					A("l") |    
					A("ł") |    
					A("m") |    
					A("n") |    
					A("ń") |    
					A("p") |    
					A("r") |    
					A("s") |    
					A("ś") |    
					A("t") |    
					A("w") |    
					A("z") |    
					A("ź") |    
					A("ż"))
		cons_out = (A("b") | 
					A("[t͡s]") | #orthographic c
					A("[t͡ʂ]") | #orthographic ć
					A("[t͡ɕ]") | #palatalized
					A("d") | 
					A("[d͡z]") | #dz
					A("[d͡ʑ]") | #palatal dz
					A("[d͡ʐ]") | #dż
					A("f") |    
					A("g") |    
					A("ɟ") | #palatal g 
					A("x") | #h
					A("j") |    
					A("k") | 
					A("c") | #palatal k   
					A("l") |    
					A("w") | #ł
					A("m") |    
					A("n") |    
					A("ɲ") | #ń 
					A("p") |    
					A("r") |    
					A("s") |    
					A("ʂ") | #ś    
					A("ɕ") | #palatal s
					A("t") |    
					A("v") | #w  
					A("z") |    
					A("ʑ") | #ź
					A("ʐ")) #ż

		helpers = (A("~") | A("ʲ") | A("͡"))
		palatals = (A("ɕ") | A("ʑ") | A("ɲ") | A("ɟʲ"))

		sigma_without_space = pynini.closure(vowels_in | vowels_out | cons_in | cons_out | helpers | epsilon )
		sigmaStar = pynini.closure(sigma_without_space | A(" ") | A(""))
		"""
		PALATALIZATION
		"""
		# 1) Insert ʲ to mark palatalization
		add_pal = pynini.cdrewrite(T("", "ʲ"), cons_in | cons_out, A("i"), sigmaStar).optimize()
		#2) For fricatives & /n/, rewrite sequence with new character
		s_pal = (T("sʲi", "ɕi") | T("ś", "ɕ"))
		s_palatal = pynini.cdrewrite(s_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
		z_pal = (T("zʲi", "ʑi") | T("ź", "ʑ"))
		z_palatal = pynini.cdrewrite(z_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
		n_pal = (T("nʲi", "ɲi") | T("ń", "ɲ"))
		n_palatal = pynini.cdrewrite(n_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
		aff_pal = (T("[t͡s]ʲi", "[t͡ɕ]i") | T("[d͡z]ʲi", "[d͡ʑ]i"))
		aff_palatal = pynini.cdrewrite(aff_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
		redundant = pynini.cdrewrite(T("jʲ", "j"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#3) figure out how to rewrite JiV sequences as JjV
		#STILL PROBLEMATIC
		pal_before_vowel = pynini.cdrewrite(T("i", ""), "ʲ", vowels_in | vowels_out | "[EOS]", sigmaStar).optimize()
		  
		self.palatalization = (add_pal @ pal_before_vowel @ s_palatal @ z_palatal @ n_palatal @ aff_palatal @ redundant).optimize()

					
		"""
		MULTI-CHARACTER
		"""		
		#sz
		sz = pynini.cdrewrite(T("sz", "ʂ"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#ch    
		ch = pynini.cdrewrite(T("ch", "x"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#cz
		cz = pynini.cdrewrite(T("cz", "[t͡ʂ]"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#rz
		rz = pynini.cdrewrite((T("rz", "ʐ") | T("ż", "ʐ")), sigmaStar, sigmaStar, sigmaStar).optimize()
			
		self.multi_char = (sz @ ch @ cz @ rz).optimize()


		
		"""
		VOICING ASSIMILATION
		"""
		#make sure the right consonants are where theyre supposed to be 
		voiced_cons = (A("b") | 
					A("d") | 
					A("[d͡z]") | #dz
					A("[d͡ʑ]") | #palatal dz
					A("[d͡ʐ]") | #dż
					A("g") |    
					A("ɟ") | #palatal g 
					A("x") | #h
					A("j") |     
					A("l") |    
					A("w") | #ł
					A("m") |    
					A("n") |    
					A("ɲ") | #ń      
					A("v") | #w  
					A("z") |    
					A("ʑ") | #ź
					A("ʐ")) #ż)
		voiceless_cons = (A("[t͡s]") |
					A("[t͡ɕ]") |
					A("[t͡ʂ]") | #orthographic ć
					A("f") |    
					A("x") | #h
					A("k") | 
					A("c") | #palatal k   
					A("p") |    
					A("r") | 					
					A("s") |    
					A("ʂ") | #ś    
					A("ɕ") | #palatal s
					A("t"))
		devoiced_pairs = (T("b", "p") | T("d", "t") | T("g", "k") | T("v", "f") | T("z", "s") | T("ʐ", "ʂ") | T("ʑ","ɕ") | T("[d͡z]","[t͡s]") | T("[d͡ʐ]","[t͡ʂ]"))
		voiced_pairs = (T("p", "b") | T("t", "d") | T("k", "g") | T("f", "v") | T("s", "z") | T("ʂ", "ʐ") | T("ɕ", "ʑ") | T("[t͡s]", "[d͡z]") | T("[t͡ʂ]", "[d͡ʐ]"))
		word_final_devoicing = pynini.cdrewrite(devoiced_pairs, sigmaStar, "[EOS]", sigmaStar).optimize()
		regressive_voicing = pynini.cdrewrite(voiced_pairs, sigmaStar, voiced_cons, sigmaStar).optimize()
		regressive_devoicing = pynini.cdrewrite(devoiced_pairs, sigmaStar, voiceless_cons, sigmaStar).optimize()
		self.voicing = (word_final_devoicing @ regressive_devoicing @ regressive_voicing).optimize()
					
		"""
		SINGLE CHARACTERS
		"""		
		#w->v
		w = pynini.cdrewrite(T("w", "v"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#c->ts
		c = pynini.cdrewrite(T("c", "[t͡s]"), sigmaStar, sigmaStar, sigmaStar).optimize()
		tc = pynini.cdrewrite(T("ć", "[t͡ʂ]"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#h->x
		h = pynini.cdrewrite(T("h", "x"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#l->w
		barred_L = pynini.cdrewrite(T("ł", "w"), sigmaStar, sigmaStar, sigmaStar).optimize()
		
		#Update vowels
		nasals = pynini.cdrewrite(T("ą", "ɔ̃") | T("ę", "ɛ~"), sigmaStar, sigmaStar, sigmaStar).optimize()
		other_vowels = pynini.cdrewrite(T("e", "ɛ") | T("o", "ɔ") | T("ó", "u") | T("y", "ɨ"), sigmaStar, sigmaStar, sigmaStar).optimize()
		
		self.sing_char = (w @ c @ tc @ h @ barred_L @ nasals @ other_vowels).optimize()
		

		#add spacings a la wikipron 
		self.add_spaces = pynini.cdrewrite(T("", " "), cons_out | vowels_out | A("ʲ"), cons_out | vowels_out, sigmaStar).optimize()

		#after spaces, change affricates back to normal unicode
		symbol_changes = (T("[d͡z]","d͡z") | T("[d͡ʑ]", "d͡ʑ") | T("[t͡s]", "t͡s") | T("[t͡ʂ]", "t͡ʂ") | T("[t͡ɕ]", "t͡ɕ") | T("[d͡ʐ]", "d͡ʐ"))
		self.symbols = pynini.cdrewrite(symbol_changes, sigmaStar, sigmaStar, sigmaStar)
			
#to determine the transcription of a single word, barring vowels    
	def t(self, line:str) -> str:
		A = functools.partial(pynini.acceptor, token_type="utf8")
		return (((A(line) @ self.palatalization @ self.multi_char @ self.voicing @ self.sing_char @ self.add_spaces @ self.symbols).optimize()).stringify(token_type="utf8"))
