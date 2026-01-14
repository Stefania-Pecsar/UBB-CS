package org.prudconsum.linkedList;

public class LinkedList implements ILinkedList {
    private final LinkedListE head;
    private final LinkedListE tail;

    public LinkedList() {
        head = new LinkedListE("HEAD_SENTINEL", Integer.MIN_VALUE);
        tail = new LinkedListE("TAIL_SENTINEL", Integer.MAX_VALUE);
        head.next = tail;
    }

    @Override
    public LinkedListE getHead() {
        head.lock();
        try {
            return head.next == tail ? null : head.next;
        } finally {
            head.unlock();
        }
    }

    @Override
    public void add(LinkedListE element) {
        head.lock();
        try {
            LinkedListE first = head.next;
            first.lock();
            try {
                element.next = first;
                head.next = element;
            } finally {
                first.unlock();
            }
        } finally {
            head.unlock();
        }
    }

    @Override
    public void remove(String key) {
        LinkedListE pred = head;
        pred.lock();
        try {
            LinkedListE curr = pred.next;
            curr.lock();
            try {
                while (curr != tail) {
                    if (curr.participant.equals(key)) {
                        pred.next = curr.next;
                        return;
                    }

                    pred.unlock();
                    pred = curr;
                    curr = curr.next;
                    curr.lock();
                }
            } finally {
                curr.unlock();
            }
        } finally {
            pred.unlock();
        }
    }

    @Override
    public LinkedListE search(String key) {
        LinkedListE pred = head;
        pred.lock();
        try {
            LinkedListE curr = pred.next;
            curr.lock();
            try {
                while (curr != tail) {
                    if (curr.participant.equals(key)) {
                        return curr;
                    }
                    pred.unlock();
                    pred = curr;
                    curr = curr.next;
                    curr.lock();
                }
                return null;
            } finally {
                curr.unlock();
            }
        } finally {
            pred.unlock();
        }
    }

    @Override
    public void addOrUpdate(LinkedListE element) {
        LinkedListE pred = head;
        pred.lock();
        try {
            LinkedListE curr = pred.next;
            curr.lock();
            try {
                while (curr != tail) {
                    if (curr.participant.equals(element.participant)) {
                        curr.nota = Math.max(curr.nota, element.nota);
                        return;
                    }
                    pred.unlock();
                    pred = curr;
                    curr = curr.next;
                    curr.lock();
                }
                element.next = tail;
                pred.next = element;
            } finally {
                curr.unlock();
            }
        } finally {
            pred.unlock();
        }
    }

    @Override
    public LinkedListE extractHead() {
        head.lock();
        try {
            LinkedListE first = head.next;
            if (first == tail) return null;
            first.lock();
            try {
                head.next = first.next;
                first.next = null;
                return first;
            } finally {
                first.unlock();
            }
        } finally {
            head.unlock();
        }
    }

    @Override
    public void insertSorted(LinkedListE element) {
        LinkedListE pred = head;
        pred.lock();
        try {
            LinkedListE curr = pred.next;
            curr.lock();
            try {
                while (curr != tail) {
                    if (element.nota > curr.nota) {
                        element.next = curr;
                        pred.next = element;
                        return;
                    }
                    pred.unlock();
                    pred = curr;
                    curr = curr.next;
                    curr.lock();
                }
                element.next = tail;
                pred.next = element;
            } finally {
                curr.unlock();
            }
        } finally {
            pred.unlock();
        }
    }
}