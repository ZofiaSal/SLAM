function [p, P_r, P_pr] = fromFrame3D(r, p_r)

t = r(1:2);
a = r(3);

R = [cos(a) -sin(a) ; sin(a) cos(a)];

p_r_xy = p_r(1:2);

p(1:2) = R*p_r_xy + t;
p(3) = p_r(3);

if nargout > 1
    px = p_r(1);
    py = p_r(2);

    P_r = [...
        [ 1, 0, - py*cos(a) - px*sin(a)]
        [ 0, 1,   px*cos(a) - py*sin(a)]
        [ 0, 0, 0]];

    P_pr = [...
      [cos(a) , -sin(a) , 0]
      [sin(a) , cos(a)  , 0]
      [0      , 0       , 1]];

end

end

%%
function f()
%%
syms x y a px py real
r = [x y a]';
p_r = [px py]';
p = fromFrame2D(r, p_r);
P_r = jacobian(p, r)
end
