function R = reprectangle(f,a,b,n)
  h=(b-a)/n;
  mids = f((a+h/2):h:(b-h/2));
  R = h * sum(mids);
