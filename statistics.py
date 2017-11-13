from __future__ import division
import regex as re
import argparse
import itertools
import math

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

    down_count = (len([1 for match in re.findall(re.compile(context[::-1]), s[:-1], overlapped=True)]))

    if (up_count == 0):
        return 0
    #print("p"+context+"+"+char+" : "+str(up_count / down_count))
    return up_count / down_count

def suffix(context_tree,parent):
    sufx=False
    for context in context_tree:
        if context.endswith(parent):
            sufx=True
    return sufx




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

        k =math.ceil(math.log(len(s),2))


        # print(s)
        # CONTEXT IS RECEIVED ON CONDITIONAL PROBABILITY NOTATION
        # i.e. THE OPPOSITE AS IS WRITTEN IN THE STRING
        # returns max likelihood estimation of char given context in a sequence s

        # Now let's use the context algorithm

        context_tree = {}
        candidates ={}
        #  k-1 level
        candidate_list = ["".join(seq) for seq in itertools.product("01", repeat=k-1)]
        candidates = dict([(x,x) for x in candidate_list])
        while (len(candidates)>0):
            ncandidates ={}
            for context in candidates.keys():
                temp = 0

                # Checking for context
                for a in ["0", "1"]:
                    for b in ["0", "1"]:
                        temp = max(temp, abs(p(a, context, s) - p(a, context + b, s)))

                parent=context[:-1]

                if (temp > eps and height> len(context)) :
                    if (not context in context_tree):
                        context_tree["0"+context]="0"+context
                        context_tree["1"+context]="1"+context
                    if (parent in ncandidates):
                        del ncandidates[parent]
                        # adding my brother to context
                        if(context[-1]=='0'):
                            context_tree["1"+parent]="1"+parent
                        else:
                            context_tree["0"+parent]="0"+parent


                else:
                    if(not suffix(context_tree.keys(),parent) and len(context)>1):
                        if (not parent in ncandidates):
                            ncandidates[parent]=parent

                    else:
                        if (not context in context_tree and height >=len(context)):
                            context_tree[context]=context


            candidates = ncandidates
        print(list(context_tree))
        print("Max Likelihood:")

        for context in context_tree:
        	print("P(0|" + context[::-1] + ")", p("0", context[::-1], s))
