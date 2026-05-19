pkg load symbolic
syms x a b fa fb fm

m = (a+b)/2

L(x) = (x-m)*(x-b)/((a-m)*(a-b)) * fa + (x-a)*(x-b)/((m-a)*(m-b)) * fm + (x-a)*(x-m)/((b-a)*(b-m)) * fb

expand(L)
int(L,x,a,b)
Simpspn = simplify(int(L,x,a,b))
