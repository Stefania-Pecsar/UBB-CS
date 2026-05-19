package org.prudconsum.thread;

import org.prudconsum.linkedList.ILinkedList;
import org.prudconsum.queue.CustomQueue;
import org.prudconsum.utils.Constants;

import java.io.*;
import java.util.List;

public class ReaderThread extends Thread {
    private List<String> files;
    private CustomQueue<String> queue;
    private final Object lock;
    private final Boolean writeToFile;
    private ILinkedList results = null;
    private int id;

    public ReaderThread(int id,List<String> files, CustomQueue<String> queue, Object lock, Boolean writeToFile, ILinkedList results) {
        this.id=id;
        this.files = files;
        this.queue = queue;
        this.lock = lock;
        this.writeToFile = writeToFile;
        this.results = results;
    }

    @Override
    public void run() {
        if (!writeToFile) {
            //pt citire fiecare fisier si pun in coada
            for (String file : files) {
                try (BufferedReader br = new BufferedReader(new FileReader(Constants.OUTPUT_DIR + '\\' + file))) {
                    String line;
                    while (true) {
                        try {
                            if (!((line = br.readLine()) != null)) break;
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                        synchronized (lock)
                        //pun in coada
                        {
                            queue.enqueue(line);
                            lock.notifyAll();
                        }
                    }
                } catch (FileNotFoundException e) {
                    throw new RuntimeException(e);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                //notfic
            }
        } else {
            //scriu in fisier
            try (BufferedWriter bw = new BufferedWriter(new FileWriter("resultsParallel.txt"))) {
                while (results.getHead() != null) {
                    bw.write(results.getHead().participant + " " + results.getHead().nota + "\n");
                    results.remove(results.getHead().participant);
                }
            }catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
}