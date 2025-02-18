package com.example.socialnetworwfx.service;

public interface Service<E> {
    E delete(Long ID);
    Iterable<E> findAll();

}
