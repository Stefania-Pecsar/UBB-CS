% 10
% a

intercaleaza(Elem,0,[],[Elem]).

intercaleaza(_,Poz,[],_):-
    Poz>0,!,false.

intercaleaza(Elem,0,[H|Tail],[Elem,H|Tail]).

intercaleaza(Elem,Poz,[H|Tail],[H|Rez]):-
    Poz>0,
    Poz1 is Poz-1,
    intercaleaza(Elem,Poz1,Tail,Rez).


% b

cmmdc(A,0,A).

cmmdc(A,B,D):-
    B>0,
    Div is A mod B,
    cmmdc(B,Div,D).

cmmd_lista([X],X).

cmmd_lista([H|Tail],D):-
    cmmd_lista(Tail,DTail),
    cmmdc(H,DTail,D).
