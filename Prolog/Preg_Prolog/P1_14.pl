% 14
% a

membrul(X,[X|_]).
membrul(X,[_|Tail]):-
    membrul(X,Tail).

submultime([],_).

submultime([H|Tail],Rez):-
    membrul(H,Rez),
    submultime(Tail,Rez).

multimi_egale(M1,M2):-
    submultime(M1,M2),
    submultime(M2,M1).

% b

pozitie([],_,_).

pozitie([H|_],1,H).

pozitie([_|Tail],Poz,E):-
    Poz > 1,
    Poz1 is Poz - 1,
    pozitie(Tail,Poz1,E).

