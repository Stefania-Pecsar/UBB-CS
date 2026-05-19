function [I,NIter]=adquad(f,a,b,err=1e-13)
  I1=repsimpson(f,a,b,1);
  I2=repsimpson(f,a,b,2);
  I1=(16*I2-I1)/15;
  NIter=2;
  if abs(I1-I2)<err
    I=I1;
  else
    [I1,NIter1]=adquad(f,a,(a+b)/2,err);
    [I2,NIter2]=adquad(f,(a+b)/2,b,err);
    I=I1+I2;
    NIter=NIter1+NIter2;
  end
 end