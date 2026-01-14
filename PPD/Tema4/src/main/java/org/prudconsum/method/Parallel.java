package org.prudconsum.method;

import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.queue.CustomQueue;
import org.prudconsum.thread.ReaderThread;
import org.prudconsum.thread.WorkerThread;
import org.prudconsum.utils.Constants;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Parallel {
    public static void run(int nrOfReaderThreads, int nrOfWriterThreads){
        //create list
        LinkedList result = new LinkedList();
        //coada
        CustomQueue<String> queue = new CustomQueue<>();
        Object lock = new Object();

        int p_r=nrOfReaderThreads;
        int p_w=nrOfWriterThreads;

        List<String> filesArray = new ArrayList<>();

        for(int i = 1;i<= Constants.NO_OF_PROBLEMS;i++){
            filesArray.add("proiect" + i + ".txt");
        }

        //threads arrays
        Thread[] readerThreads = new Thread[p_r];
        Thread[] writerThreads = new Thread[p_w];

        //start la workeri
        for(int i = 0; i< p_w; i++){
            writerThreads[i] = new WorkerThread(i,queue,result,lock);
            writerThreads[i].start();
        }

        //calc cate fisiere ia fiecare thread
        int filesPerThread = filesArray.size()/p_r;
        int rest = filesArray.size()%p_r;
        int start = 0;

        for(int i = 0;i<p_r;i++)
        {
            int filesCount = filesPerThread + (i < rest ? 1 : 0);
            int end = start + filesCount;

            List<String> threadFiles = new ArrayList<>();
            for (int j = start; j < end; j++) {
                threadFiles.add(filesArray.get(j));
            }
            readerThreads[i]= new ReaderThread(i,threadFiles,queue,lock,false,null);
            readerThreads[i].start();
            start = end ;
        }

        //astept sa termine toti readerii
        for(Thread reader : readerThreads){
            try {
                reader.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        //pun in coada -1 -1 pentru a sti ca s-a terminat
        for(int i = 0; i< p_w; i++){
            queue.enqueue("-1 -1");
            synchronized(lock){
                lock.notifyAll();
            }
        }

        //astept sa termine toti workerii
        for(Thread worker : writerThreads){
            try {
                worker.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        //trimit la primul reader ca sa salvez rez
        readerThreads[0] = new ReaderThread(0,filesArray,queue,lock,true,result);
        readerThreads[0].start();

        try {
            readerThreads[0].join();
        }catch (InterruptedException e){
            e.printStackTrace();
        }
    }
}