# Insight Data Engineering Coding Challenge

## Colin M. Rees

This project fulfills the following specifications:

- Use H1B Visa data to determine the 10 most popular occupations, and locations of certified H1B visa applicants.

- Output data files containing the lists of occupations and states, allong with the total number of certified applicants in each catagory and the percentage of total certified applicants in each catagory.

### Usage

The run.sh script will automatically run any file named h1b_input.csv in the input/ directory.
In general the usage syntax is as follows:
python ./src/h1b_certification.py -i <inputfilepath> -o1 <joboutputfilepath> -o2 <stateoutputfilepath> [-b]
The optional -b flag will output the runtime in seconds for benchmarking purposes

### Approach

I developed this solution in Python 3.6. The problem specified that I not use non-standard data structures and database packages such as pandas, therefore the solution utilizes list and dict data structures to optimize run time.

The three relevant fields in the data files for this problem are the Job title, Case status, and Employment state. The field number for each of these fields is extracted from the headers in the first line of the input file and recorded before iterating through the remainder of the input file. Identifying field indicies in this way is tolerant to variation in field order across input files, but is not tolerant to different heading labels across input files. This solution in it's current state expects input files with field headings that are exact matches to those in the sample data file.

The primary method for tabulating the number of certified applicants in each catagory is contained in the h1b_tally.py module. This method utilizes dict data structures which utilizes a hash table for faster lookup. When a new record for a given catagory is counted, if that catagory already exists in the dict, the count is incremented, if it does not, then the catagory is appended to the dict, and the count is set to 1.

The dicts returned by the tally method are then sorted in order to extract the top 10 catagories using the default python Timsort algorithm. The sort key is defined using a lambda expression to specify that the elements be sorted first by count, then by catagory. The key achieves a sort of the counts in decending order by specifying that the negative of the counts be sorted in ascending order.

The python indexing operator will automatically return a smaller list if fewer than 10 catagories exist.

This solution does not utilize multithreading. A sample datafile containing 647852 records was processed using this solution on a single core in 4.32 seconds. 