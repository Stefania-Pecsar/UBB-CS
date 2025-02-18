% 15
% a

par([]).

par([_,_|Tail]):-
    par(Tail).

% b

min([X],X).

min([H|Tail],H):-
    min(Tail,MinT),
    H =< MinT.

min([H|Tail],MinT):-
    min(Tail,MinT),
    H > MinT.

elimina_min(Lista,Rez):-
    min(Lista,Min),
    elimina_prim(Min,Lista,Rez).


elimina_prim(_, [], []).
elimina_prim(Elem, [Elem|T], T) :- !.
elimina_prim(Elem, [H|T], [H|Rez]) :-
    elimina_prim(Elem, T, Rez).
