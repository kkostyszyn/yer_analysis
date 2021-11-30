import sys
from states import State, Feature

def main(features = False, language = Fale):
	#first, build feature chart 
	if not features:
		print("Missing feature descriptions.")
		return None
	
	#then build language as a map of feaures 
	if not language:
		print("Missing language inventory data."
		return None
	
	#Start generating states for minimal feature space by removing all features where there is no
	#contrast in +/- values (where, for dependent features, 0 == -). 
	#State 0 will be the initial stripped state.
	states = {}
	
	#Then, looking at the remaining features and symbols, start removing a single feature.
	#If the resulting state still has all features contrasting, keep it.
	#If the resulting state is identical to another state, remove it. 
	#All previous states are retained. If no more features can be removed, mark as 'done'.
	

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[0], sys.argv[1])
	else:
		main()