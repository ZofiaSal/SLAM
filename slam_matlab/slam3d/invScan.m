function [p, P_y] = invScan(y)

d = y(1);
a = y(2);
pz = y(3);

px = d * cos(a);
py = d * sin(a);

p = [px;py;pz];

if nargout > 1

   P_y = [...
       cos(a) -d*sin(a) 0
       sin(a)  d*cos(a) 0
       0        0       1];

end
