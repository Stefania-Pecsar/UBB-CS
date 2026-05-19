// program cu erori in limbajul original si MLP

#include <iostream>
using namespace std;

int main() {
    int a // Eroare: lipseste punct și virgula(final de rand)
    int int; // Eroare: cuvânt cheie folosit ca identificator

    cout << "Introduceti un numar intreg: ";
    cin >> a;

    cout << "Suma este: ";
    cout << (a + int); // Eroare: identificatorul "int" nu este valid

    return 0;
}