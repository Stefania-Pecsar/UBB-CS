package org.prudconsum.linkedList;

import java.util.Objects;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class LinkedListE {
    public String participant;
    public Integer nota;
    public LinkedListE next;

    private final Lock lock = new ReentrantLock(); // un ReentrantLock este un lock
    // care poate fi
    // blocat si deblocat de acelasi thread

    public LinkedListE(String participant, Integer nota) {
        this.participant = participant;
        this.nota = nota;
        this.next = null;
    }

    public void lock() {
        lock.lock();
    }
    public void unlock() {
        lock.unlock();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof LinkedListE that)) return false;
        return Objects.equals(participant, that.participant) ;
    }

    @Override
    public int hashCode() {
        return Objects.hash(participant);
    }

}