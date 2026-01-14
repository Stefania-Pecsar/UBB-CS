package com.example.socialnetworwfx.utils;

import jdk.jfr.Event;

public interface Observer<E extends Event> {
    void update(E e);
}