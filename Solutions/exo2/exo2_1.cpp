#include <bits/stdc++.h>
using namespace std;

const int MAX = 200'007;
const int MOD = 1'000'000'007;

void badSort(vector<int> &v){
	for(int i = 0; i < v.size(); i++){
		for(int j = 0; j < v.size(); j++){
			if(v[i] < v[j]){
				swap(v[i], v[j]);
			}
		}
	}
}

void solve() {
	int n;
	cin >> n;
	vector<int> v(n);
	for(int i = 0; i < n; i++){
		cin >> v[i];
	}
	badSort(v);
	for(int i : v){
		cout << i << ' ';
	}
}
int main(){
	int t = 1;
	while(t--){
		solve();
	}
}

	