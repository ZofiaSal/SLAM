function [p_r, PR_r, PR_p] = toFrame3D(r, p)
% transforms point P from global frame to frame r (to r being center of coordinate)
p_xy = p(1:2);
t = r(1:2);
a = r(3);

R = [cos(a) -sin(a) ; sin(a) cos(a)];

p_r_xy = R' * (p_xy - t);
p_r(1:2) = p_r_xy;
p_r(3) = p(3);

if nargout > 1
    px = p(1);
    py = p(2);
    x = t(1);
    y = t(2);

    PR_r = [...
        [ -cos(a), -sin(a),   cos(a)*(py - y) - sin(a)*(px - x)]
        [  sin(a), -cos(a), - cos(a)*(px - x) - sin(a)*(py - y)]
        [       0,       0,                                   0]];

    PR_p = [...
      [cos(a)   , sin(a), 0]
      [-sin(a)  , cos(a), 0]
      [0        , 0     , 1]];
end

end

%%
function f()
%%
syms x y a px py real
r = [x y a]';
p = [px py]';
p_r = toFrame2D(r, p);
PR_r = jacobian(p_r, r)
end