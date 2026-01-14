% 1
% a

exista(_,[]):-false.
exista(X,[X|_]).
exista(X,[_|T]):-
    exista(X,T).

diferenta([],_,[]).

diferenta([H|Tail],N,[H|Rez]):-
    \+exista(H, N),
    diferenta(Tail,N,Rez).

diferenta([H|Tail],N,Rez):-
    exista(H,N),
    diferenta(Tail,N,Rez).

% b

e_par(X):-
    0 is X mod 2.

adauga([],[]).

adauga([H|T],[H,1|Rez]):-
    e_par(H),
    adauga(T,Rez).

adauga([H|T],[H|Rez]):-
    \+ e_par(H),
    adauga(T,Rez).

