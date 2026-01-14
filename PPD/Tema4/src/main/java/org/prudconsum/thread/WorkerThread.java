package org.prudconsum.thread;

import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.linkedList.LinkedListE;
import org.prudconsum.queue.CustomQueue;



public class WorkerThread extends Thread {
    private LinkedList list;
    private CustomQueue<String> queue;
    private final Object lock;
    private int id;

    public WorkerThread(int id,CustomQueue<String> queue, LinkedList list, Object lock) {
        this.id=id;
        this.queue = queue;
        this.list = list;
        this.lock = lock;
    }

    @Override
    public void run() {
        while (true) {
            String line;
            synchronized (lock) {
                //cat timp coada goala,astemptam
                while (queue.isEmpty()) {
                    try {
                        lock.wait();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
                // scoatem din coada
                line= queue.dequeue();
                // daca e -1 -1 iesim
                if(line.equals("-1 -1"))
                {
                    queue.enqueue(line);
                    lock.notifyAll();
                    break;
                }
            }
            //procesez linia
            process(line);
        }
    }

    private void process(String line) {
        String[] fields = line.split(" ");
        String id =  fields[0].trim();
        int score = Integer.parseInt(fields[1].trim());

        //blochez lista
        synchronized (list){
          LinkedListE element = new LinkedListE(id, score);
          list.addOrUpdate(element);
        }
    }
}