function L=Newton_interpolare(x,f,X)
 c=dif_div(x,f)(1,:);
 L=[];
 for k=1:length(X)
   P=1; L(k)=c(1);
   for i=1:length(x)-1
     P*=(X(k)-x(i));
     L(k)+=c(i+1)*P;
   endfor
 end
end
