function T = reptrapezium(f,a,b,n)
  h = (b-a)/n;
  x = (a+h): h:(b-h);
  T = h * (sum(f(x)) + h/2*(f(a) +f(b)));
