from collections import defaultdict
import MapReduce
import sys

__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
# Matrix multiplication for sparse matrices.
# Length of each matrix is hardcoded as the matrix is a sparse matrix.

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
# value is ("A", i, j, a_ij) or ("B", j, k, b_jk)
# make [1] the key, remaining the values 

    if record[0] == "a":
        i = record[1]
        j = record[2]
        a_ij = record[3]
        for k in range(0,5):
            mr.emit_intermediate((i, k), ("a", j, a_ij))
    else:
        j = record[1]
        k = record[2]
        b_jk = record[3]
        for i in range(0,5):
        	mr.emit_intermediate((i, k), ("b", j, b_jk))
def reducer(key, list_of_values):
	#key is (i, k)
    #values is a list of ("a", j, a_ij) and ("b", j, b_jk)
    row=key[0]
    col=key[1]
    hash_A=defaultdict(int)
    hash_B=defaultdict(int)
    for item in list_of_values:
    	if item[0] == "a":
    		hash_A[item[1]]=item[2]
    	else:
    		hash_B[item[1]]=item[2]
    result = 0
    for j in range(0,5):
        result += hash_A[j] * hash_B[j]
    mr.emit((row,col, result))
	
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
