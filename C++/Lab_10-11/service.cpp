#include "service.h"

#include <assert.h>
#include <algorithm>
#include <fstream>
#include <memory>

using std::sort;

Service::Service(AbsRepo* rp, Validator& vd) 
{
    repo = rp;
    valid = vd;
    undo_act.clear();
}

vector<Turism >& Service::get_all_ent() 
{
    return repo->get_elems();
}

void Service::add(const string& cdenumire, const string& cdestinatie, const string& ctip, const int& cpret)
{
    Validator::validate(cdenumire, cdestinatie, ctip, cpret);
    auto t = Turism(cdenumire, cdestinatie, ctip, cpret);
    auto& v = repo->get_elems();
    vector<string> err;
    for (auto& it : v) 
    {
        if (it == t)
        {
            err.emplace_back("Element deja existent");
        }
    }
    if (!err.empty())
    {
        throw RepoException(err);
    }
    repo->add_turism(t);
    undo_act.push_back(new UndoAdd(repo, t));
}

void Service::modify(const int& poz, const string& cdenumire, const string& cdestinatie, const string& ctip, const int& cpret)
{
    Validator::validate(cdenumire, cdestinatie, ctip, cpret);
    vector<string> err;
    if (poz < 0 || poz >= repo->get_elems().size())
    {
        err.emplace_back("Pozitie invalida");
        throw RepoException(err);
    }
    auto t = repo->get_elems()[poz];
    repo->modify_turism(Turism(cdenumire, cdestinatie, ctip, cpret), poz);
    undo_act.push_back(new UndoMod(repo, t, poz));
}

void Service::del(const int& poz) 
{
    vector<string> err;

    if (poz < 0 || poz >= repo->get_elems().size()) 
    {
        err.emplace_back("Pozitie invalida");
        throw RepoException(err);
    }
    auto dlt = repo->get_elems()[poz];
    repo->delete_turism(poz);
    undo_act.push_back(new UndoDel(repo, dlt, poz));
}

bool Service::search(const string& cdenumire, const string& cdestinatie, const string& ctip, const int& cpret)
{
    //vector<string> err;

    Validator::validate(cdenumire, cdestinatie, ctip, cpret);

    auto t = Turism(cdenumire, cdestinatie, ctip, cpret);

    auto it = find_if(repo->get_elems().begin(), repo->get_elems().end(), [=](Turism& tur) {
        return tur.get_denumire() == t.get_denumire() && tur.get_pret() == t.get_pret() && tur.get_tip() == t.get_tip() &&
            tur.get_destinatie() == t.get_destinatie();
        });

    return it < repo->get_elems().end();

}

void Service::filter(int crit, const string& val, vector<Turism>& rez) 
{
    if (crit == 0) 
    {
        vector <string> err;
        int prc = 0;
        bool vld = true;
        for (auto& ch : val) {
            if ('0' <= ch && ch <= '9') {
                prc = prc * 10 + (ch - '0');
            }
            else {
                vld = false;
            }
        }
        if (!vld) {
            err.emplace_back("Pret invalid");
            throw RepoException(err);
        }

        rez.clear();
        copy_if(repo->get_elems().begin(), repo->get_elems().end(), back_inserter(rez), [=](Turism& t) {
            return t.get_pret() == prc;
            });
        return;
    }

    rez.clear();
    copy_if(repo->get_elems().begin(), repo->get_elems().end(), back_inserter(rez), [=](Turism& t) {
        return t.get_destinatie() == val;
        });

}

bool crit_0(const Turism& el1, const Turism& el2) {
    return el1.get_denumire() < el2.get_denumire();
}

bool crit_1(const Turism& el1, const Turism& el2) {
    return el1.get_destinatie() < el2.get_destinatie();
}

bool crit_2(const Turism& el1, const Turism& el2) {
    return el1.get_tip() < el2.get_tip() || (el1.get_tip() == el2.get_tip() &&
        el1.get_pret() < el2.get_pret());
}

void Service::sort(int crit, vector<Turism>& rez) {
    rez = repo->get_elems();
    if (crit == 0) {
        ::sort(rez.begin(), rez.end(), crit_0);
    }
    else if (crit == 1) {
        ::sort(rez.begin(), rez.end(), crit_1);
    }
    else if (crit == 2) {
        ::sort(rez.begin(), rez.end(), crit_2);
    }
}

void Service::undo() {
    if (undo_act.empty()) {
        vector<string> err;
        err.emplace_back("Nu exista operatii la care sa se faca undo");
        throw RepoException(err);
    }
    ActUndo* act = undo_act.back();
    act->doUndo();
    undo_act.pop_back();
    delete act;
}

