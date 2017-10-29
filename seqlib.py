from __future__ import division
import regex as re
import itertools

# Input file is a txt with a single string of 0s and 1s
f = open('sample2.txt', 'r')
s = f.read()

# Algorithm Parameters
context_tree_size = 5
delta = .05

# CONTEXT IS RECEIVED ON CONDITIONAL PROBABILITY NOTATION
# i.e. THE OPPOSITE AS IS WRITTEN IN THE STRING
# returns max likelihood estimation of char given context in a sequence s
def p(char, context, s):


    up_count = (len([1 for match in re.findall(re.compile(context[::-1] + char ), s, overlapped=True)]))

    # I have no idea why s[:-2] works. It should be -1
    down_count = (len([1 for match in re.findall(re.compile(context[::-1]), s[:-2], overlapped=True)]))

    if (up_count == 0):
        return 0

    return up_count / down_count


# Now let's use the context algorithm

context_tree = []

# first level
candidate_contexts = ["0", "1"]

for i in range(1, context_tree_size):

    discarted = []

    for context in candidate_contexts:

        temp = -10000

        for a in ["0", "1"]:
            for b in ["0", "1"]:

                temp = max(temp, abs(p(a, context, s) - p(a, context + b, s)))

        if (delta < temp):
            print (context + ' is NOT a context.')
            discarted.append(context)
        else:
            print (context + ' is a context.')
            # this should not happen
            if context not in context_tree:
                context_tree.append(context)

    # If this is not a context, then we append one more character and iterate again
    # e.g. if 1 is not a context, we have as candidates 10 and 11 for the next iteration
    # if 0 is a context we don't even test 01 and 00
    candidate_contexts = []
    for context in discarted:
        candidate_contexts = candidate_contexts + [context + "".join(seq) for seq in itertools.product("01", repeat=1)]

# Print final context tree
print(context_tree)


for context in context_tree:
    print("P(0|" + context + ")", p("0", context, s))


