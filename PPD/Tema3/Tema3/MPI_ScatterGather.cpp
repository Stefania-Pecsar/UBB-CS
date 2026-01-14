//#include "mpi.h"
//#include <stdio.h>
//#include <stdlib.h>
//#include <random>
//#include <chrono>
//#include <iostream>
//#include <vector>
//#include <chrono>
//using namespace std;
//
//#include "utils.h"
//
//int main(int argc, char** argv) {
//    int rank, numprocs;
//    MPI_Init(&argc, &argv);
//    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
//    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
//    MPI_Status status;
//
//    if (numprocs < 2) {
//        if (rank == 0) {
//            std::cerr << "This program requires at least 2 MPI processes." << std::endl;
//        }
//        MPI_Finalize();
//        return 1;
//    }
//
//    vector<int> vector1, vector2, rezultat;
//    int total_size = 0;
//    int finalCarry = 0;
//
//    auto startTime = std::chrono::high_resolution_clock::now();
//
//    if (rank == 0) {
//        vector1 = readVectorFromFile("C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar1.txt");
//        vector2 = readVectorFromFile("C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar2.txt");
//
//        total_size = max(vector1.size(), vector2.size());
//
//        // Ajustăm dimensiunea pentru a fi divizibilă cu numărul de procese
//        if (total_size % numprocs != 0) {
//            total_size += numprocs - (total_size % numprocs);
//        }
//
//        vector1.resize(total_size, 0);
//        vector2.resize(total_size, 0);
//        rezultat.resize(total_size, 0);
//
//    }
//
//    MPI_Bcast(&total_size, 1, MPI_INT, 0, MPI_COMM_WORLD);
//
//    // calc dim locale
//    int chunk_size = total_size / numprocs;
//    vector<int> local_vec1(chunk_size), local_vec2(chunk_size), local_result(chunk_size);
//
//    // Distribuim datele
//    MPI_Scatter(vector1.data(), chunk_size, MPI_INT, local_vec1.data(), chunk_size, MPI_INT, 0, MPI_COMM_WORLD);
//    MPI_Scatter(vector2.data(), chunk_size, MPI_INT, local_vec2.data(), chunk_size, MPI_INT, 0, MPI_COMM_WORLD);
//
//    int localCarry = 0;
//
//    if (rank > 0) {
//        MPI_Recv(&localCarry, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, &status);
//    }
//
//    // calc suma locala
//    auto resultPair = addLargeNumbers(local_vec1, local_vec2, localCarry);
//    local_result = resultPair.first;
//    int outgoingCarry = resultPair.second;
//
//    // Trimitem carry catre urm procese
//    if (rank < numprocs - 1) {
//        MPI_Ssend(&outgoingCarry, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
//    }
//    else {
//        // ultim proces patstreaza carry final
//        finalCarry = outgoingCarry;
//    }
//
//    // colectam rezultatele
//    MPI_Gather(local_result.data(), chunk_size, MPI_INT, rezultat.data(), chunk_size, MPI_INT, 0, MPI_COMM_WORLD);
//
//    // gestionare rez
//    if (rank == 0) {
//        // Primim carry-ul final de la ultimul proces
//        if (numprocs > 1) {
//            MPI_Recv(&finalCarry, 1, MPI_INT, numprocs - 1, 1, MPI_COMM_WORLD, &status);
//        }
//
//        if (finalCarry > 0) {
//            rezultat.push_back(finalCarry);
//        }
//
//        auto endTime = std::chrono::high_resolution_clock::now();
//        auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(endTime - startTime).count();
//        double durationInSeconds = static_cast<double>(duration) / 1e9;
//        cout << "Durata: " << durationInSeconds << " s" << endl;
//
//        vector<int> rezultat_final = reverseVector(rezultat);
//        cout << "Suma: ";
//        printVector(rezultat_final);
//        saveVectorToFile(rezultat_final, "C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar3.txt");
//    }
//    else if (rank == numprocs - 1) {
//        MPI_Send(&finalCarry, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
//    }
//
//    MPI_Finalize();
//    return 0;
//}