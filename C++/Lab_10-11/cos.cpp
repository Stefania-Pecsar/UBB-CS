#include "cos.h"
#include <random>
#include <fstream>
#include <assert.h>

Cos::Cos() 
{
    comp.clear();
}

void Cos::add_to_cos(const Turism& t)
{
    comp.push_back(t);
    notify();
}

void Cos::empty_cos()
{
    comp.clear();
    notify();
}

void Cos::random_add(const vector<Turism>& elems, const int& q) {
    std::mt19937 mt{ std::random_device{}() };
    std::uniform_int_distribution<> dist(0, elems.size() - 1);
    for (int i = 0; i < q; ++i) {
        int nr = dist(mt);
        add_to_cos(elems[nr]);
    }
    notify();
}

void Cos::save_to_file(const string& filename) {
    ofstream fout(filename);
    fout << "First cell\n";
    fout << "Nrcrt. Nume Prod Subst Pret\n";
    int i = 0;
    for (auto& tur : comp) {
        fout << i++ << " " << tur.get_denumire() << " " << tur.get_destinatie() << " " << tur.get_tip() << " " << tur.get_pret() << "\n";
    }
}

vector<Turism>& Cos::get_all() {
    return comp;
}