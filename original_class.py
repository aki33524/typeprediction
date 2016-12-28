"""
python extract_entities.py classes.txt instance_types_ja.ttl.bz2 entities.txt
"""
import re
import sys
import bz2

RESOURCE_PATTERN = re.compile('<http://.*dbpedia\.org/resource/(.*)>')

ctoi = {}
with open(sys.argv[1]) as f:
	N = int(f.readline())
	for i in range(N):
		s = f.readline()[:-1]
		ctoi[s] = i

d = {}
with bz2.BZ2File(sys.argv[2]) as f:
	for l in f.readlines()[1:-1]:
		s, p, o = l.split()[:-1]
		sm = RESOURCE_PATTERN.match(s)
		assert sm is not None
		d[sm.group(1)] = ctoi[o[1:-1]]

with open(sys.argv[3]) as f:
	N = int(f.readline())
	print N
	for i in range(N):
		s = f.readline()[:-1]
		if s in d:
			print d[s]
		else:
			print -1