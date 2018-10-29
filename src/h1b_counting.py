from __future__ import division
import sys
import math
import traceback

# October 28-29, 2018, Helena Zhang
# written and tested in Python 2.7.10

# This script takes in a CSV file and outputs two files, top_10_occupations.txt and top_10_states.txt.
# Check README.md for more information.

############################################
# EDITABLE PARAMETERS
#
# by default, program will generate top 10 rankings. To change the number, edit below:
numrankings=10

# Possible aliases for the three fields we care about are listed below.
# If your dataset has a different column name for one of the fields, add it to the corresponding list.

statusnames=["CASE_STATUS","STATUS"]
statenames=["WORKSITE_STATE", "LCA_CASE_WORKLOC1_STATE"]
jobnames=["SOC_NAME","LCA_CASE_SOC_NAME"]

# END OF EDITABLE PARAMETERS
############################################


inputfile=sys.argv[1]
statefile=sys.argv[2]
occupationfile=sys.argv[3]

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

                # if not certified we don't care at all, skip--EDIT THIS if you want to check for other values
                if(l2[fieldindices[0]].upper()!="CERTIFIED"):
                    continue
                
                # add state to the dictionary as a key if it doesn't exist, or increment value of existing key if it does
                lstate=l2[fieldindices[1]]
                if lstate in states:
                    states[lstate]+=1
                else:
                    states[lstate]=1
                
                # do the same for occupations, and remove quotes
                ljob=l2[fieldindices[2]].strip('"')
                if ljob in jobs:
                    jobs[ljob]+=1
                else:
                    jobs[ljob]=1
        return [states, jobs]
    except:
        print traceback.format_exc()
        sys.exit()

# writes top-10 files given type (for column name), output file name, and data dictionary
def write_topfile(filetype, filename, datadict):
    try:
        total=sum(datadict.values()) # total number of certified cases, should be the same in both cases
        fo=open(filename, "w")
        fo.write("TOP_%s;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n" %(filetype))
        for i in range(numrankings):

            # this should give us the highest, alphabetically by key (to break ties)
            maxkey=max(sorted(datadict), key=datadict.get)

            # want to round percentages blindly (.05 always -> .1)
            fo.write("%s;%d;%.1f%%\n" %(maxkey, datadict[maxkey], math.floor(1000*datadict[maxkey]/total+0.5)/10))

            # remove this key from the dictionary
            datadict.pop(maxkey)
            if len(datadict)==0: # there are less than 10 entries, we're done
                break
        fo.close()
        return 0
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
    sys.exit()