import MapReduce
import sys

__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
# Implementation of a natural relational join using MapReduce.
# Mapper uses the order id as the key and maps all related data from both table as one element.
# Reducer then adds the tuples together and creates a flat list

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
# [0] is the name of the table, [1] is the key, remaining are attributes
# make [1] the key, remaining the values 
	key=record[1]
	mr.emit_intermediate(key, record)
def reducer(key, list_of_values):
	for i in range(1,len(list_of_values)):
		tmp_join=[]
		tmp_join.append(list_of_values[0])
		tmp_join.append(list_of_values[i])
		values=sum(tmp_join, [])#used to make a flat list, otherwise the output is a list of two lists.
		mr.emit(values)
	
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
