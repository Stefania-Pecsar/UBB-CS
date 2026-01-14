% 1
% a

suma(L1,L2,Suma):-
    inversare(L1,L1Inv),
    inversare(L2,L2Inv),
    suma_lista_inv(L1Inv,L2Inv,0,SumInv),
    inversare(SumInv,Suma).

suma_lista_inv([],[],0,[]).

suma_lista_inv([],[],Transport,[Transport]):-
    Transport > 0.

suma_lista_inv([],[Y|T2],Transport,[S|Rest]):-
    S is(Y + Transport) mod 10,
    NouTransport is (Y + Transport) // 10,
    suma_lista_inv([],T2,NouTransport,Rest).

suma_lista_inv([X|Tail1],[Y|Tail2],Transport,[S|Rest]):-
    S is (X + Y + Transport) mod 10,
    NouTransport is (X + Y + Transport) // 10,
    suma_lista_inv(Tail1, Tail2, NouTransport, Rest).

inversare([],[]).
inversare([H|Tail],Inv):-
    inversare(Tail,InvT),
    concat(InvT,[H],Inv).

concat([],L,L).
concat([H|Tail],L,[H|Rez]):-
    concat(Tail,L,Rez).
