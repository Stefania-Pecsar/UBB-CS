% 14
% a

predecesor([],1,[]):-!.

predecesor([H|Tail],Transport,[Cifra|Rez]):-
    predecesor(Tail,TransC,Rez),
    (H =:= 0 -> Cifra is 10 - TransC, Transport = 1;
     Cifra is H - TransC, Transport = 0).

main14(L,Rez):-
    L=[0], !,
    Rez = -1.

main14(L,Rez):-
    predecesor(L,_,[H|Tail]),
    (H =:= 0 -> Rez = Tail;Rez = [H|Tail]).
