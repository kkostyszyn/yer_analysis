# Analysis of yers in Polish morphology

Using Unimorph data, extracting all instances of yer in Polish morphological paradigms, to see what generalizations can be made. 

Where possible, transcriptions are taken from wikipron. Otherwise, IPA transcriptions are made via transducers (built in pynini), in alignment with wikipron standards for consistency.

To generate data from scratch, run:
`python gen_data.py`

To generate data using pre-existing translations, run:
`python gen_data.py data/SAVE.txt` 
