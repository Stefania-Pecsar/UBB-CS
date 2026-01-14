#include <iostream>
using namespace std;
int main()
{
    int n;
    cout << "Introdu numarul de elemente: ";
    cin >> n;
    int sum = 0;
    int i = 0;
    while (i < n)
    {
        int x;
        cout << "Introdu element: ";
        cin >> x;
        sum = sum + x;
        i = i + 1;
    }
    cout << "Suma numerelor este: ";
    cout << sum;
}