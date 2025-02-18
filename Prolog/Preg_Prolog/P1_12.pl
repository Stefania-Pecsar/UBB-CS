% 12
% a

substituire(_,_,[],[]).

substituire(E,Elem,[E|Tail],[Elem|Tail]).

substituire(E,Elem,[H|Tail],[H|RezTail]):-
    substituire(E,Elem,Tail,RezTail),!.

% b

sublista_1([],_, _, _,[]):-!.

sublista_1([H|Tail],M,N,I,[H|Rez]):-
    I >= M,
    I =< N,!,
    Poz is I + 1,
    sublista_1(Tail,M,N,Poz,Rez).

sublista_1([_|Tail],M,N,I,Rez):-
    I > N,!,
    Poz is I + 1,
    sublista_1(Tail,M,N,Poz,Rez).

sublista_1([_|T], M, N, I, Rez):-
    I < M, !,
    Index is I + 1,
    sublista_1(T, M, N, Index, Rez).
