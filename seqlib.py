from __future__ import division
import regex as re
import argparse
import itertools

import json

# Read command line argument - configuration file
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

eps = params['eps']



def p(char, context, s):
    up_count = (len([1 for match in re.findall(re.compile(context[::-1] + char ), s, overlapped=True)]))

    # I have no idea why s[:-2] works. It should be -1
    down_count = (len([1 for match in re.findall(re.compile(context[::-1]), s[:-1], overlapped=True)]))

    if (up_count == 0):
        return 0
    #print('----- '+char+"|"+context+" = "+str(up_count)+"/"+str(down_count)+ "valor="+str(up_count / down_count) )
    return up_count / down_count


for t in range(0,ntrees):
    outdir = params["trees"][t]["outdir"]
    for ns in range(0,nsamples):
        # Input file is a txt with a single string of 0s and 1s
        print('*************************************************************')
        print("Statistics for sample: t"+str(t)+"sample"+str(ns)+".sample")
        f = open("samples/"+outdir+"/t"+str(t)+"sample"+str(ns)+".sample", "r")
        s = f.read().rstrip()

        # Algorithm Parameters
        height=params['trees'][t]['height']
        context_tree_size = height + 1

        # CONTEXT IS RECEIVED ON CONDITIONAL PROBABILITY NOTATION
        # i.e. THE OPPOSITE AS IS WRITTEN IN THE STRING
        # returns max likelihood estimation of char given context in a sequence s

        # Now let's use the context algorithm

        context_tree = []

        # first level
        candidate_contexts = ["0", "1"]

        for i in range(1, context_tree_size):

            discarted = []

            for context in candidate_contexts:

                temp = 0

                for a in ["0", "1"]:
                    for b in ["0", "1"]:


                        temp = max(temp, abs(p(a, context, s) - p(a, context + b, s)))


                print(temp, context)

                if (eps > temp):
                    # if we are at the last level of the tree we want to generate
                    # we just take this non context and add it's children to the tree
                    if len(context)==height-1:
                        context_tree.append(context + "0")
                        context_tree.append(context + "1")
                    # if not then we will try to check if his children are contexts
                    else:

                        discarted.append(context)
                else:
                    # not much to do here
                    if context not in context_tree:
                        context_tree.append(context)

            # If this is not a context, then we append one more character and iterate again
            # e.g. if 1 is not a context, we have as candidates 10 and 11 for the next iteration
            # if 0 is a context we don't even test 01 and 00
            candidate_contexts = []

            #create the next tree level
            for context in discarted:
                candidate_contexts.append(context + "0")
                candidate_contexts.append(context + "1")


        # Print final context tree
        print("Final Context Tree: ")
        print(context_tree)

        # Max. Likelihood of transitions
        print("Max Likelihood:")
        for context in context_tree:
            print("P(0|" + context + ")", p("0", context, s))
