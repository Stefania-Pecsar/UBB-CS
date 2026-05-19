// program cu erori in MLP, dar care NU sunt erori si in limbajul C++

#include <iostream>
using namespace std;

int main() {
    int a, b; // Eroare în MLP - fiecare declarație trebuie să fie pe o linie separată
    int valori[10]; // Eroare în MLP - NU se permite declararea de vectori

    cout << "Introdu 2 numere intregi: ";
    cin >> valori[0] >> valori[1]; // Eroare în MLP - operatorul de citire pentru mai multe variabile

    cout << "Suma numerelor este: " << valori[0] + valori[1]; // Eroare în MLP - numele variabilei NU este acceptat + NU se pot afisa mai multe

    return 0;
}