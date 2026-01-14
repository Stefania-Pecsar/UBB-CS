#include "mpi.h"
#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include "utils.h"
#include <chrono>
using namespace std;

int main(int argc, char** argv)
{
    int rank, numprocs;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (numprocs < 2) {
        if (rank == 0) {
            std::cerr << "This program requires at least 2 MPI processes." << std::endl;
        }
        MPI_Finalize();
        return 1;
    }

    vector<int> numar1, numar2, rezultat;
    int total_size = 0;

    auto startTime = std::chrono::high_resolution_clock::now();

    // Procesul 0 citeste datele
    if (rank == 0) {
        numar1 = readVectorFromFile("C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar1.txt");
        numar2 = readVectorFromFile("C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar2.txt");

        total_size = max(numar1.size(), numar2.size());

        if (total_size % numprocs != 0) {
            total_size += numprocs - (total_size % numprocs);
        }

        numar1.resize(total_size, 0);
        numar2.resize(total_size, 0);
        rezultat.resize(total_size, 0);
    }

    MPI_Bcast(&total_size, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int chunk_size = total_size / numprocs;
    vector<int> local_num1(chunk_size), local_num2(chunk_size), local_rezultat(chunk_size);

    vector<MPI_Request> send_requests; 
    MPI_Request recv_requests[2];


    if (rank == 0) {
        // Procesul 0 isi pastreaza primul chunk
        copy(numar1.begin(), numar1.begin() + chunk_size, local_num1.begin());
        copy(numar2.begin(), numar2.begin() + chunk_size, local_num2.begin());

        for (int i = 1; i < numprocs; i++) {
            int start = i * chunk_size;
            MPI_Request req1, req2;

            MPI_Isend(numar1.data() + start, chunk_size, MPI_INT, i, 0, MPI_COMM_WORLD, &req1);
            MPI_Isend(numar2.data() + start, chunk_size, MPI_INT, i, 1, MPI_COMM_WORLD, &req2);

            send_requests.push_back(req1);
            send_requests.push_back(req2);
        }

    }
    else {
        MPI_Irecv(local_num1.data(), chunk_size, MPI_INT, 0, 0, MPI_COMM_WORLD, &recv_requests[0]);
        MPI_Irecv(local_num2.data(), chunk_size, MPI_INT, 0, 1, MPI_COMM_WORLD, &recv_requests[1]);

    }

    int carry = 0;
    MPI_Request carry_recv_request, carry_send_request;

    if (rank > 0) {
        // Primeste carry de la procesul anterior 
        MPI_Irecv(&carry, 1, MPI_INT, rank - 1, 2, MPI_COMM_WORLD, &carry_recv_request);
    }
    auto result = addLargeNumbers(local_num1, local_num2, carry);
    local_rezultat = result.first;
    int outgoing_carry = result.second;


    if (rank < numprocs - 1) {
        MPI_Isend(&outgoing_carry, 1, MPI_INT, rank + 1, 2, MPI_COMM_WORLD, &carry_send_request);
    }

    MPI_Request gather_request;
    MPI_Gather(local_rezultat.data(), chunk_size, MPI_INT,
        rezultat.data(), chunk_size, MPI_INT, 0, MPI_COMM_WORLD, &gather_request);

    if (rank == 0) {
        MPI_Wait(&gather_request, MPI_STATUS_IGNORE);

        // Primeste carry final de la ultimul proces - IRecv
        int final_carry = 0;
        if (numprocs > 1) {
            MPI_Request final_carry_request;
            MPI_Irecv(&final_carry, 1, MPI_INT, numprocs - 1, 3, MPI_COMM_WORLD, &final_carry_request);
           // MPI_Wait(&final_carry_request, MPI_STATUS_IGNORE);
        }

        // Adauga carry final
        if (final_carry > 0) {
            rezultat.push_back(final_carry);
        }

        auto endTime = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(endTime - startTime).count();
        double durationInSeconds = static_cast<double>(duration) / 1e9;

        cout << "Durata Varianta 3 (Asincron): " << durationInSeconds << " secunde" << endl;

        vector<int> rezultat_final = reverseVector(rezultat);
        saveVectorToFile(rezultat_final, "C:/Users/Administrator/Fac/AN 3/PPD/Tema3/Tema3/Numar3.txt");
    }
    else if (rank == numprocs - 1) {
        MPI_Request final_send_request;
        MPI_Isend(&outgoing_carry, 1, MPI_INT, 0, 3, MPI_COMM_WORLD, &final_send_request);
        //MPI_Wait(&final_send_request, MPI_STATUS_IGNORE);
    }

    MPI_Finalize();
    return 0;
}