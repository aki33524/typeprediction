"""
python extract_properties.py mappingbased_objects_ja.ttl.bz2
"""
import sys
import bz2

entities = set()
with bz2.BZ2File(sys.argv[1]) as f:
	for l in f.readlines()[1:-1]:
		s, p, o = l.split()[:-1]
		entities.add(p[1:-1])

print len(entities)
for v in sorted(entities):
	print v