% 7
% a

reuniune([],M,M).

reuniune([H|Tail],M,Rez):-
    adauga(H,M),
    reuniune(Tail,M,Rez).

reuniune([H|Tail],M,[H|Rez]):-
    \+adauga(H,M),
    reuniune(Tail,M,Rez).

adauga(E,[E|_]).

adauga(E,[_|Tail]):-
    adauga(E,Tail).


% b

perechi([],[]).

perechi([_],[]).

perechi([H|Tail],Rez):-
    perechi_f(H,Tail,Perechi),
    perechi(Tail,PerechiT),
    adauga_sf(Perechi,PerechiT,Rez),!.

perechi_f(_,[],[]).

perechi_f(E,[H|Tail],[[E,H]|Rez]):-
    perechi_f(E,Tail,Rez).

adauga_sf([],L,L).

adauga_sf([H|Tail],L,[H|Rez]):-
    adauga_sf(Tail,L,Rez).
