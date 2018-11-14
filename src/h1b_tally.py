# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 20:23:08 2018

@author: Colin M Rees
"""

# increments the count in the tally for the  given catagory
# if catagory is not found in the tally, the catagory is appended and set to 1
def increment( tally, catagory ):
    if ( catagory in tally ):
        tally[catagory] += 1
    else:
        tally[catagory] = 1

# given a list of records, tallies the number of records for each unique entry
# in the field indexes iJobName and iState where the entry in the field index 
# iStatus is 'CERTIFIED'
# Returns dict objects enumerating both tallies, and the total count tallied
def tally( records, iStatus, iJobName, iState ):
              
    #running total of certified applicents for calculating percentages
    totalCertified= 0
    
    #Tally of certified candidates in each catagory. Storing in hash tables for optimized lookup speed
    stateCounts = {}
    jobCounts = {}
    
    for line in records:
        try:
            record = line.rstrip().split(';')
        except TypeError:
            #Invalid Data Format - Ignore and skip record
            continue
        except ValueError:
            #Invalid Data Format - Ignore and skip record
            continue
        
        #Ignore records which were not certified. Tally Certified records
        if( record[iStatus] == "CERTIFIED" ):
            totalCertified += 1
            
            increment( stateCounts, record[iState].strip('"') )
            increment( jobCounts, record[iJobName].strip('"') )
    
    return (jobCounts, stateCounts, totalCertified)