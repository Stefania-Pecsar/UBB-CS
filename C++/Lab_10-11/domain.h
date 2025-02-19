#pragma once

#include<vector>
#include<sstream>

using namespace std;

/**
 * Clasa de exceptii
 */
class ValidationException {
public:
    explicit ValidationException(const vector<string>& errors) : msg{ errors } {}

    friend ostream& operator<<(ostream& out, const ValidationException& ex);

    vector <string> msg;
};

ostream& operator<<(ostream& out, const ValidationException& ex);

class BadLuckException {
private:
    string msg;
public:
    explicit BadLuckException(const string& str) : msg{ str } {}

    friend ostream& operator<<(ostream& out, const BadLuckException& ex);
};

ostream& operator<<(ostream& out, const BadLuckException& ex);

/**
 * Clasa de entitati
 */
class Turism {
public:

    /**
     * Constructor
     * @param denumire
     * @param destinatie
     * @param tip
     * @param pret
     */
    Turism();
    Turism(const string& denumire, const string& destinatie, const string& tip, const int& pret);

    Turism(const Turism& t) = default;
    //gettee
    [[nodiscard]] string get_denumire() const {
        return denumire;
    }
    [[nodiscard]] string get_destinatie() const {
        return destinatie;
    }
    [[nodiscard]] string get_tip() const {
        return tip;
    }
    [[nodiscard]] int get_pret() const {
        return pret;
    }

    //suprascriem operatorul de egalitate
    bool operator==(const Turism& ot);

    //egalitate
    Turism& operator=(const Turism& ot);

private:
    string denumire;
    string destinatie;
    string tip;
    int pret;
};

/**
 * Clasa Validator
 */
class Validator {
public:
    /**
     * Functia de validare
     * @param denumire de validat
     * @param destinatie
     * @param tip
     * @param pret
     * @return un string de erori
     */
    static void validate(const string& denumire, const string& destinatie, const string& tip, const int& pret);
};

/**
 * Verfica daca un string are litere
 * @param S stringul de verificat
 * @return 0 sau 1 ca raspuns
 */
bool has_letters(const string& S);

string toMyString(vector<string> msg);

void test_domain();
