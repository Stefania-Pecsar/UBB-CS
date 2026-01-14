package org.prudconsum.linkedList;

public class LinkedList implements ILinkedList{
    public LinkedListE head;
    public LinkedList() {
        this.head = null;
    }
    //daca primesc head-ul
    public LinkedList(LinkedListE head) {
        this.head = head;
    }
    @Override
    public LinkedListE getHead() {
        return this.head;
    }

    @Override
    public void add(LinkedListE element) {
       element.next = this.head;
       this.head = element;
    }

    @Override
    public void remove(String key) {
        if (this.head == null) {
            return;
        }

        if (this.head.participant.equals(key)) {
            this.head = this.head.next;
            return;
        }

        LinkedListE current = this.head;
        while (current.next != null && !current.next.participant.equals(key)) {
            current = current.next;
        }

        if (current.next != null) {
            current.next = current.next.next;
        }

    }

    @Override
    public LinkedListE search(String key) {
        LinkedListE current = this.head;
        while (current != null) {
            if (current.participant.equals(key)) {
                return current;
            }
            current = current.next;
        }
        return null;
    }

    @Override
    public void addOrUpdate(LinkedListE element) {
        var current = search(element.participant);
        if (current == null) {
            add(element);
        } else {
            current.nota += element.nota;
            remove(element.participant);
            add(current);
        }
    }
}