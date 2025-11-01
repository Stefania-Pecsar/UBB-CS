#include <iostream>
#include<thread>
#include<chrono>
using namespace std;
using namespace std::chrono;

const int N = 10000;
const int P = 8;
const int MAX_VAL = 100000;
int a[N], b[N], c[N], c_secv[N];

void init(int* v, int len)
{
	for (int i = 0;i < len;i++)
	{
		v[i] = rand() % MAX_VAL;
	}
}

void sum(const int* a, const int* b, int len, int *c)
{
	for (int i = 0; i < len;i++) {
		//c[i] = a[i] + b[i];
		c[i] = sqrt(a[i] * a[i]) + b[i] * b[i];
	}
}

void suma(const int* a, const int* b, int* c, int start, int end)
{
	for (int i = start; i < end;i++) {
		//c[i] = a[i] + b[i];
		c[i] = sqrt(a[i] * a[i]) + b[i] * b[i];
	}
}

void start_thr(int* a, int* b, int* c, int* c_secv)
{
	int dim_thr = N / P;
	int r = N % P;
	int start_idx = 0;
	int end_idx = dim_thr;

	thread t[P];


	auto start_time_par = high_resolution_clock::now();

	for (int tid = 0; tid < P;tid++)
	{
		if (r > 0)
		{
			end_idx++;
			r--;
		}

		/*cout << "Tid: " << tid << " start: " << start_idx << " end: " << end_idx << endl;*/

		t[tid] = thread(suma, a, b, c, start_idx, end_idx);

		start_idx = end_idx;
		end_idx += dim_thr;
	}


	for (int tid = 0; tid < P;tid++) {
		t[tid].join();
	}

	auto end_time_par = high_resolution_clock::now();
	duration<double, micro> delta_time_par = end_time_par - start_time_par;

	cout << "Timpul paralel este: " << delta_time_par.count() << " microsecunde" << endl;

	bool ok = true;
	for (int i = 0; i < N; i++)
	{
		if (c[i] != c_secv[i])
		{
			cout << "err at:" << i << " expected: " << c_secv[i] << " got: " << c[i] << endl;
			ok = false;
		}
	}

	if (ok)
	{
		cout << "All ok!\n";
	}
}

int main()
{
	auto start_time = high_resolution_clock::now();
	cout << "Hello thread!" << endl;
	init(a, N);
	init(b, N);

	auto start_time_secv = high_resolution_clock::now();
	sum(a, b, N, c_secv);
	auto end_time_secv = high_resolution_clock::now();
	duration<double, micro> delta_time_secv = end_time_secv - start_time_secv;

	cout << "Timpul secvential este: " << delta_time_secv.count() << " microsecunde" << endl;

	for (int i = 0; i < 5;i++)
	{
		cout << "a: " << a[i] << " b: " << b[i] << " c: "<< c_secv[i]<<endl;
	}

	start_thr(a, b, c, c_secv);

	auto end_time = high_resolution_clock::now();
	duration<double, micro> delta_time = end_time - start_time;

	cout << "Timpul este: " << delta_time.count() << " microsecunde" << endl;

	int* a_dyn = new int[N];
	int* b_dyn = new int[N];
	int* c_dyn = new int[N];

	int* all = new int[N * 3];

	for (int i = 0; i < N; i++)
	{
		a_dyn[i] = a[i];
		b_dyn[i] = b[i];
		all[i] = a[i];
		all[i + N] = b[i];
	}

	start_thr(a_dyn, b_dyn, c_dyn, c_secv);
	start_thr(all, all + N, all + N * 2, c_secv);

	delete[] a_dyn;
	delete[] b_dyn;
	delete[] c_dyn;
	return 0;

	//n linii, m coloane
	//a_ij = i*m + j = i+j*n
	//i=a_ij/m = a_ij % n
	//j = a_ij/n = a_ij % m
}

