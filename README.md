# BinaryMarkovChain
One script will generate a binary sequence according  to some probabilistic rule. The other will create statistics and try to guess those rules. 


Run `python3 genseq.py` to generate a new file called sample2.txt.

Then run `python3 seqlib.py` to print statistics about this file.

To edit the contexts generating the sequence, change the following dict on `genseq.py`

```python
contexts = {'0': .3, '10': .4, '11': .7}
```

Those probabilities represent p(0| context) e.g. in the example p(0|0) = 0,3 and p(0|10) = 0,4
