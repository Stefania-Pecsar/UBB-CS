 function [c,err]=linsys2(A,f)
   [Q,R]=qr(A);
   b=Q'*f;
   m=size(A,2);
   c=R(1:m,:)\b(1:m);% operatorul \ rezolva sisteme liniare
   err=norm(b(m+1:end));
 endfunction
