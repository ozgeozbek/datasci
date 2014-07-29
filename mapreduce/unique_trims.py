import MapReduce
import sys

__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
# Reads a json with tuples sequence_id and nucleotide, trims last 10 characters of the nucleotide and maps each sequence_id to nucleotides.
#  Reducer then only emits the key which is the nucleotide -- cannot be dupe due to being key in the list.

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: nucleotide -- this will be dupe, so keep it as a key
    # value: sequence_id --this is unique so make it value
    key = record[1][:-10]
    value = record[0]
    mr.emit_intermediate(key,value)

def reducer(key, list_of_values):
    # key: nucleotide
    # value: list of sequence_ids
    #emitting key itself would be sufficient to get rid of duped nucleotides
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
