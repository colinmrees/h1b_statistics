#!/bin/bash
#
# Program Execution Script.
infile='./input/h1b_input.csv'
#infile='./input/H1B_FY_2016.csv'
outfile1='./output/top_10_occupations.txt'
outfile2='./output/top_10_states.txt'
python ./src/h1b_certification.py -i $infile -o1 $outfile1 -o2 $outfile2

