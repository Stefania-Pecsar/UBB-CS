package org.prudconsum.method;

import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.queue.CustomQueue;
import org.prudconsum.thread.ReaderThreadV2;
import org.prudconsum.thread.WorkerThread;
import org.prudconsum.utils.Constants;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ParallelV2 {
    public static void run(int nrOfReaderThreads, int nrOfWriterThreads) {
        // Inițializare structuri de date
        LinkedList result = new LinkedList();
        LinkedList sortedResult = new LinkedList();
        Set<String> blackList = Collections.synchronizedSet(new HashSet<>());

        // Coada partajată (Producător-Consumator)
        CustomQueue<String> queue = new CustomQueue<>(100, nrOfWriterThreads);

        // AICI ESTE EXECUTORUL (Thread Pool pentru citire)
        ExecutorService readerExecutor = Executors.newFixedThreadPool(nrOfReaderThreads);

        // 1. Pornire WORKERI (Consumatori)
        // Ei pornesc imediat și așteaptă date în coadă
        Thread[] workerThreads = new Thread[nrOfWriterThreads];
        for (int i = 0; i < nrOfWriterThreads; i++) {
            workerThreads[i] = new WorkerThread(i, queue, result, blackList, sortedResult);
            workerThreads[i].start();
        }

        // 2. Trimitere TASK-URI DE CITIRE către Executor
        for (int j = 1; j <= Constants.NO_OF_PROBLEMS; j++) {
            String fileName = "/proiect" + j + ".txt";
            readerExecutor.submit(new ReaderThreadV2(j, fileName, queue, false, null));
        }

        // 3. BARIERĂ: Așteptăm TERMINAREA CITIRII
        // Este crucial să așteptăm aici, altfel trimitem semnalul de stop prea devreme!
        readerExecutor.shutdown();
        try {
            boolean finished = readerExecutor.awaitTermination(1, TimeUnit.HOURS);
            if (!finished) System.err.println("Timeout la citire!");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // 4. SEMNALIZARE STOP (Poison Pill)
        // Trimitem câte un "-1 -1 -1" pentru fiecare worker, CA SĂ ȘTIE SĂ SE OPREASCĂ
        for (int i = 0; i < nrOfWriterThreads; i++) {
            try {
                queue.enqueue("-1 -1 -1");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        // 5. Așteptăm WORKERII să termine procesarea și sortarea
        for (Thread worker : workerThreads) {
            try {
                worker.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        // 6. Afișare Blacklist în Consolă
        System.out.println("\n=== STUDENȚI FRAUDULOȘI (Nota -1) ===");
        synchronized (blackList) {
            if(blackList.isEmpty()) System.out.println("Niciun student.");
            else blackList.forEach(id -> System.out.println("ID: " + id));
        }
        System.out.println("=====================================\n");

        // 7. Salvare Blacklist în Fișier
        saveBlacklistToFile(blackList);

        // 8. Scriere Rezultate Finale (Descrescător)
        Thread writerThread = new ReaderThreadV2(0, "resultsParallel.txt", queue, true, sortedResult);
        writerThread.start();
        try {
            writerThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private static void saveBlacklistToFile(Set<String> blackList) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter("blacklist.txt"))) {
            bw.write("--- Lista Studenti Copiat ---\n");
            for (String id : blackList) {
                bw.write(id + "\n");
            }
            bw.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}