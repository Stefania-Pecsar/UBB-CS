function [H,dH]=Hermite_interpolare(x,f,df,X)
 c=dif_div_duble(x,f,df)(1,:);
 z=repelem(x,2);
 H=[];dH=[];
 for k=1:length(X)
   P=1; DP=0; H(k)=c(1); dH(k)=0;
   for i=1:length(z)-1
     DP=DP*(X(k)-z(i))+P;
     P*=(X(k)-z(i));
     H(k)+=c(i+1)*P;
     dH(k)+=c(i+1)*DP;
   endfor
 end
end