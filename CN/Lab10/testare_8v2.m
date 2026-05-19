clc
f = @(x) 4./(1+x.^2)
R = reprectangle(f,0,1,100)
T = reptrapezium(f,0,1,100)
S = repsimpson(f,0,1,100)

pkg load symbolic
syms x

primitiva = int(f(x))
integrala = int(f(x),0,1)

fplot(f,[0,1],N = 1000)
axis([0 1 0 4])
T = romberg(f,0,1,4)