void test_service() {
    auto* r = new FileRepo("chaos.txt");
    auto v = Validator();

    auto s = Service(r, v);


    //test add
    s.add("Sejur", "Ibiza", "all-inclusive", 10);

    vector<Turism> mv;
    mv = s.get_all_ent();
    assert(mv[0].get_pret() == 10);
    assert(mv[0].get_denumire() == "Sejur");
    assert(mv[0].get_destinatie() == "Ibiza");
    assert(mv[0].get_tip() == "all-inclusive");


    try {
        s.add("", "Ibiza", "all-inclusive", 10);
        assert(false);
    }
    catch (ValidationException& ex) {
        assert(true);
    }

    try {
        s.add("Sejur", "", "all-inclusive", 10);
        assert(false);
    }
    catch (ValidationException& ex) {
        assert(true);
        //cout<<ex;
    }

    try {
        s.add("Sejur", "Ibiza", "", 10);
        assert(false);
    }
    catch (ValidationException& ex) {
        assert(true);
    }

    try {
        s.add("Sejur", "Ibiza", "all-inclusive", -5);
        assert(false);
    }
    catch (ValidationException& ex) {
        assert(true);
    }

    try {
        s.add("57486", "Ibiza", "all-inclusive", 10);
        assert(false);
    }
    catch (ValidationException& ex) {
        assert(true);
    }

    try {
        s.add("Sejur", "5788", "all-inclusive", 10);
        assert(false);
    }
    catch (ValidationException& ex) {
        assert(true);
    }

    try {
        s.add("Sejur", "Ibiza", "95874", 10);
        assert(false);
    }
    catch (ValidationException& ex) {
        assert(true);
    }

    //test mod
    s.modify(0, "Vacanta", "Paris", "all-inclusive", 15);

    mv = s.get_all_ent();

    assert(mv[0].get_pret() == 15);
    assert(mv[0].get_denumire() == "Vacanta");
    assert(mv[0].get_destinatie() == "Paris");
    assert(mv[0].get_tip() == "all-inclusive");

    try {
        s.modify(-5, "Vacanta", "Paris", "all-inclusive", 15);
        assert(false);
    }
    catch (RepoException& re) {
        assert(true);
    }

    try {
        s.modify(8, "Vacanta", "Paris", "all-inclusive", 15);
        assert(false);
    }
    catch (RepoException& re) {
        assert(true);
    }

    //test del
    s.add("Vacanta", "Paris", "all-inclusive", 10);

    //+test_search
    assert(s.search("Vacanta", "Paris", "all-inclusive", 10) == 1);
    assert(s.search("Vacanta", "Pars", "all-inclusive", 10) == 0);

    s.del(0);
    mv = s.get_all_ent();

    assert(mv[0].get_pret() == 10);
    assert(mv[0].get_denumire() == "Vacanta");
    assert(mv[0].get_denumire() == "Paris");
    assert(mv[0].get_tip() == "all-inclusive");

   

    try {
        s.add("Vacanta", "Paris", "all-inclusive", 10);
        assert(false);
    }
    catch (RepoException& re) {
        assert(true);
    }

    s.del(0);
    try {
        s.del(-8);
        assert(false);
    }
    catch (RepoException& re) {
        assert(true);
    }

    try {
        s.del(7);
        assert(false);
    }
    catch (RepoException& re) {
        assert(true);
        //cout<<re;
    }

    //filter test
    s.add("Vacanta", "Paris", "all-inclusive", 10);
    s.add("Serviciu", "Viena", "all-inclusive", 5);
    s.add("Balneo", "Viena", "mic-dejun inclus", 10);


    {
        vector<Turism> res;
        s.filter(1, "Viena", res);
        assert(res.size() == 2);
        assert(res[0].get_pret() == 10);
        assert(res[0].get_tip() == "mic-dejun inclus");
        assert(res[0].get_destinatie() == "Viena");
        assert(res[0].get_denumire() == "Balneo");

        assert(res[1].get_pret() == 5);
        assert(res[1].get_tip() == "all-inclusive");
        assert(res[1].get_destinatie() == "Viena");
        assert(res[1].get_denumire() == "Serviciu");
    }

    {
        vector<Turism> res;
        s.filter(0, "10", res);
        assert(res.size() == 2);
        assert(res[0].get_pret() == 10);
        assert(res[0].get_tip() == "all-inclusive");
        assert(res[0].get_destinatie() == "Paris");
        assert(res[0].get_denumire() == "Vacanta");

        assert(res[1].get_pret() == 10);
        assert(res[1].get_tip() == "mic-dejun inclus");
        assert(res[1].get_destinatie() == "Viena");
        assert(res[1].get_denumire() == "Balneo");

        try {
            s.filter(0, "a3", res);
            assert(false);
        }
        catch (...) {
            assert(true);
        }
    }

    //sort

    {
        vector<Turism> res;
        s.sort(0, res);
        assert(res.size() == 3);
        assert(res[0].get_denumire() == "Balneo");
        assert(res[1].get_denumire() == "Serviciu");
        assert(res[2].get_denumire() == "Vacanta");
    }

    {
        vector<Turism> res;
        s.sort(1, res);
        assert(res.size() == 3);
        assert(res[0].get_denumire() == "Vacanta");
        assert(res[1].get_denumire() == "Balneo");
        assert(res[2].get_denumire() == "Serviciu");
    }

    {
        vector<Turism> res;
        s.sort(2, res);
        assert(res.size() == 3);
        assert(res[0].get_denumire() == "Serviciu");
        assert(res[1].get_denumire() == "Vacanta");
        assert(res[2].get_denumire() == "Balneo");
    }

    ofstream dll("chaos.txt");
    dll.close();

    delete r;
}