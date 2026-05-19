 function [nodes,coefs,pin]=gauss_quad_sym(w,x,a,b,n)
  pi0=sym(0); pi1=sym(1);
  int_pi1=int(w,a,b);
  alpha=int(x*pi1^2*w,a,b)/int_pi1;
  beta=int_pi1;
  for k=1:n
    pin=(x-alpha)*pi1-beta*pi0;
    pi0=pi1;pi1=pin;
    int_pi0=int_pi1;
    int_pi1=int(pi1^2*w,a,b);
    alpha=int(x*pi1^2*w,a,b)/int_pi1;
    beta=int_pi1/int_pi0;
  endfor
  pin=expand(pin);
  nodes=simplify(solve(pin==0))';
  coefs=sym([]);
  for k=1:n
   coefs(k)=simplify(int(prod(x-nodes([1:k-1,k+1:n]))...
                     *w,a,b)/subs(diff(pin),nodes(k)));
  endfor
 endfunction 