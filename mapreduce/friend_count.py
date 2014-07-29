import MapReduce
import sys

__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
# Counts the number of friends a person has. Input data is in the format of a tuple with pairs of names.

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: personA
    # value: personB
    key = record[0]
    value = record[1]
    mr.emit_intermediate(key, 1)

def reducer(key, list_of_values):
    # key: person
    # value: 1 for each occurrence of a friend
    total = 0
    for v in list_of_values:
      total += v
    mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
