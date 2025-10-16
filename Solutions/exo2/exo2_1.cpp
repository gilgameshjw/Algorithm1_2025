#include <bits/stdc++.h>
using namespace std;

const int MIN = 2147483647;
const int MAX = -2147483648;
int k = 0;
void badSort(vector<int> &v) {
    int n = (int)v.size();
    for (int i = 0; i < n / 2; ++i) {
        int start = i, end = n - 1 - i;

        int mn = v[start], mn_pos = start;
        int mx = v[start], mx_pos = start;


        for (int j = start; j <= end; ++j) {
            ++k; 
			if (v[j] < mn) { 
				mn = v[j]; mn_pos = j; 
				}
            ++k; 
			if (v[j] > mx) { 
				mx = v[j]; mx_pos = j; 
				}
        }

        if (mn_pos != start){
			swap(v[start], v[mn_pos]);
			}
        if (mx_pos == start){
        	mx_pos = mn_pos;
		} 

        if (mx_pos != end) {
			swap(v[mx_pos], v[end]);
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
	cout << "\n" << k;
}
int main(){
	int t = 1;
	while(t--){
		solve();
	}
}

	