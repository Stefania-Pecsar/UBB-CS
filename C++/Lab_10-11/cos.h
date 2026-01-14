#pragma once

#include <vector>
#include <string>
#include "domain.h"
#include "observer.h"

using std::vector;

/**
 * Clasa care implementeaza ideea de cos
 */
class Cos : public Observable {
private:
    vector<Turism> comp;
public:
    /**
     * Default constructor
     */
    Cos();

    /**
     * Returneaza toate ofertele din cos
     * @return vector de oferte cu ofertele din cos
     */
    [[nodiscard]] vector<Turism>& get_all();

    /**
     * Adauga o noua oferta de turism la cos
     * @param m oferta de turism de adaugat
     */
    void add_to_cos(const Turism& t);

    /**
     * Goleste cosul
     */
    void empty_cos();

    /**
     * Adauga random entitati la cos
     * @param elems ofertele disponibile
     * @param q numarul de oferte ce trebuie adaugate
     */
    void random_add(const vector<Turism>& elems, const int& q);

    /**
     * Salveaza in fisier entitatile
     * @param filename numele fisierului
     */
    void save_to_file(const string& filename);
};
