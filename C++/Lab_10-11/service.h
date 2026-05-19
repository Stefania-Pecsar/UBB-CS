#pragma once

#include "repo.h"
#include "undo_act.h"

/**
 * Clasa Service din arhitectura GRASP
 */
class Service {
public:
    /**
     * Functia constructor
     * @param rp repo
     * @param vd validator
     */
    Service(AbsRepo* rp, Validator& vd);

    /**
     * Functia returneaza toate entitatile
     * @return un vector cu elemente de tip medcine
     */
    vector<Turism>& get_all_ent();

    /**
     * Adauaga un element in lista de obicete
     * @param cdenumire denumirile
     * @param cdestinatie destinatie
     * @param ctip tipul
     * @param cpret pretul 
     * @raises un string de erori
     */
    void add(const string& cdenumire, const string& cdestinatie, const string& ctip, const int& cpret);

    /**
     * Modifica o entitate deja existenta
     * @param poz pozitia de sters
     * @param cdenumire denumirile
     * @param cdestinatie destinatie
     * @param ctip tipul
     * @param cpret pretul 
     * @raises un string de erori
     */
    void modify(const int& poz, const string& cdenumire, const string& cdestinatie, const string& ctip, const int& cpret);

    /**
     * Functia sterge entitatea de pe pozitia poz
     * @param poz pozitia de sters
     * @raises string de erori
     */
    void del(const int& poz);

    /**
     * Functia cauta o anumita entitate
     * @param cdenumire denumirile
     * @param cdestinatie destinatie
     * @param ctip tipul
     * @param cpret pretul 
     * @return 0 sau 1, daca se gaseste sau nu
     */
    bool search(const string& cdenumire, const string& cdestinatie, const string& ctip, const int& cpret);

    /**
     * Functia de filtrare
     * @param crit criteriul
     * @param val valoarea
     * @param res vectorul rezultat
     */
    void filter(int crit, const string& val, vector<Turism>&);

    /**
     * Functia de sortare
     * @param crit criteriul
     * @param rez rezultateu
     */
    void sort(int crit, vector<Turism>& rez);

    void undo();

    ///destructor
    ~Service() = default;
private:
    AbsRepo* repo;
    [[maybe_unused]] Validator valid;
    vector<ActUndo*> undo_act;
};

void test_service();