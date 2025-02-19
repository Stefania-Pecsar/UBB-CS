#pragma once

#include "domain.h"
#include <map>

using namespace std;

class AbsRepo {
public:
    virtual void add_turism(const Turism& a) = 0;

    virtual void modify_turism(const Turism& a, int poz) = 0;

    virtual void delete_turism(int poz) = 0;

    virtual vector<Turism>& get_elems() = 0;

    virtual ~AbsRepo() = default;
};


/**
 * Clasa repository
 */
class Repo :public AbsRepo {
public:
    Repo() = default;
    /**
     * Adauga o oferta de turism in repo
     * @param a oferta de turism de adaugat
     */
    virtual void add_turism(const Turism& a) override;

    /**
     * Modifica o oferta de turism deja existent
     * @param a oferta de turism de modificat
     * @param poz pozitia ofertei de turism
     */
    virtual void modify_turism(const Turism& a, int poz) override;

    /**
     * Functie getter
     * @return un vector cu elemente de tip oferta de turism
     */
    vector<Turism>& get_elems() override;

    /**
     * Sterge oferta de turism de pe o pozitie
     * @param poz pozitia ofertei de turism
     */
    virtual void delete_turism(int poz) override;

    virtual ~Repo() = default;

private:
    vector<Turism> elems;
};


class FileRepo : public Repo {
private:
    string filename;

    void load_from_file();

    void save_to_file();

public:
    FileRepo() = default;
    explicit FileRepo(string fn);

    ~FileRepo() override = default;

    void add_turism(const Turism& a) override {
        Repo::add_turism(a);
        save_to_file();
    }

    void modify_turism(const Turism& a, int poz) override {
        Repo::modify_turism(a, poz);
        save_to_file();
    }

    void delete_turism(int poz) override {
        Repo::delete_turism(poz);
        save_to_file();
    }

};

class RepoProb :public AbsRepo {
private:
    float prob;
    map<int, Turism> elems;
    void det_luck();
public:
    RepoProb() = default;

    explicit RepoProb(float chance);

    void add_turism(const Turism& m) override;

    void modify_turism(const Turism& m, int poz) override;

    void delete_turism(int poz) override;

    vector<Turism>& get_elems() override;
};

/**
 * Clasa custom de exceptie
 */
class RepoException {
public:
    explicit RepoException(const vector<string>& errors) : msg{ errors } {}

    friend ostream& operator<<(ostream& out, const RepoException& ex);

    vector<string> msg;
};

ostream& operator<<(ostream& out, const RepoException& ex);

void test_repo();