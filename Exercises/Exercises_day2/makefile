#######################################################################	

all: normalize_vec.cpp.exec dot_prod.exec

#######################################################################	

## Example 1
normalize_vec.cpp.exec : normalize_vec.cpp
	g++ normalize_vec.cpp -fopenmp -o normalize_vec.cpp.exec

dot_prod.exec : dot_prod.cpp
	g++ dot_prod.cpp -fopenmp -o dot_prod.exec

clean:
	rm -f *.exec
