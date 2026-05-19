clc
format rat
%Lagrange cu Newton

x = 1:5
f = [14 2 17 23 13]
T = dif_div(x,7)

X = linspace(1,5,1000);
LX = Newton_interpolare(x,f,X);
plot(X,LX)

clf
hold on
plot(X,LX,'-','color','blue','linewidth', 2)
plot(x, f ,'o','color','red','markerfacecolor','red')
grid on

%Hermite
timpi = [0 3 5 8 13];
distante = [0 255 383 623 993];
viteze = [75 77 80 74 72];

x = linspace(0,13,1000); %diviziune a intervalului de timp
[H,dH] = Hermite_interpolare(timpi,distante,viteze,X);

clf
hold on
plot(H,dH,'-', 'color','blue','linewidth',1.5)
plot(distante,viteze,'o','color','red','markerfacecolor','red')
