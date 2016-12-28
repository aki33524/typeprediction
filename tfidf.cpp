/*
cat data/original_class.txt data/graph.txt data/classes.txt data/entities.txt | ./tfidf 
*/
#include <bits/stdc++.h>
using namespace std;

const int CLASS_NUM = 153;

int N;
vector<vector<int>> classes;
map<int, double> idfs; //node, freq
vector<map<int, double>> tfs; //doc, node, freq
vector<string> class_name, resource_name;
vector<int> class_count(CLASS_NUM);

int node_to_hash(int rev, int p){
	const int R = 2;
	return rev + R * p;
}
void load_original_class(){
	cin >> N;
	classes.resize(N);
	for(int i=0; i<N; i++){
		int c; cin >> c;
		classes[i].resize(c);
		for(int j=0; j<c; j++){
			cin >> classes[i][j];
			class_count[classes[i][j]]++;
		}
	}
}
void load_graph(){
	cin >> N;
	for(int u=0; u<N; u++){
		map<int, double> d;
		int m; cin >> m;
		for(int i=0; i<m; i++){
			bool rev;
			int p, to;
			cin >> rev >> p >> to;
			int h = node_to_hash(rev, p);
			d[h] += 1.0/m;
		}
		for(auto &p: d)
			idfs[p.first] += 1.0/N;
		tfs.push_back(d);
	}
	for(auto p: idfs){
		idfs[p.first] = -log(p.second);
		// cout << idfs[p.first] << endl;
	}
}
void load_class_name(){
	int C; cin >> C;
	class_name.resize(C);
	for(auto &v: class_name)
		cin >> v;
}
void load_resource_name(){
	cin >> N;
	resource_name.resize(N);
	for(auto &v: resource_name)
		cin >> v;
}
void input(){
	load_original_class();
	load_graph();
	load_class_name();
	load_resource_name();
}
double cos_similarity(map<int, double> &vec1, map<int, double> &vec2){
	double s = 0;
	// if(vec1.size() > vec2.size()) swap(vec1, vec2);
	for(auto p: vec1) if(vec2.find(p.first) != vec2.end())
		s += p.second * vec2[p.first];
	
	double d1 = 0, d2 = 0;
	for(auto p: vec1)
		d1 += p.second * p.second;
	for(auto p: vec2)
		d2 += p.second * p.second;

	return s / sqrt(d1) / sqrt(d2);
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);

	cerr << "Input...";
	input();
	cerr << "Done" << endl;

	// 339140 日本
	// 70522 アメリカ合衆国
	// 174186 バラク・オバマ
	int idx1 = 0;
	
	while(true){
		cerr << ">>> "; cin >> idx1;
		if(idx1 >= N){
			cerr << "out of range" << endl;
			continue;
		}

		vector<double> r(CLASS_NUM);
		map<int, double> vec1;
		for(auto p: tfs[idx1]){
			vec1[p.first] = p.second * idfs[p.first];
			// cout << vec1[p.first] << endl;
		}
		for(int idx2=0; idx2<N; idx2++){
			// if(idx1 == idx2) continue;

			map<int, double> vec2;
			for(auto p: tfs[idx2])
				vec2[p.first] = p.second * idfs[p.first];
			// FIXME
			if(vec2.size() == 0)
				continue;
			double x = cos_similarity(vec1, vec2);
			for(auto v: classes[idx2])
				r[v] += x;
		}
		vector<pair<double, int>> l;
		for(int i=0; i<CLASS_NUM; i++){
			if(class_count[i] == 0) continue;
			l.push_back({r[i]/class_count[i], i});
		}
		sort(l.rbegin(), l.rend());

		cout << "----------" << endl;
		for(int i=0; i<l.size(); i++){
			if(l[0].first != l[i].first){
				for(int j=0; j<i; j++){
					auto p = l[j];
					cout << p.first << "\t" <<  class_name[p.second] << endl;
				}
				break;
			}
		}
		cout << "----------" << endl;
		for(auto v: classes[idx1])
			cout << class_name[v] << endl;
		cout << resource_name[idx1] << endl;
	}
	return 0;
}