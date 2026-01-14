package org.prudconsum.queue;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class CustomQueue<T> {
    private Node<T> head;
    private Node<T> tail;
    private final AtomicInteger size = new AtomicInteger(0);
    private final int capacity;
    private final int totalConsumers;
    private volatile boolean sortingPhase = false;
    private boolean hasFinished = false;

    private final Lock lock = new ReentrantLock();
    private final Condition isNotFull = lock.newCondition();
    private final Condition isNotEmpty = lock.newCondition();

    private static class Node<T> {
        T value;
        Node<T> next;
        Node(T value) { this.value = value; this.next = null; }
    }

    public CustomQueue(int capacity, int totalConsumers) {
        this.capacity = capacity; // MAX=100 conform cerinței
        this.totalConsumers = totalConsumers;
    }

    public void enqueue(T item) throws InterruptedException {
        lock.lock();
        try {
            while (size.get() == capacity) isNotFull.await(); // Variabilă condițională
            Node<T> newNode = new Node<>(item);
            if (tail == null) head = tail = newNode;
            else { tail.next = newNode; tail = newNode; }
            size.incrementAndGet();
            isNotEmpty.signalAll();
        } finally { lock.unlock(); }
    }

    public T dequeue() throws InterruptedException {
        lock.lock();
        try {
            while (size.get() == 0) {
                if (hasFinished) return null; // Permite ieșirea workerilor pentru faza de sortare
                isNotEmpty.await(); // Variabilă condițională
            }
            T value = head.value;
            head = head.next;
            if (head == null) tail = null;
            size.decrementAndGet();
            isNotFull.signalAll();
            return value;
        } finally { lock.unlock(); }
    }

    public void consumerFinished() {
        lock.lock();
        try {
            hasFinished = true;
            isNotEmpty.signalAll(); // Deblochează workerii care așteaptă la o coadă goală
            isNotFull.signalAll();
        } finally { lock.unlock(); }
    }

    public void startSortingPhase() {
        lock.lock();
        try {
            this.sortingPhase = true;
            isNotEmpty.signalAll();
        } finally { lock.unlock(); }
    }

    public boolean isSortingPhase() { return sortingPhase; }

    private final AtomicInteger finishedSortingCount = new AtomicInteger(0);
    public void signalWorkerFinishedSorting() {
        finishedSortingCount.incrementAndGet();
    }
}