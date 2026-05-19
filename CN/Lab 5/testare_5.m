clc
n = 10
A = diag(5*ones(n,1)) + diag(-ones(n-1,1),1) + diag(-ones(n-1,1),-1)
b = [4;3*ones(n-2,1);4]

[Jacobi_it(A,b,10) GS_it(A,b,10) SOR_it(A,b,1.039,10)]

#A = magic(5)
#diag(A)
#diag(1:5)
#diag(diag(A))
#tril(A)

[x,ni,rho_J]=Jacobi(A,b)
[x,ni,rho]=GS(A,b)
omega = 2/ (1+sqrt(1-rho_J^2))
[x,ni,rho]=SOR(A,b,omega)
