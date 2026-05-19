//#include <iostream>
//#include <vector>
//#include <fstream>
//#include <algorithm>
//#include <mpi.h>
//#include <cstdint>
//#include <string>
//using namespace std;
//
//bool compareFiles(const char* file1, const char* file2) {
//    ifstream f1(file1);
//    ifstream f2(file2);
//
//    if (!f1.is_open() || !f2.is_open()) {
//        cerr << "Eroare la deschiderea fisierelor pentru comparatie!" << endl;
//        return false;
//    }
//
//    string line1, line2;
//    while (getline(f1, line1) && getline(f2, line2)) {
//        if (line1 != line2) {
//            return false;
//        }
//    }
//
//    return f1.eof() && f2.eof();
//}
//
//int main() {
//
//    if (compareFiles("C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar3.txt", "C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Secvential.txt")) {
//        std::cout << "Fisierele sunt identice." << std::endl;
//    }
//    else {
//        std::cout << "Fisierele sunt diferite." << std::endl;
//    }
//
//    return 0;
//}