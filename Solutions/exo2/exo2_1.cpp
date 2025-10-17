#include <bits/stdc++.h>
using namespace std;

const int MIN = 2147483647;
const int MAX = -2147483648;

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
	int mid = l + (r - l) / 2;
	
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
			if (v[j] < mn) { 
				mn = v[j]; mn_pos = j; 
			}
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

void merge(vector<int> &v, int l, int m, int r, vector<int> &tmp){
	int i = l;
	int j = m + 1;
	int k = l;
	if(v[m] <= v[m + 1]){
		return;
	}
	while(i <= m && j <= r){
		if(v[i] <= v[j]){
			tmp[k] = v[i];
			i++;
		}
		else{
			tmp[k] = v[j];
			j++;
		}
		k++;
	}
	while(i <= m){
		tmp[k] = v[i];
		i++;
		k++;
	}
	while(j <= r){
		tmp[k] = v[j];
		j++;
		k++;
	}
	for(int t = l; t <= r; t++){
		v[t] = tmp[t]; 
	}
}

void mergeSort(vector<int> &v, int l, int r, vector<int> &tmp){
	if(l >= r){
		return;
	}
	int m = l + (r - l) / 2;
	mergeSort(v, l, m, tmp);
	mergeSort(v, m + 1, r, tmp);
	merge(v, l, m, r, tmp);
}

void solve() {
	int n;
	cin >> n;
	vector<int> v(n);
	vector<int> tmp(n);
	for(int i = 0; i < n; i++){
		cin >> v[i];
	}
	mergeSort(v, 0, v.size() - 1, tmp);
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

	