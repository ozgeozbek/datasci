import MapReduce
import sys

__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
# Returns a list of tuples that has 1- person 2- friend where friend is actually not friends with person.
# It returns the symmetrical tuple as well (instead of only showing the asymmetrical tuple) 

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: personA
    # value: personB
    key = record[0]
    value = record[1]
    mr.emit_intermediate((key, value),1)
    mr.emit_intermediate((value, key),1)

def reducer(key, list_of_values):
    # key: persons
    # value: friends
    #if person is a key 
    if len(list_of_values)<2:
    	mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
