# encoding:utf-8

"""
python tfidf.py original_class.txt graph.txt classes.txt
"""

import sys
import math

def cos_similarity(vec1, vec2):
	s = 0
	for node in set(vec1) & set(vec2):
		s += vec1[node] * vec2[node]

	d1 = 0
	for x in vec1.values():
		d1 += x ** 2
	d2 = 0
	for x in vec2.values():
		d2 += x ** 2

	d1 = d1 ** 0.5
	d2 = d2 ** 0.5

	return s / d1 / d2

classes = []
ctoi = {}
with open(sys.argv[1]) as f:
	N = int(f.readline())
	for u in range(N):
		c = int(f.readline())
		classes.append(c)
		if c not in ctoi:
			ctoi[c] = []
		ctoi[c].append(u)

idfs = {}
tfs = []
with open(sys.argv[2]) as f:
	N = int(f.readline())
	for u in range(N):
		d = {}
		m = int(f.readline())
		for i in range(m):
			rev, p, to = map(int, f.readline().split())
			# if classes[to] < 0:
			# 	continue
			# node = (rev, p, classes[to])
			node = (rev, p)
			if node not in d:
				d[node] = 0
			d[node] += 1
		for node in d:
			if node not in idfs:
				idfs[node] = 0
			idfs[node] += 1
		tfs.append(d)

class_idf = {}
class_tfs = {}
for c, resources in ctoi.items():
	if c < 0:
		continue
	d = {}
	for u in resources:
		for node, count in tfs[u].items():
			if node not in d:
				d[node] = 0
			d[node] += count
	for node in d:
		if node not in class_idf:
			class_idf[node] = 0
		class_idf[node] += 1
	s = 0
	for count in d.values():
		s += count
	for node in d:
		d[node] = d[node] / float(s)
	class_tfs[c] = d;

for d in tfs:
	s = 0
	for ndoe, count in d.items():
		s += count
	for node in d:
		d[node] = d[node] / float(s)

for node in idfs:
	idfs[node] = -math.log(idfs[node]/float(N))

for node in class_idf:
	class_idf[node] = -math.log(class_idf[node]/float(len(classes)))

class_name = []
with open(sys.argv[3]) as f:
	C = int(f.readline())
	for i in range(C):
		c = f.readline()[:-1]
		class_name.append(c)

while True:
	# 339140 日本
	# 70522 アメリカ合衆国
	idx = int(raw_input(">>>"))

	vec1 = {}
	for node, v in tfs[idx].items():
		vec1[node] = v * idfs[node]

	l = []
	for c, tf in class_tfs.items():
		vec2 = {}
		for node, v in tf.items():
			vec2[node] = v * class_idf[node]
		l.append((cos_similarity(vec1, vec2), c))
	l.sort()
	for p in l:
		print p[0], class_name[p[1]]
	print "Ans: ", class_name[classes[idx]]
