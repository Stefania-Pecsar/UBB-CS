function [S,dS]=evalsplineHermite(x,f,df,X)
S=[]; dS=[];
for i=1:length(X)
  if X(i)==x(end)
    S(i)=f(end);
    dS(i)=df(end);
  else
    poz=find(X(i)<x,1)-1;
    [S(i),dS(i)]=Hermite_interpolare(...
    x([poz poz+1]),f([poz poz+1]),df([poz poz+1]),X(i));
  endif
endfor
endfunction

