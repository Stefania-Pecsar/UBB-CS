#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <random>
#include <fstream>
#include <iostream>
#include <vector> 

using namespace std;

vector<int> generateRandomVector(int size)
{
    vector<int> vector(size);
    random_device rd;
    mt19937 gen0(rd());
    uniform_int_distribution<> dis0(1, 9);
    vector[0] = dis0(gen0);

    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 9);
    for (int i = 1; i < size; i++)
    {
        vector[i] = dis(gen);
    }
    return vector;
}

// Functia care salveaza lungimea vectorului pe un rand si pe urmatorul rand continutul vectorului intr-un fisier
void saveVectorToFile(const vector<int>& vectorr, const char* fileName)
{
    FILE* file;
    if (fopen_s(&file, fileName, "w") != 0) {
        cerr << "Eroare la deschiderea fisierului pentru salvare: " << fileName << endl;
        return;
    }
    fprintf(file, "%d\n", vectorr.size());
    for (size_t i = 0; i < vectorr.size(); i++)
    {
        fprintf(file, "%d ", vectorr[i]);
    }
    fclose(file);
}

void createvectors()
{
    // Generare si salvare vectori random in fișiere
    saveVectorToFile(generateRandomVector(16), "C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar1.txt");
    saveVectorToFile(generateRandomVector(16), "C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar2.txt");
}

// Functia care citeste vectorul din fisier (se stie ca pe prima linie in fisier se afla lungimea vectorului)
vector<int> readVectorFromFile(const char* fileName)
{
    ifstream file(fileName);

    if (!file.is_open()) {
        cerr << "Eroare la deschiderea fisierului pentru citire: " << fileName << endl;
        exit(1);
    }

    int size;
    file >> size; 

    if (!file.good()) {
        cerr << "Fisier invalid: nu s-a gasit dimensiunea vectorului." << endl;
        exit(1);
    }

    vector<int> vec(size);

    for (size_t i = 0; i < size; i++) {
        if (!(file >> vec[i])) {
            cerr << "Eroare la citirea elementului " << i << endl;
            exit(1);
        }
    }

    file.close();

    reverse(vec.begin(), vec.end());
    return vec;
}


vector<int> readVectorFromFileManipulated(const char* fileName, int start, int end)
{
    ifstream file(fileName);
    if (!file.is_open()) {
        cerr << "Eroare la deschiderea fisierului pentru citire: " << fileName << endl;
        MPI_Abort(MPI_COMM_WORLD, 1);
        return {};
    }

    int size;
    file >> size; 

    if (start < 0 || end >= size || start > end) {
        cerr << "Interval invalid: start = " << start << ", end = " << end << endl;
        MPI_Abort(MPI_COMM_WORLD, 1);
        return {};
    }

    vector<int> fullVector(size);
    for (size_t i = 0; i < size; i++) {
        file >> fullVector[i]; 
    }

    reverse(fullVector.begin(), fullVector.end());

    vector<int> subVector(fullVector.begin() + start, fullVector.begin() + end + 1);

    file.close();
    return subVector;
}



// Functie care inverseaza un vector si returneaza rezultatul
vector<int> reverseVector(const vector<int>& vec) {
    vector<int> reversedVec(vec.size());
    for (size_t i = 0; i < vec.size(); i++) {
        reversedVec[i] = vec[vec.size() - i - 1];
    }
    return reversedVec;
}

void printVector(const vector<int>& vec)
{
    for (const int& val : vec)
    {
        cout << val << " ";
    }
    cout << endl;
}

vector<int> removeLeadingZeros(const vector<int>& vec) {
    // Căutăm primul element diferit de 0
    int index = 0;
    while (index < vec.size() && vec[index] == 0) {
        ++index;
    }

    return vector<int>(vec.begin() + index, vec.end());
}

pair<vector<int>, int> addLargeNumbers(const vector<int>& vec1, const vector<int>& vec2, int initialCarry) {
    int size = vec1.size();
    vector<int> result(size), vec11, vec22;
    int carry = initialCarry;


    for (int i = 0; i < size; i++) {
        int sum = vec1[i] + vec2[i] + carry;
        result[i] = sum % 10;
        carry = sum / 10;
    }

    //result = reverseVector(result);
    return { result, carry };  // returnează carry-ul final pentru următorul proces
}