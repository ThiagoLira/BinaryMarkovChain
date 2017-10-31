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
    random.seed(1337)

    #create output directory if it does not exist.
    outdir = params['trees'][t]['outdir']
    os.makedirs("samples/"+outdir, exist_ok=True)

    # probability of 0 given contexts
    contexts = params['trees'][t]['contexts']
    #create nsamples
    for ns in range(0, nsamples):
        # create file or overwrites it
        f = open("samples/"+outdir+"/t"+str(t)+"sample"+str(ns)+".sample", "w+")
        #
        # Buffer with last entries in sequence
        # we start with some initial conditions
        s = "01"

        # same initial conditions on file
        f.write("0")
        f.write("1")

        # we begin with 2 characters already written on the string
        count = len(s)

        # Simulate Markov Chain!
        while (count < ssample + 2):

            rand = random.uniform(0, 1)

            present_context = ""

            i = 0
            # go back on sequence until we find something
            # that is a context to generate next character
            while (present_context not in contexts):
                present_context = present_context + s[len(s) -1 - i]
                i = i + 1
            # remove first char from buffer s and add new char
            # our buffer will never have more chars than 2
            if (rand < contexts[present_context]):
                f.write("0")
                s = s[1:] + "0"
            else:
                s = s[1:] + "1"
                f.write("1")

            count = count + 1

        f.close()
print('--------Successful. See the samples in the files *.sample--------')
