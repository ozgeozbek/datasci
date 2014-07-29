import MapReduce
import sys

__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
# Mapper creates a (key, value) pair in the form of (word, document_id)
# Reducer then returns the unique list of document ids for each word

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
	value=record[0]
	words=record[1].split()
	for w in words:
		key=w
		mr.emit_intermediate(w, value)
def reducer(key, list_of_values):
	#key: word
	#value: document ID that contains the word
	temp_vals=[] #to hold the unique list of document_ids, otherwise the resulting list contains duplicate document_ids
	for v in list_of_values:
		if v not in temp_vals:
			temp_vals.append(v)
	mr.emit((key, temp_vals))
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
