//#include "mpi.h"
//#include <stdio.h>
//#include <stdlib.h>
//#include <random>
//#include <iostream>
//#include <chrono>
//#include <vector>
//#include "utils.h"
//using namespace std;
//
//int main(int argc, char** argv)
//{
//    int rank, numprocs;
//    MPI_Init(&argc, &argv);
//    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
//    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
//    MPI_Status status;
//
//    if (numprocs <= 1) {
//        if (rank == 0) {
//            std::cerr << "This program requires at least 2 MPI processes." << std::endl;
//        }
//        MPI_Finalize();
//        return 1;
//    }
//
//    vector<int> vector1, vector2, rezultat;
//    int total_size = 0;
//    int start, end;
//
//    auto startTime = std::chrono::high_resolution_clock::now();
//
//    if (rank == 0) {
//        // citirea datelor
//        vector1 = readVectorFromFile("C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar1.txt");
//        vector2 = readVectorFromFile("C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar2.txt");
//
//
//        total_size = max(vector1.size(), vector2.size());
//        vector1.resize(total_size, 0);
//        vector2.resize(total_size, 0);
//        rezultat.resize(total_size, 0);
//
//        // calc segmentele
//        int base_chunk = total_size / (numprocs - 1);
//        int remainder = total_size % (numprocs - 1);
//        start = 0;
//
//        for (int i = 1; i < numprocs; i++) {
//            int chunk_size = base_chunk + (i <= remainder ? 1 : 0);
//            end = start + chunk_size - 1;
//
//            // send start și end
//            MPI_Send(&start, 1, MPI_INT, i, 0, MPI_COMM_WORLD);
//            MPI_Send(&end, 1, MPI_INT, i, 1, MPI_COMM_WORLD);
//            MPI_Send(&chunk_size, 1, MPI_INT, i, 2, MPI_COMM_WORLD);
//
//            // send doar segmentele relevante
//            MPI_Send(vector1.data() + start, chunk_size, MPI_INT, i, 3, MPI_COMM_WORLD);
//            MPI_Send(vector2.data() + start, chunk_size, MPI_INT, i, 4, MPI_COMM_WORLD);
//
//            start = end + 1;
//        }
//    }
//
//    if (rank != 0) {
//        // procesare worker
//        int chunk_size;
//        MPI_Recv(&start, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
//        MPI_Recv(&end, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
//        MPI_Recv(&chunk_size, 1, MPI_INT, 0, 2, MPI_COMM_WORLD, &status);
//
//        vector<int> nr1(chunk_size), nr2(chunk_size);
//        MPI_Recv(nr1.data(), chunk_size, MPI_INT, 0, 3, MPI_COMM_WORLD, &status);
//        MPI_Recv(nr2.data(), chunk_size, MPI_INT, 0, 4, MPI_COMM_WORLD, &status);
//
//        // primeste carry de la procesul anterior
//        int initialCarry = 0;
//        if (rank > 1) {
//            MPI_Recv(&initialCarry, 1, MPI_INT, rank - 1, 5, MPI_COMM_WORLD, &status);
//        }
//
//        //calc suma
//        pair<vector<int>, int> additionResult = addLargeNumbers(nr1, nr2, initialCarry);
//        vector<int> result = additionResult.first;
//        int localCarry = additionResult.second;
//
//
//        // trm carry catre urm proces
//        if (rank != numprocs - 1) {
//            MPI_Send(&localCarry, 1, MPI_INT, rank + 1, 5, MPI_COMM_WORLD);
//        }
//
//        // trm rez la procesul 0
//        MPI_Send(&start, 1, MPI_INT, 0, 6, MPI_COMM_WORLD);
//        MPI_Send(&end, 1, MPI_INT, 0, 7, MPI_COMM_WORLD);
//        MPI_Send(&localCarry, 1, MPI_INT, 0, 8, MPI_COMM_WORLD);
//        MPI_Send(result.data(), chunk_size, MPI_INT, 0, 9, MPI_COMM_WORLD);
//    }
//
//    if (rank == 0) {
//        // colecteaza rezultatele
//        int final_carry = 0;
//        for (int i = 1; i < numprocs; i++) {
//            int start_recv, end_recv, carry_recv;
//            MPI_Recv(&start_recv, 1, MPI_INT, i, 6, MPI_COMM_WORLD, &status);
//            MPI_Recv(&end_recv, 1, MPI_INT, i, 7, MPI_COMM_WORLD, &status);
//            MPI_Recv(&carry_recv, 1, MPI_INT, i, 8, MPI_COMM_WORLD, &status);
//
//            int chunk_size_recv = end_recv - start_recv + 1;
//            vector<int> chunk_result(chunk_size_recv);
//            MPI_Recv(chunk_result.data(), chunk_size_recv, MPI_INT, i, 9, MPI_COMM_WORLD, &status);
//
//            // rezultat final
//            for (int j = 0; j < chunk_size_recv; j++) {
//                rezultat[start_recv + j] = chunk_result[j];
//            }
//
//            // pastreaza carry de la ultimul proces
//            if (i == numprocs - 1) {
//                final_carry = carry_recv;
//            }
//
//        }
//
//        // adauga carry final daca e necesar
//        if (final_carry > 0) {
//            rezultat.push_back(final_carry);
//        }
//
//        auto endTime = std::chrono::high_resolution_clock::now();
//        auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(endTime - startTime).count();
//        double durationInSeconds = static_cast<double>(duration) / 1e9;
//
//        cout << "Durata: " << durationInSeconds << " s" << endl;
//
//        vector<int> rezultat_final = reverseVector(rezultat);
//        cout << "Suma corecta: ";
//        printVector(rezultat_final);
//        saveVectorToFile(rezultat_final, "C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar3.txt");
//    }
//
//    MPI_Finalize();
//    return 0;
//}