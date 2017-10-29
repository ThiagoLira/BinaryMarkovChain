from __future__ import division
import random

# create file or overwrites it
f = open("sample2.txt", "w+")

# probability of 0 given contexts
contexts = {'0': .3, '10': .4, '11': .7}

random.seed(1337)

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
while (count < 100000 + 2):

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