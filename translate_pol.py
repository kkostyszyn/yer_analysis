import pynini
import functools
import re

class Translate:

	"""
		A single class that will build all then requisite FSTs for translation.
		
		In __init__ I have to update the output chars to match those of WikiPron. Then, translate() should actually translate the strings. 
	"""
	
	def __init__(self) -> None:
		self.A = functools.partial(pynini.acceptor, token_type="utf8")
		self.T = functools.partial(pynini.transducer, input_token_type="utf8", output_token_type="utf8")
		self.epsilon = pynini.epsilon_machine()

		#DEFINE POLISH INVENTORY - INPUT VS. OUTPUT
		vowels_in = (A("a") | A("ą") | A("e") | A("ę") | A("i") | A("o") |  A("ó") | A("u") | A("y"))
		vowels_out =(A("a") | A("i") | A("ɔ") | A("u") | A("ɛ") | A("ɨ"))
		
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
					A("C") | #orthographic c
					A("[tʃ]") | #orthographic ć
					A("d") | 
					A("[dz]") | #dz
					A("[dʑ]") | #palatal dz
					A("[dʒ]") | #dż
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
					A("ʃ") | #ś    
					A("ɕ") | #palatal s
					A("t") |    
					A("v") | #w  
					A("z") |    
					A("ʑ") | #ź
					A("ʒ")) #ż

		helpers = (A("~") | A(" "))

		sigma_out = (vowels_out | cons_out)
		sigmaStar = pynini.closure(vowels_in | vowels_out | cons_in | cons_out | helpers | epsilon )

		#FIX THIS
		# 1) For 'Cie' sequences, change to 'Cʲ i ɛ' sequence 
		# 2) All other instances (except the fricatives & nasal), rewrite 'Ci' as 'Cʲ'
		#find all instances of palatalization		
		s_pal = (T("si", "ɕi") | T("ś", "ɕ"))
		s_palatal = pynini.cdrewrite(s_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
		z_pal = (T("zi", "ʑi") | T("ź", "ʑ"))
		z_palatal = pynini.cdrewrite(z_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
		n_pal = (T("ni", "ɲi") | T("ń", "ɲ"))
		n_palatal = pynini.cdrewrite(n_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
		k_palatal = pynini.cdrewrite(T("ki", "kʲ"), sigmaStar, sigmaStar, sigmaStar).optimize()
		g_palatal = pynini.cdrewrite(T("gi", "ɟi"), sigmaStar, sigmaStar, sigmaStar).optimize()
		m_palatal = pynini.cdrewrite(T("mi", "mʲ"), sigmaStar, sigmaStar, sigmaStar).optimize()   
		  
		self.palatalization = (s_palatal @ z_palatal @ n_palatal @ k_palatal @ g_palatal @ m_palatal).optimize()

		#once palatalization is normalized, do 1-to-1 transductions for all other characters
			
		#other multi-character tranductions
		#dz combined into the z palatalization 
		#sz
		sz = pynini.cdrewrite(T("sz", "ʂ"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#ch    
		ch = pynini.cdrewrite(T("ch", "x"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#cz
		cz = pynini.cdrewrite(T("cz", "t͡ʂ"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#rz
		rz = pynini.cdrewrite((T("rz", "ʐ") | T("ż", "ʐ")), sigmaStar, sigmaStar, sigmaStar).optimize()
			
		self.multi_char = (sz @ ch @ cz @ rz).optimize()

		#Add rule for word-final devoicing 
			
		#single characters
		#w->v
		w = pynini.cdrewrite(T("w", "v"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#c->ts
		c = pynini.cdrewrite(T("c", "t͡s"), sigmaStar, sigmaStar, sigmaStar).optimize()
		tc = pynini.cdrewrite(T("ć", "t͡ɕ"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#h->x
		h = pynini.cdrewrite(T("h", "x"), sigmaStar, sigmaStar, sigmaStar).optimize()
		#l->w
		barred_L = pynini.cdrewrite(T("ł", "w"), sigmaStar, sigmaStar, sigmaStar).optimize()
		
		#Update vowels
		#		vowels_in = (A("a") | A("ą") | A("e") | A("ę") | A("i") | A("o") |  A("ó") | A("u") | A("y"))
		nasals = pynini.cdrewrite(T("ą", "a~") | T("ę", "ɛ~"), sigmaStar, sigmaStar, sigmaStar), optimize()
		other_vowels = pynini.cdrewrite(T("e", "ɛ") | T("o", "ɔ") | T("ó", "u") | T("y", "ɨ"), sigmaStar, sigmaStar, sigmaStar).optimize()
			
		self.sing_char = (w @ c @ tc @ h @ barred_L @ nasals @ other_vowels).optimize()
			
#to determine the transcription of a single word, barring vowels    
	def t(line:str) -> str:
		return (((self.A(line) @ self.palatalization @ self.multi_char @ self.sing_char).optimize()).stringify(token_type="utf8"))
