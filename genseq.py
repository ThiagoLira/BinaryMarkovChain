from __future__ import division
import random
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("configfile", help="Path to configuration file.",
    default="config/treeparams", nargs="?")
configfile = parser.parse_args().configfile

#load json parameters
with open(configfile) as params_file:
    params = json.load(params_file)
ntrees=len(params['trees'])
nsamples=params['nsamples']
ssample=params['sizesample']

print('******Generating '+str(nsamples)+ ' samples for ' + str(ntrees)+' trees******')

for t in range(0,ntrees):

    #create output directory if it does not exist.
    outdir = params['trees'][t]['outdir']
    os.makedirs("samples/"+outdir, exist_ok=True)

    # initial sequence
    iniseq = params['trees'][t]['iniseq']

    # probability of 0 given contexts
    contexts = params['trees'][t]['contexts']
    print(contexts)
    #create nsamples
    for ns in range(0, nsamples):
        # create file or overwrites it
        f = open("samples/"+outdir+"/t"+str(t)+"sample"+str(ns)+".sample", "w+")

        # we start with the initial conditions
        s = iniseq

        # we begin with 2 characters already written on the string
        count = len(s)

        # Simulate Markov Chain!
        while (count < ssample + len(iniseq)):
            rand = random.uniform(0, 1)
            present_context = ""
            i=1
            while (present_context not in contexts):                
                present_context = present_context+s[-i]
                i = i + 1

            if (rand < contexts[present_context]):
                s = s + "0"
            else:
                s = s + "1"
            count = count + 1
        f.write(s)
        f.close()
print('--------Successful. See the samples in the files *.sample--------')
