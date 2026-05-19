#include "domain.h"
#include <assert.h>

Turism::Turism(const string& denumire, const string& destinatie, const string& tip, const int& pret)
{
    this->denumire = denumire;
    this->destinatie = destinatie;
    this->tip = tip;
    this->pret = pret;
}

bool Turism::operator==(const Turism& ot)
{
    if (denumire == ot.denumire && destinatie == ot.destinatie && tip == ot.tip && pret == ot.pret)
    {
        return true;
    }
    return false;
}

Turism::Turism()
{
    denumire = "";
    destinatie = "";
    tip = "";
    pret = -1;
}

Turism& Turism::operator=(const Turism& ot) = default;

bool has_letters(const string& S) {
    for (auto& ch : S) {
        if ('A' <= ch && ch <= 'Z' || 'a' <= ch && ch <= 'z') {
            return true;
        }
    }
    return false;
}

ostream& operator<<(ostream& out, const ValidationException& ex) {
    for (const auto& mess : ex.msg) {
        out << mess << "\n";
    }
    return out;
}

ostream& operator<<(ostream& out, const BadLuckException& ex) {
    out << ex.msg;
    return out;
}

void Validator::validate(
    const string& cdenumire,
    const string& cdestinatie,
    const string& ctip,
    const int& cpret)
{
    vector<string> errors;

    bool vden = has_letters(cdenumire);
    if (cdenumire.empty()) {
        errors.emplace_back("Denumirea nu poate fi vid");
    }
    else if (!vden) {
        errors.emplace_back("Denumirea trebuie sa contina minim o litera");
    }

    bool vdes = has_letters(cdestinatie);
    if (cdestinatie.empty()) {
        errors.emplace_back("Destinatia nu poate fi vid");
    }
    else if (!vdes) {
        errors.emplace_back("Destinatia trebuie sa contina litere");
    }

    bool vtip = has_letters(ctip);
    if (ctip.empty()) {
        errors.emplace_back("Tipul nu poate fi vid");
    }
    else if (!vtip) {
        errors.emplace_back("Tipul trebuie sa contina litere");
    }

    if (cpret <= 0) {
        errors.emplace_back("Pretul trebuie sa fie un numar natural nenul");
    }
    if (!errors.empty()) {
        throw ValidationException(errors);
    }
}

string toMyString(vector<string> msg) {
    string ans = "";
    for (const auto& mg : msg) {
        ans += mg;
        ans += "\n";
    }
    return ans;
}

void test_domain() {
    Turism tt;
    tt = Turism("Sejur", "Ibiza", "all-inclusive", 50000);
    assert(tt.get_pret() == 50000);
    Turism t = Turism("Sejur", "Ibiza", "all-inclusive", 50000);
    assert(t.get_denumire() == "Sejur");
    assert(t.get_destinatie() == "Ibiza");
    assert(t.get_tip() == "all-inclusive");
    assert(t.get_pret() == 50000);

    //test validator

    try {
        Validator::validate("", "Ibiza", "all-inclusive", 10);
        assert(false);
    }
    catch (ValidationException& val) {
        //cout<<val;
        assert(true);
    }

    try {
        Validator::validate("", "", "", -5);
        assert(false);
    }
    catch (ValidationException& val) {
        assert(true);
    }

    try {
        Validator::validate("Sejur", "Ibiza", "all-inclusive", -5);
        assert(false);
    }
    catch (ValidationException& val) {
        assert(true);
    }

    try {
        Validator::validate("Sejur", "Ibiza", "all-inclusive", 10);
        assert(true);
    }
    catch (ValidationException& val) {
        assert(false);
    }

    try {
        Validator::validate("Sejur", "", "all-inclusive", 10);
        assert(false);
    }
    catch (ValidationException& val) {
        assert(true);
        //cout<<val;
    }

    try {
        Validator::validate("Sejur", "Ibiza", "", 10);
        assert(false);
    }
    catch (ValidationException& val) {
        assert(true);
    }

    try {
        Validator::validate("-5748654", "-5748654", "-5748654", 10);
        assert(false);
    }
    catch (ValidationException& val) {
        assert(true);
    }

    //test has letters
    assert(has_letters("-5748654") == false);
    assert(has_letters("48654") == false);
    assert(has_letters("4d86a54") == true);
    assert(has_letters("a48654") == true);
    assert(has_letters("a48654") == true);
}