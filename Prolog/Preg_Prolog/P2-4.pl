% 4
% a

interclasare([],[],[]).

interclasare([],L,L).

interclasare(L,[],L).

interclasare([H1|Tail1],[H2|Tail2],[H1|Rez]):-
    H1 < H2,
    interclasare(Tail1,[H2|Tail2],Rez).

interclasare([H1|Tail1],[H2|Tail2],[H2|Rez]):-
     H1 > H2,
     interclasare([H1|Tail1],Tail2,Rez).

interclasare([H|Tail1],[H|Tail2],[H|Rez]):-
    interclasare(Tail1,Tail2,Rez).
