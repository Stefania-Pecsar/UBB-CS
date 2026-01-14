package org.prudconsum.thread;

import org.prudconsum.linkedList.ILinkedList;
import org.prudconsum.linkedList.LinkedListE; // Import necesar pentru iterare la scriere
import org.prudconsum.queue.CustomQueue;
import org.prudconsum.utils.Constants;

import java.io.*;

public class ReaderThreadV2 extends Thread {
    private String fileName; // Numele fișierului (ex: proiect1.txt)
    private CustomQueue<String> queue;
    private final Boolean writeToFile;
    private ILinkedList results;

    // Constructor pentru CITIRE (Reader)
    public ReaderThreadV2(int id, String fileName, CustomQueue<String> queue, Boolean writeToFile, ILinkedList results) {
        this.fileName = fileName;
        this.queue = queue;
        this.writeToFile = writeToFile;
        this.results = results;
    }

    @Override
    public void run() {
        if (!writeToFile) {
            readFilesAndEnqueue();
        } else {
            writeResultsToFile();
        }
    }

    private void readFilesAndEnqueue() {
        // Construim calea corectă folosind separatorul de sistem
        File file = new File(Constants.OUTPUT_DIR, fileName);

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                // Punem linia în coadă pentru workeri
                queue.enqueue(line);
            }
        } catch (FileNotFoundException e) {
            System.err.println("Fișierul NU a fost găsit: " + file.getAbsolutePath());
        } catch (IOException | InterruptedException e) {
            System.err.println("Eroare la citire: " + e.getMessage());
        }
    }

    private void writeResultsToFile() {
        // Această metodă este apelată doar la final, de un singur thread
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(fileName))) { // Aici fileName va fi "resultsParallel.txt"
            LinkedListE curr = results.getHead();
            while (curr != null) {
                bw.write(curr.participant + " " + curr.nota + "\n");
                curr = curr.next;
            }
        } catch (IOException e) {
            System.err.println("Eroare la scriere rezultate: " + e.getMessage());
        }
    }
}