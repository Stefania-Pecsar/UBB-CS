package org.prudconsum.linkedList;

public interface ILinkedList {

    LinkedListE getHead();
    void add(LinkedListE element);
    void remove(String key);
    LinkedListE search(String key);
    void addOrUpdate(LinkedListE element);
    LinkedListE extractHead();
    void insertSorted(LinkedListE element);
}