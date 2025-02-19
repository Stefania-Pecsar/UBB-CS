#pragma once

#include "repo.h"

class ActUndo {
public:
    virtual void doUndo() = 0;
    virtual ~ActUndo() = default;
};

class UndoAdd :public ActUndo {
private:
    AbsRepo* fr;
    Turism last;
public:
    UndoAdd(AbsRepo* f, const Turism& lst) : fr{ f }, last{ lst } {}
    void doUndo() override {
        int i = 0;
        for (auto& it : fr->get_elems()) {
            if (it == last) {
                break;
            }
            ++i;
        }
        fr->delete_turism(i);
    }
};

class UndoMod :public ActUndo {
private:
    AbsRepo* fr;
    Turism  last;
    int l_poz;
public:
    UndoMod(AbsRepo* f, const Turism& t, const int l_p) : fr{ f }, last{ t }, l_poz{ l_p } {}
    void doUndo() override {
        fr->modify_turism(last, l_poz);
    }
};

class UndoDel :public ActUndo {
private:
    AbsRepo* fr;
    Turism  dlt;
    int poz;
public:
    UndoDel(AbsRepo* f, const Turism& t, const int pz) : fr{ f }, dlt{ t }, poz{ pz } {}
    void doUndo() override {
        auto it = fr->get_elems().begin();
        it += poz;
        fr->get_elems().insert(it, dlt);
    }
};
