package com.example.socialnetworwfx.domain;

import java.io.Serializable;

public abstract class Entity<ID> implements Serializable {
    private ID identityKey;


    public ID getID() {

        return identityKey;
    }

    public void setID(ID identityKey) {

        this.identityKey = identityKey;
    }


}
