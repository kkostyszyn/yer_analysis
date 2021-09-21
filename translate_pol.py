import pynini
import functools
import re

A = functools.partial(pynini.acceptor, token_type="utf8")
T = functools.partial(pynini.transducer, input_token_type="utf8", output_token_type="utf8")
epsilon = pynini.epsilon_machine()

#DEFINE POLISH INVENTORY - INPUT VS. OUTPUT

vowels = (A("a") | A("ą") | A("e") | A("ę") | A("i") | A("o") |  A("ó") | A("u") | A("y"))

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

sigma_out = (vowels | cons_out)
sigmaStar = pynini.closure(vowels | cons_in | cons_out | epsilon )


#find all instances of palatalization 
s_pal = (T("si", "ɕi") | T("ś", "ɕ"))
s_palatal = pynini.cdrewrite(s_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
z_pal = (T("zi", "ʑi") | T("ź", "ʑ"))
z_palatal = pynini.cdrewrite(z_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
n_pal = (T("ni", "ɲi") | T("ń", "ɲ"))
n_palatal = pynini.cdrewrite(n_pal, sigmaStar, sigmaStar, sigmaStar).optimize()
k_palatal = pynini.cdrewrite(T("ki", "Ci"), sigmaStar, sigmaStar, sigmaStar).optimize()
g_palatal = pynini.cdrewrite(T("gi", "ɟi"), sigmaStar, sigmaStar, sigmaStar).optimize()
   
palatalization = (s_palatal @ z_palatal @ n_palatal @ k_palatal @ g_palatal).optimize()

#once palatalization is normalized, do 1-to-1 transductions for all other characters
    
#other multi-character tranductions
#dz combined into the z palatalization 
#sz
sz = pynini.cdrewrite(T("sz", "ʃ"), sigmaStar, sigmaStar, sigmaStar).optimize()
#ch    
ch = pynini.cdrewrite(T("ch", "x"), sigmaStar, sigmaStar, sigmaStar).optimize()
#cz
cz = pynini.cdrewrite(T("cz", "tʃ"), sigmaStar, sigmaStar, sigmaStar).optimize()
#rz
rz = pynini.cdrewrite((T("rz", "ʒ") | T("ż", "ʒ")), sigmaStar, sigmaStar, sigmaStar).optimize()
    
multi_char = (sz @ ch @ cz @ rz).optimize()

    
#single characters
#w->v
w = pynini.cdrewrite(T("w", "v"), sigmaStar, sigmaStar, sigmaStar).optimize()
#c->ts
c = pynini.cdrewrite(T("c", "ts"), sigmaStar, sigmaStar, sigmaStar).optimize()
tc = pynini.cdrewrite(T("ć", "t"), sigmaStar, sigmaStar, sigmaStar).optimize()
#h->x
h = pynini.cdrewrite(T("h", "x"), sigmaStar, sigmaStar, sigmaStar).optimize()
#l->w
barred_L = pynini.cdrewrite(T("ł", "w"), sigmaStar, sigmaStar, sigmaStar).optimize()
    
sing_char = (w @ c @ tc @ h @ barred_L).optimize()
    
#to determine the transcription of a single word, barring vowels    
def t(line):
    return (((A(line) @ palatalization @ multi_char @ sing_char).optimize()).stringify(token_type="utf8"))

#translate a list of documents
#previously i attempted to use the t() function here to transcribe w; however,
#this led to a breakdown between functions, and the 'FST is not a string' error
# was raised, no matter at which point I declared the string as an acceptor.
def trans(f):
    data = open(f).readlines()
    
    f = re.split(r'.txt', f)
    o = open(f[0] + "_clusters.txt", "w")
    x = open(f[0] + "_exceptions.txt", "w")
    t = open(f[0] + "_transcriptions.txt", "w")
    d = {}
    
    for line in data:
        try:
            w = re.split(r'\s', line)
            w = (A(w[0]) @ palatalization @ multi_char @ sing_char).optimize()
            w = w.stringify(token_type="utf8")
            w = re.split(r'(a|e|i|o|u|y|ą|ę|ó)', w)
            if w[0] in d:
                d[w[0]] = d[w[0]] + 1
            else:
                d[w[0]] = 1
            t.write(line + " " + str(w) + "\n")
        except:
            x.write(line)
        
    for cl in sorted(d):
        o.write(cl + ": " + str(d[cl]) + "\n")
        
    o.close()
    x.close()
    t.close()
