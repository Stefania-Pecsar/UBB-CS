function x=GaussElimNaiv(A,b)
  A=[A b];
  for i=1:length(b)-1
    pivpos=i;
    while A(i,pivpos)==0
      pivpos++;
    endwhile
    if pivpos>i
      A([i pivpos],i:end)=A([pivpos i],i:end);
    endif
    for k=i+1:length(b)
      A(k,i:end)=A(k,i:end)-(A(k,i)/A(i,i))*A(i,i:end);
    endfor
  endfor
  A
  x=bkwsubs(A(:,1:end-1),A(:,end));
endfunction
