package com.example.socialnetworwfx.repository.Paginare;

public class Pageable {
    private int pageNr;
    private int pageSize;

    public Pageable(int pageSize, int pageNr) {
        this.pageSize = pageSize;
        this.pageNr = pageNr;
    }

    public int getPageNr() {
        return pageNr;
    }

    public int getPageSize() {
        return pageSize;
    }
}
