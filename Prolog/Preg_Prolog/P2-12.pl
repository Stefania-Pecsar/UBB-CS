% 12
% a

inlocuiste([],_,_,[]).

inlocuieste([E|Tail],E,L1,Rez):-
    inlocuieste(Tail,E,L1,R1),
    concat(L1,R1,Rez).

inlocuieste([H|T],E,L1,[H|R]):-
    H \= E,
    inlocuieste(T,E,L1,R).

concat([],L,L).

concat([H|T],L,[H|R]):-
    concat(T,L,R).
