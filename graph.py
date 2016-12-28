#-*- coding: utf-8 -*-
"""
python graph.py entities.txt properties.txt mappingbased_objects_ja.ttl.bz2
"""

import re
import sys
import bz2

RESOURCE_PATTERN = re.compile('<http://.*dbpedia\.org/resource/(.*)>')

entities = {}
with open(sys.argv[1]) as f:
	N = int(f.readline())
	for i in range(N):
		entities[f.readline()[:-1]] = i

properties = {}
with open(sys.argv[2]) as f:
	M = int(f.readline())
	for i in range(M):
		properties[f.readline()[:-1]] = i

graph = [[] for i in range(N)]
with bz2.BZ2File(sys.argv[3]) as f:
	for l in f.readlines()[1:-1]:
		s, p, o = l.split()[:-1]

		sm = RESOURCE_PATTERN.match(s)
		om = RESOURCE_PATTERN.match(o)

		if sm is None or om is None:
			continue

		si = entities[sm.group(1)]
		oi = entities[om.group(1)]
		pi = properties[p[1:-1]]

		graph[si].append((0, pi, oi))
		graph[oi].append((1, pi, si))
		
print N
for e in graph:
	print len(e)
	for v in e:
		# 逆辺かどうか, property id, entity id
		print v[0], v[1], v[2]
