package com.example.socialnetworwfx.repository.Paginare;

public class Page<E> {
    private Iterable<E> elementsOnPage;

    private int totalNrOfElems;

    public Page(int totalNrOfElems, Iterable<E> elementsOnPage) {
        this.totalNrOfElems = totalNrOfElems;
        this.elementsOnPage = elementsOnPage;
    }

    public Iterable<E> getElementsOnPage() {
        return elementsOnPage;
    }

    public int getTotalNrOfElems() {
        return totalNrOfElems;
    }
}
