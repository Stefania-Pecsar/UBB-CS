A = [10 7 8 7; 7 5 6 5; 8 6 10 9; 7 5 9 10]'
b = [32 23 33 31]'
bp = [32.1 22.9 33.1 30.9]'
y = A\b # "\" rez sis liniare
yp = A\bp
Ap = [10 7 8.1 7.2; 7.08 5.04 6 5; 8 5.98 9.89 9; 6.99 4.99 9 9.98]'
yp2 = Ap\b

er_rel_in= errel(b,bp)
er_rel_out= errel(y,yp)
er_rel_out/er_rel_in
cond(A)

 for n=10:15
   cond(hilb(n))
 end

 for n=10:15
  ## t = -1 : 2/n : 1;
   t = 1./(1:n);
   cond(vander(t))
 end
 #pol_test
 condpol(poly(1:15),6)
