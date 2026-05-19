clc
pkg load symbolic

#syms x
#nodes = [0 1 2 3]
#f(x) = x.^3 +  x.^ 2 + x + 1
#values = f(nodes)
#L(x)=lagrange_sym(nodes,values)
#L(nodes)
#f pol de gr cel mai mare(nodes -1) => L = f

#sgrt(115)

nodes = [100 121 144 81] # patrate perfecte
values = [10 11 12 9] #rad
L(x)=lagrange_sym(nodes,values)
L(115)

aprox1 = double(L(115))
aprox2 = LagrangeBary(nodes, values, 115)
exact = sqrt(115)
err=abs(aprox1 - exact)


f(x) = sqrt(x)
syms csi
df_4(csi) = subs(diff(f,x,4),x,csi)
R_f_115(csi) = abs(prod(115 - nodes) / factorial(sym(4)) * df_4(csi))
err_max = double(subs(R_f_115,csi,81))

