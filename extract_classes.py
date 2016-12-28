"""
python extract_entities.py instance_types_ja.ttl.bz2
"""
import re
import sys
import bz2

RESOURCE_PATTERN = re.compile('<http://.*dbpedia\.org/resource/(.*)>')

classes = set()
with bz2.BZ2File(sys.argv[1]) as f:
	for l in f.readlines()[1:-1]:
		s, p, o = l.split()[:-1]

		sm = RESOURCE_PATTERN.match(s)
		assert sm is not None
		classes.add(o[1:-1])

print len(classes)
for v in sorted(classes):
	print v