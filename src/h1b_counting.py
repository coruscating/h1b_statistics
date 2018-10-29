from __future__ import division
import sys
import math
import traceback

# October 28-29, 2018, Helena Zhang
# written and tested with Python 2.7.10

# this script takes in a CSV file and outputs two files, top_10_occupations.txt and top_10_states.txt. Check README.md for more information.

# it does not check whether the CSV is malformed. For example, if someone puts "software engineer; applications" as an occupation, that will break the current code. This can easily be fixed by 

inputfile=sys.argv[1]
statefile=sys.argv[2]
occupationfile=sys.argv[3]

# We are looking for the following fields:
# CASE_STATUS: need CERTIFIED (case-insensitive). If application is not certified, skip it.
# WORKSITE_STATE: for top states
# SOC_NAME: occupation name for top occupations

# If the field name needs to be changed (while the rest of the conditions remain the same), change below:

# Possible aliases for the three fields we care about are listed below. If your dataset has a different name, add it to the corresponding list.
statusnames=["CASE_STATUS","STATUS"]
statenames=["WORKSITE_STATE", "LCA_CASE_WORKLOC1_STATE"]
jobnames=["SOC_NAME","LCA_CASE_SOC_NAME"]

fields=[statusnames, statenames, jobnames]

states={}
jobs={}

# reads H1B file into array, gets array of top states and occupations
def read_h1bfile():
    try:
        with open(inputfile) as f:

            # get first line, which should be the field
            fieldline=f.readline().split(";")
            fieldindices=[]
            for field in fields:
                for alias in field:
                    if alias in fieldline:
                        fieldindices.append(fieldline.index(alias))
                        break
            if (len(fieldindices) != 3):
                print "Didn't find all three fields, exiting!"
                sys.exit()
            for l in f: # this handles large files better than readlines()
                l2=l.split(";")
                # if not certified we don't care at all, skip
                if(l2[fieldindices[0]].upper()!="CERTIFIED"):
                    continue
                
                lstate=l2[fieldindices[1]]
                if lstate in states:
                    states[lstate]+=1
                else:
                    states[lstate]=1
                
                # remove quotes
                ljob=l2[fieldindices[2]].strip('"')
                if ljob in jobs:
                    jobs[ljob]+=1
                else:
                    jobs[ljob]=1
        return [states, jobs]
    except:
        print traceback.format_exc()
        #print "Error: can't open input file %s, exiting!" %(inputfile)
        sys.exit()

# writes top-10 files given type of (for column name), data dictionaries, and 
def write_topfile(filetype, filename, datadict):
    try:
        total=sum(datadict.values()) # total number of certified cases, should be the same in both cases
        fo=open(filename, "w")
        fo.write("TOP_%s;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n" %(filetype))
        for i in range(0,10):
            # this should give us the highest, alphabetically by key (to break ties)
            maxkey=max(sorted(datadict), key=datadict.get)
            # want to round percentages blindly (.05 always -> .1)
            fo.write("%s;%d;%.1f%%\n" %(maxkey, datadict[maxkey], math.floor(1000*datadict[maxkey]/total+0.5)/10))
            datadict.pop(maxkey)
            if len(datadict)==0: # there are less than 10 entries
                break
        fo.close()
    except:
        print traceback.format_exc()
        sys.exit()

# main block

try:
    [states, jobs]=read_h1bfile()
    write_topfile("OCCUPATIONS", occupationfile, states)
    write_topfile("STATES", statefile, jobs)

except:
    print traceback.format_exc()
    #print "Error: can't open input file %s, exiting!" %(inputfile)
    sys.exit()