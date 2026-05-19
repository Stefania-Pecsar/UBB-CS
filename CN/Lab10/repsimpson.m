function S = repsimpson(f,a,b,n)
  h=(b-a)/n;
  x = a : h :b ;
  mids = f((a+h/2):h:(b-h/2));
  S = h/6 * (f(a) + f(b) + 2 * sum(f(x)) + 4*sum(f(mids)));
