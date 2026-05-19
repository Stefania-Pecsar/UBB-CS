#include "repo.h"
#include <fstream>
#include <assert.h>

void Repo::add_turism(const Turism& a)
{
	this->elems.push_back(a);
}

void Repo::modify_turism(const Turism& a, int poz)
{
	this->elems[poz] = a;
}

vector<Turism>& Repo::get_elems()
{
	return elems;
}

void Repo::delete_turism(int poz)
{
	this->elems.erase(elems.begin() + poz);
}

ostream& operator<<(ostream& out, const RepoException& ex)
{
	for (const auto& mesg : ex.msg)
	{
		out << mesg << "\n";
	}
	return out;
}

FileRepo::FileRepo(string fn)
{
	filename = move(fn);
	load_from_file();
}

void FileRepo::load_from_file() 
{
    ifstream fin(filename);
    string str;
    while (getline(fin, str))
    {
        stringstream ss(str);

        string word;
        vector<string> tur;
        while (getline(ss, word, ';'))
        {
            tur.push_back(word);
        }
        int nr = 0;
        for (auto& ch : tur[3]) 
        {
            nr = nr * 10 + (ch - '0');
        }
        Repo::add_turism(Turism(tur[0], tur[1], tur[2], nr));
    }
    fin.close();
}

void FileRepo::save_to_file()
{
    ofstream fout(filename);
    int index = 0;
    for (auto& it : Repo::get_elems())
    {
        fout << it.get_denumire() << ";" << it.get_destinatie() << ";" << it.get_tip() << ";" << it.get_pret();
        ++index;
        if (index != Repo::get_elems().size())
        {
            fout << "\n";
        }
    }
    fout.close();
}

void RepoProb::add_turism(const Turism& m) 
{
    det_luck();
    elems.insert(make_pair(elems.size(), m));
}

void RepoProb::modify_turism(const Turism& m, int poz) 
{
    det_luck();
    for (auto& it : elems) {
        if (it.first == poz) {
            elems.erase(poz);
            elems.insert(make_pair(poz, m));
            break;
        }
    }
}

void RepoProb::delete_turism(int poz)
{
    det_luck();
    elems.erase(poz);
    map<int, Turism> sec;
    sec.clear();
    for (auto& it : elems) {
        sec.insert(make_pair(sec.size(), it.second));
    }
    elems = sec;
}
vector<Turism> all;
vector<Turism>& RepoProb::get_elems() 
{
    det_luck();
    all.clear();
    for (auto& it : elems) {
        all.push_back(it.second);
    }
    return all;
}

RepoProb::RepoProb(float chance) 
{
    prob = chance;
    elems.clear();
}

void RepoProb::det_luck() 
{
    auto prb = int(prob * 10);
    int nr = rand() % 10 + 1;
    if (nr <= prb) {
        return;
    }
    throw BadLuckException("Putina teapa!\n");
}

void test_repo() 
{
    Repo repo;
    Turism t = Turism("Sejur", "Ibiza", "all-inclusive", 500);

    //test add elem & test get elems
    repo.add_turism(t);
    vector<Turism> tv;
    tv = repo.get_elems();

    assert(tv.size() == 1);
    assert(tv[0].get_denumire() == "Sejur");
    assert(tv[0].get_destinatie() == "Ibiza");
    assert(tv[0].get_tip() == "all-inclusive");
    assert(tv[0].get_pret() == 500);

    //test modify elem
    Turism t1 = Turism("Sejur", "Paris", "all-inclusive", 10);
    repo.modify_turism(t1, 0);

    tv = repo.get_elems();

    assert(tv.size() == 1);
    assert(tv[0].get_denumire() == "Sejur");
    assert(tv[0].get_destinatie() == "Paris");
    assert(tv[0].get_tip() == "all-inclusive");
    assert(tv[0].get_pret() == 10);

    //test delete elems
    repo.add_turism(t);
    repo.delete_turism(0);

    tv = repo.get_elems();

    assert(tv.size() == 1);
    assert(tv[0].get_denumire() == "Sejur");
    assert(tv[0].get_destinatie() == "Ibiza ");
    assert(tv[0].get_tip() == "all-inclusive");
    assert(tv[0].get_pret() == 500);

    FileRepo frp{ "test_file.txt" };

    frp.add_turism(Turism("Sejur", "Paris", "all-inclusive", 10));

    auto prp = RepoProb(1);
    prp.add_turism(Turism("Sejur", "Ibiza", "all-inclusive", 500));

    tv = prp.get_elems();

    assert(tv.size() == 1);
    assert(tv[0].get_denumire() == "Sejur");
    assert(tv[0].get_destinatie() == "Ibiza");
    assert(tv[0].get_tip() == "all-inclusive");
    assert(tv[0].get_pret() == 500);

    prp.modify_turism(Turism("Nush", "Ibiza", "ultra", 10), 0);

    tv = prp.get_elems();

    assert(tv.size() == 1);
    assert(tv[0].get_denumire() == "Nush");
    assert(tv[0].get_destinatie() == "Ibiza");
    assert(tv[0].get_tip() == "ultra");
    assert(tv[0].get_pret() == 10);

    prp.add_turism(Turism("Sejur", "Ibiza", "all-inclusive", 500));

    tv = prp.get_elems();

    assert(tv.size() == 2);

    prp.delete_turism(0);

    tv = prp.get_elems();

    assert(tv.size() == 1);

    auto noch = RepoProb(0);

    try 
    {
        noch.add_turism(Turism("Sejur", "Ibiza", "all-inclusive", 500));
        assert(false);
    }
    catch (BadLuckException& re)
    {
        assert(true);
    }
}