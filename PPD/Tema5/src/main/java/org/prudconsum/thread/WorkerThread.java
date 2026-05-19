package org.prudconsum.thread;

import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.linkedList.LinkedListE;
import org.prudconsum.queue.CustomQueue;
import java.util.Set;

public class WorkerThread extends Thread {
    private LinkedList list;
    private LinkedList sortedList;
    private CustomQueue<String> queue;
    private Set<String> blackList;
    private final int id;

    public WorkerThread(int id, CustomQueue<String> queue, LinkedList list, Set<String> blackList, LinkedList sortedList) {
        this.id = id;
        this.queue = queue;
        this.list = list;
        this.blackList = blackList;
        this.sortedList = sortedList;
    }

    @Override
    public void run() {
        // FAZA 1: Consumare date (Procesare)
        while (true) {
            try {
                String line = queue.dequeue();

                // Verificare semnal de oprire
                if (line.equals("-1 -1 -1")) {
                    break;
                }

                process(line);

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }

        // FAZA 2: Sortare Colectivă
        // După ce nu mai sunt date de citit, mutăm nodurile în lista sortată
        LinkedListE node;
        while ((node = list.extractHead()) != null) {
            sortedList.insertSorted(node);
        }
    }

    private void process(String line) {
        String[] parts = line.trim().split(" ");
        if (parts.length < 2) return; // Evităm linii goale sau corupte

        String id = parts[0].trim();
        int score = 0;
        try {
            score = Integer.parseInt(parts[1].trim());
        } catch (NumberFormatException e) {
            return;
        }

        // LOGICĂ BLACKLIST: Nota -1 înseamnă copiere
        if (score == -1) {
            blackList.add(id);
            list.remove(id); // Eliminăm studentul din rezultate dacă exista deja
        } else {
            // Adăugăm doar dacă nu e în blacklist
            if (!blackList.contains(id)) {
                list.addOrUpdate(new LinkedListE(id, score));
            }
        }
    }
}