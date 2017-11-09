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

# load json parameters
with open(configfile) as params_file:
    params = json.load(params_file)
ntrees = len(params['trees'])
nsamples = params['nsamples']
ssample = params['sizesample']

eps = params['eps']


def generate_candidates(size):
    # Generate candidates on last level of context tree
    return ["".join(seq) for seq in itertools.product("01", repeat=size)]


def generate_next_level(removed_contexts):
    # for each string which is not a context,
    # we remove it's last digit (inverted notation) and create
    # a new list of context candidates
    return list((map((lambda s: s[:-1]), removed_contexts)))


def p(char, context, s):
    # calculate max likelihood of P (char | context),
    # context is GIVEN in inverted order!!!!
    up_count = (len([1 for match in re.findall(re.compile(context[::-1] + char ), s, overlapped=True)]))

    down_count = (len([1 for match in re.findall(re.compile(context[::-1]), s[:-1], overlapped=True)]))

    if (up_count == 0):
        return 0
    #print('----- '+char+"|"+context+" = "+str(up_count)+"/"+str(down_count)+ "valor="+str(up_count / down_count) )
    return up_count / down_count


for t in range(0, ntrees):
    outdir = params["trees"][t]["outdir"]
    for ns in range(0, nsamples):
        # Input file is a txt with a single string of 0s and 1s
        print('*************************************************************')
        print("Statistics for sample: t" + str(t) + "sample" + str(ns)+ ".sample")
        f = open("samples/" + outdir+ "/t" + str(t) +"sample" + str(ns) + ".sample", "r")
        s = f.read().rstrip()

        # Algorithm Parameters
        height=params['trees'][t]['height']
        context_tree_size = height 

        # CONTEXT IS RECEIVED ON CONDITIONAL PROBABILITY NOTATION
        # i.e. THE OPPOSITE AS IS WRITTEN IN THE STRING
        # returns max likelihood estimation of char given context in a sequence s

        # Now let's use the context algorithm

        # we add eligible contexts on that tree
        context_tree = []

        # first level
        candidate_contexts = generate_candidates(context_tree_size)

        for i in range(1, context_tree_size + 1):

            discarted = []

            for context in candidate_contexts:

                temp = 0

                for a in ["0", "1"]:
                    for b in ["0", "1"]:

                        # we are giving the contexts in INVERTED order!
                        temp = max(temp, abs(p(a, context[:-1], s) - p(a, context, s)))

                if (temp < eps):
                    # Prune this level of tree
                    discarted.append(context)
                    #print(context, "is not a context")
                else:
                    context_tree.append(context)

                candidate_contexts = generate_next_level(discarted)

                discarted = []

        # Print final context tree
        print("Final Context Tree: ")
        print(context_tree)

        # Max. Likelihood of transitions
        print("Max Likelihood:")
        for context in context_tree:
            print("P(0|" + context + ")", p("0", context, s))
