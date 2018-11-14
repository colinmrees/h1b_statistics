#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 20:23:08 2018

@author: Colin M Rees
"""

import sys
import time
import getopt

import h1b_tally
    
def main( argv ):
    
    #default command line arguments
    benchmark=False
    infilename = 'input/h1b_input.csv'
    outfile1name = 'output/top_10_occupations.txt'
    outfile2name = 'output/top_10_states.txt'
    
    #read command line arguments for input file, output files and optional benchmarking
    try:
        opts, args = getopt.getopt(argv,"hi:o1:o2:b")
    except getopt.GetoptError:
        print( 'h1b_certification.py -i <inputfilepath> -o <outputfilepath>' )
        sys.exit(0)
    for opt, arg in opts:
        if ( opt == '-h' ):
            print( 'h1b_certification.py -i <inputfilepath> -o1 <joboutputfilepath> -o2 <stateoutputfilepath> [-b]' )
            sys.exit(0)
        elif ( opt == '-i' ):
            infilename = arg
        elif ( opt == '-o1' ):
            outfile1name = arg
        elif ( opt == '-o2' ):
            outfile2name = arg
        elif ( opt == '-b' ):
            benchmark = True
    
    #record start time for optimization benchmarking
    if( benchmark ):
        startTime = time.process_time()
    
    #open input and output files
    try:
        infile=open(infilename, 'r', encoding="utf8")
    except FileNotFoundError:
        print("No Valid Input File: " + infilename)
        exit(0)
    outfile1=open(outfile1name, 'w+')
    outfile2=open(outfile2name, 'w+')
    
    #first line of input file should contain field headers
    headers = infile.readline().rstrip().split(';')
    
    #Determine field indicies of relevent fields, Job title, Case status, and Employment state
    try:
        iJobName = headers.index('SOC_NAME')       #iJobName = headers.index('LCA_CASE_SOC_NAME')
        iStatus = headers.index('CASE_STATUS')     #iStatus = headers.index('STATUS')
        iState = headers.index('WORKSITE_STATE')    #iState = headers.index('LCA_CASE_WORKLOC1_STATE')
    except ValueError:
        print("Invalid Data Format. Check File Headings.")
        exit(0)
        
    
    # Create dict objects enumerating the number of applicants certified in each
    # state and for each job title, and the total number of certified applicants
    (jobCounts, stateCounts, totalCertified) = h1b_tally.tally( infile.readlines(), iStatus, iJobName, iState ) 
    
    if( benchmark ):
        sys.stderr.write( "Tally Complete: " + str(time.process_time() - startTime) + "\n" )
    
    # Sort both dicts. First decending numerically by count, then Ascending alphabetically by Catagory.
    # First 10 elements of the sorted list are obtained
    topJobs = sorted(jobCounts.items(), key=lambda x: (-x[1], x[0]) )[:10]
    topStates = sorted(stateCounts.items(), key=lambda x: (-x[1], x[0]) )[:10]     
    
    # Calculate percentage of certified in each catagory and
    # write sorted lists to output files
    outfile1.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
    for x in topJobs:
        outfile1.write( "{:s};{:d};{:.1f}%\n".format(x[0], x[1], x[1]/totalCertified*100) )
    
    
    outfile2.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
    for x in topStates:
        outfile2.write( "{:s};{:d};{:.1f}%\n".format(x[0], x[1], x[1]/totalCertified*100) )
    
    if( benchmark ):
        sys.stderr.write( "Postprocessing Complete: " + str(time.process_time() - startTime) + "\n" )
    
    infile.close()
    outfile1.close()
    outfile2.close()



if __name__ == "__main__":
    main(sys.argv[1:])