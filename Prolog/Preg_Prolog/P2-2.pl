% 2
% a

adaugare_sf(Elem,[],[Elem]).

adaugare_sf(Elem,[H|Tail],[Elem,H|Tail]):-
           Elem =< H, !.


adaugare_sf(Elem,[H|Tail],[H|Tail1]):-
            Elem > H,
            adaugare_sf(Elem,Tail,Tail1).


sortare([],[]).

sortare([H|Tail],ListaSortata):-
    sortare(Tail,SortPartial),
    adaugare_sf(H,SortPartial,ListaSortata).

