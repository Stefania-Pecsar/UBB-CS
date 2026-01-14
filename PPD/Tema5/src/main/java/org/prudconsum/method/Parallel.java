package org.prudconsum.method;

import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.queue.CustomQueue;
import org.prudconsum.thread.ReaderThread;
import org.prudconsum.thread.WorkerThread;
import org.prudconsum.utils.Constants;

import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Parallel {
    public static void run(int nrOfReaderThreads, int nrOfWriterThreads){
        //create list and blacklist
        LinkedList result = new LinkedList();
        Set<String> blackList = Collections.synchronizedSet(new HashSet<>());

        //executor service for readers
        ExecutorService readerExecutor = Executors.newFixedThreadPool(nrOfReaderThreads);

        CustomQueue<String> queue = new CustomQueue<>(100, nrOfWriterThreads);

        //prepare file list
        List<String> filesArray = new ArrayList<>();
        for(int i = 1;i<=Constants.NO_OF_PROBLEMS;i++)
        {
            filesArray.add("/proiect" + i+".txt");
        }

        //Calc file distr. for reader threads
        int filesPerThread = filesArray.size()/nrOfReaderThreads;
        int remainder = filesArray.size()%nrOfReaderThreads;
        int start = 0, end = filesPerThread;
        for(int i = 0; i < nrOfReaderThreads;i++)
        {
            if(remainder > 0)
            {
                end++;
                remainder--;
            }
            List<String> threadFiles = filesArray.subList(start, end);
            readerExecutor.submit(new ReaderThread(i,threadFiles,queue,false,null));
            start = end;
            end += filesPerThread;
        }

        //shutdown reader executor
        readerExecutor.shutdown();

        //start workwr t
        Thread[] writerThreads = new Thread[nrOfWriterThreads];
        LinkedList dummySortedList = new LinkedList();

        for (int i = 0; i < nrOfWriterThreads; i++)
        {
            // WorkerThread V2 așteaptă 5 argumente
            writerThreads[i] = new WorkerThread(i,queue,result,blackList, dummySortedList);
            writerThreads[i].start();
        }

        //wait for all readers
        try{
            if(!readerExecutor.awaitTermination(Long.MAX_VALUE, TimeUnit.MICROSECONDS))
            {
                System.err.println("Timeout waiting for reader threads");
            }


            queue.consumerFinished();

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        for(int i = 0; i < nrOfWriterThreads; i++)
        {
            try{
                queue.enqueue("-1 -1");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        //wait for all workers
        for (Thread worker : writerThreads)
        {
            try{
                worker.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        Thread writerThread = new ReaderThread(0,filesArray,queue,true,result);
        writerThread.start();

        try{
            writerThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}