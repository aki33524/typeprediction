
"""
python extract_entities.py mappingbased_objects_ja.ttl.bz2
"""
import re
import sys
import bz2

RESOURCE_PATTERN = re.compile('<http://.*dbpedia\.org/resource/(.*)>')

entities = set()
with bz2.BZ2File(sys.argv[1]) as f:
	for l in f.readlines()[1:-1]:
		s, p, o = l.split()[:-1]

		sm = RESOURCE_PATTERN.match(s)
		om = RESOURCE_PATTERN.match(o)
		if sm is not None:
			entities.add(sm.group(1))
		if om is not None:
			entities.add(om.group(1))
		
print len(entities)
for v in sorted(entities):
	print v