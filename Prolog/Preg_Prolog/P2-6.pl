% 6
% a

inloc([],_,_,[]).

inloc([E|Tail],E,L1,Rez):-
    inloc(Tail,E,L1,R1),
    concat(L1,R1,Rez).

inloc([H|T],E,L1,[H|R]):-
    H \= E,
    inloc(T,E,L1,R).

concat([],L,L).

concat([H|T],L,[H|R]):-
    concat(T,L,R).
