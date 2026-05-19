% 13
% a

multime_ultime_aparitii(Lista, Multime) :-
    eliminare_ultime_duplicate(Lista, Multime).

eliminare_ultime_duplicate([], []).

eliminare_ultime_duplicate([H|T], Rezultat) :-
    membru(H, T),
    eliminare_ultime_duplicate(T, Rezultat).

eliminare_ultime_duplicate([H|T], [H|Rezultat]) :-
    \+ membru(H, T),
    eliminare_ultime_duplicate(T, Rezultat).

membru(X, [X|_]).

membru(X, [_|T]) :-
    membru(X, T).

% b

cmmdc(A,0,A).

cmmdc(A,B,D):-
    B > 0,
    Div is A mod B,
    cmmdc(B,Div,D).

cmmdc_list([X],X).

cmmdc_list([H|Tail],Di):-
    cmmdc_list(Tail,DTail),
    cmmdc(H,DTail,Di).
