package org.prudconsum.thread;

import org.prudconsum.linkedList.ILinkedList;
import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.linkedList.LinkedListE;
import org.prudconsum.queue.CustomQueue;
import org.prudconsum.utils.Constants;

import java.io.*;
import java.util.List;

public class ReaderThread extends Thread {
    private List<String> files;
    private CustomQueue<String> queue;
    private final Boolean writeToFile;
    private ILinkedList results = null;
    private int id;

    public ReaderThread(int id,List<String > files, CustomQueue<String> queue,  Boolean writeToFile, ILinkedList results) {
        this.id=id;
        this.files = files;
        this.queue = queue;
        this.writeToFile = writeToFile;
        this.results = results;
    }

    @Override
    public void run(){
        try {
            if (!writeToFile) {
                readFilesAndEnqueue();
            } else {
                writeResultsToFile();
            }
        } catch (IllegalMonitorStateException e) {
            return;
        }
    }

    private void readFilesAndEnqueue() {
        for(String file:files)
        {
            try (BufferedReader br = new BufferedReader(new FileReader(Constants.OUTPUT_DIR + '\\' + file))) {
                String line;

                while ((line = br.readLine()) != null) {
                    queue.enqueue(line);  // Add line to queue
                }
            } catch (FileNotFoundException e) {
                System.err.printf("File %s not found!%n", file);
            } catch (IOException | InterruptedException e) {
                System.err.printf("Error reading file %s: %s%n", file, e.getMessage());
            }
        }
    }

    private void writeResultsToFile() {
        LinkedList sortedList = new LinkedList();
        LinkedListE nodeToMove;
        while ((nodeToMove = results.extractHead()) != null) {
            sortedList.insertSorted(nodeToMove);
        }

        try (BufferedWriter bw = new BufferedWriter(new FileWriter("resultsParallel.txt"))) {
            while (sortedList.getHead() != null) {
                bw.write(sortedList.getHead().participant + " " + sortedList.getHead().nota +"\n");
                sortedList.remove(sortedList.getHead().participant);
            }
        } catch (IOException e) {
            System.err.println("Eroare la scrierea rezultatelor în fișier: " + e.getMessage());
        }
    }
}