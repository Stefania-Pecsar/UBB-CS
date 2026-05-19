function Runge_exemplu(type={'echidistante','Cebisev2'},col={'r','g'},m=5)
%Runge_exemplu(type={'echidistante','Cebisev1','Cebisev2'},col={'r','g','m'},m=11)
  clf; hold on; grid on; xlim([-5 5]); xticks(-5:5);axis square;
  f=@(x) 1./(1+x.^2);
  x=linspace(-5,5,501);
  plot(x,f(x),'b','linewidth',2);
  l={'f'};
  for i=1:length(type)
   nodes=gen_nodes(-5,5,m,type{i});
   values=f(nodes);
   plot(nodes,values,'ok','markerfacecolor',col{i},'markersize',8);
   plot(x,LagrangeBary(nodes,values,x),col{i},'linewidth',2)
   l{end+1}=type{i};
   l{end+1}=['L cu ' type{i}];
  endfor
  legend(l,"location", "northeastoutside")
  set(gca,"fontsize", 17)
  axis([-5.5 5.5 -0.5 1.5])
