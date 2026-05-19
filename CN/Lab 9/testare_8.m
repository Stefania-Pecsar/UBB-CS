%AD = x1 + x2 + x3 =89
%AC = x1 + x2 =  67
%BD = x2 + x3 =53
% restul  e un sis supra det
A =[1 1 1; 1 1 0; 0 1 1; 1 0 0 ;0 0 1]
f = [89 67 53 35 20]'
[c,err]=linsys2(A,f)
