A = magic(6)
tril(A)
triu(A)
#length(A)
#ones(1, length(A))
b = triu(A)*ones(length(A),1)
x = bkwsubs(triu(A),b)

b = triu(A)*ones(length(A),1)
x = fwdsubs(triu(A),b)

A = randi(10,10)
b = triu(A)*ones(length(A),1)
x = GaussElimPivot(A,b)

n=5
A = tril(-ones(n+1,n+1)) + 2*eye(n+1);
A(:,end) = 1;
A

b = (2 : -1 : -n+2 )'
x = GaussElimPivot(A,b)

x = Gausselimscaled(A,b)

[L,U,P] = lup(A)

sol_sys_lup(A,b)

A = A+A'
R = Cholesky(A)
R*R'
