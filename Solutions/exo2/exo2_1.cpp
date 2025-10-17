#include <bits/stdc++.h>
using namespace std;

const int MIN = 2147483647;
const int MAX = -2147483648;
int k = 0;

int partition(vector<int> &v, int l, int r){
	int pivot_index =l + rand() % (r - l + 1);
	swap(v[pivot_index], v[r]);
	int pivot = v[r];
	int i = l;
	for(int j = l; j < r; j++){
		if(v[j] < pivot){
			swap(v[i], v[j]);
			i++;
		}
	}
	swap(v[r], v[i]);
	return i;
}
	
int avg_partition(vector<int> &v, int l, int r){
	int down = l;
	int up = r;
	int mid = l + (l + r) / 2;
	int a = v[down];
	int b = v[mid];
	int c = v[up];
	
	if(v[down] > v[mid]){
		swap(v[down], v[mid]);
	}
	if(v[down] > v[up]){
		swap(v[down], v[up]);
	}
	if(v[mid] > v[up]){
		swap(v[mid], v[up]);
	}
	
	swap(v[mid], v[r]);
	int pivot = v[r];
	int i = l;
	for(int j = l; j < r; j++){
		if(v[j] < pivot){
			swap(v[j], v[i]);
			i++;
		}
	}
	swap(v[i], v[r]);
	return i;
}	
	
void quickSort(vector<int> &v, int l, int r){
	if (l >= r){
		return;
	}
	int p = avg_partition(v, l, r);
	quickSort(v, l, p - 1);
	quickSort(v, p + 1, r);
}	
	
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
	quickSort(v, 0, v.size() - 1);
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

	