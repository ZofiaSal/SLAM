% SLAM algorithm

% I. INITIALIZE
%
%   0. System def.

% [dx,angle,z]
LM_SIZE = 3;

%getting data 
%CHANGE THIS NAME TO THE NAME OF THE FILE YOU WANT TO USE
%DESCRIPTION OF THE FILE STRUCTRUCTURE IS IN THE README FILE
filename = "data/circle_points.csv";
data_from_file = csvread(filename);

[dummy, dummy, NUMBER_OF_LANDMARKS] = data(data_from_file);
SIZE_OF_ALL_LANDMARKS = LM_SIZE * NUMBER_OF_LANDMARKS;

max_loop=200;

% System noise
q = [0.1;0.3];
Q = diag(q.^2);

% Measurement noise
m = [.15; 1*pi/180; .015];
M = diag(m.^2);

%
%   1. Simulator
%       R: robot pose u: control

R = [0;0;0];
y = zeros(LM_SIZE, NUMBER_OF_LANDMARKS);
x_no_slam = R;

%   2. Estimator
x = zeros(numel(R)+SIZE_OF_ALL_LANDMARKS, 1);
P = zeros(numel(x),numel(x));
mapspace = 1:numel(x); %map management
l = zeros(LM_SIZE, NUMBER_OF_LANDMARKS); %pointers to landmarks in x

r = find(mapspace,numel(R));
mapspace(r) = 0;
x(r)   = R;
P(r,r) = 0;

%   3. Graphics
mapFig = figure(1);
cla;
size = 7;
axis([-size size -size size])
axis square
RG = line('parent',gca,...
    'marker','.',...
    'color','r',...
    'xdata',R(1),...
    'ydata',R(2));
rG = line('parent',gca,...
    'linestyle','none',...
    'marker','+',...
    'color','b',...
    'xdata',x(r(1)),...
    'ydata',x(r(2)));

lG = line('parent',gca,...
    'linestyle','none',...
    'marker','+',...
    'color','b',...
    'xdata',[],...
    'ydata',[]);


%past real positions
prG = zeros(1,max_loop);
for i = 1:numel(prG)
    prG(i) = line(...
        'parent', gca,...
        'marker','.',...
        'color','r',...
        'xdata',[],...
        'ydata',[]);
end
%past no slam positions
pnG = zeros(1,max_loop);
for i = 1:numel(pnG)
    pnG(i) = line(...
        'parent', gca,...
        'marker','.',...
        'color','g',...
        'xdata',[],...
        'ydata',[]);
end

%past our positions
poG = zeros(1,max_loop);
for i = 1:numel(poG)
    poG(i) = line(...
        'parent', gca,...
        'marker','.',...
        'color','b',...
        'xdata',[],...
        'ydata',[]);
end

eG = zeros(1,NUMBER_OF_LANDMARKS);
for i = 1:numel(eG)
    eG(i) = line(...
        'parent', gca,...
        'color','g',...
        'xdata',[],...
        'ydata',[]);
end

reG = line(...
    'parent', gca,...
    'color','m',...
    'xdata',[],...
    'ydata',[]);

past_real_pos = zeros(2,0);
past_no_slam_pos = zeros(2,0);
past_our_pos = zeros(2,0);

% II. Temporal loop
for t = 1:max_loop

    % 0. Get data
    % y -> map of measurements of landmarks 
    % u -> control
    [y,u] = data(data_from_file,t);

    % 1. Simulator
    R = move(R, u);
    % noise added to the control for movement 
    n = q.*randn(2,1);
    x_no_slam = move(x_no_slam, u,n);

    % 2. Filter
    %   a. Prediction
    %   CAUTION this is sub-optimal in CPU time
    [x(r), R_r, R_n] = move(x(r), u,n);
    P_rr = P(r,r);
    P(r,:) = R_r*P(r,:);
    P(:,r) = P(r,:)';
    P(r,r) = R_r*P_rr*R_r' + R_n*Q*R_n';

    %   b. correction
    %       i. known lmks
    lids = find(l(1,:)); % find(X) returns a vector containing the linear indices of each nonzero element in array X
    for lid = lids
        
        %if not observed skip
        if  isKey(y,lid) == 0
            continue;
        end

        display('known landmark');
        display(lid);

        % expectation
        [e, E_r, E_l] = project(x(r), x(l(:,lid)));
        E_rl = [E_r E_l];
        rl   = [r l(:,lid)'];
        E    = E_rl * P(rl,rl) * E_rl'; 
        % measurement
        yi = y(lid);

        % innovation
        z = yi - e;
        if z(2) > pi
            z(2) = z(2) - 2*pi;
        end
        if z(2) < -pi
            z(2) = z(2) + 2*pi;
        end
        Z = M + E;

        % Kalman gain
        K = P(:, rl) * E_rl' * Z^-1;

        % update
        x = x + K * z;
        P = P - K * Z * K';
    end

    %       ii. init new lmks
    % check lmk availability
    %lid = find(l(1,:)==0 , 1); %find(X,n) returns the first n indices corresponding to the nonzero elements in X.
    % so lid is a first empty landmark(not observed yet)

    % for each observations add if its not already in the map.
    for el = keys(y)
        lid = el{1}; 

        % skip if we already know this landmark.
        if l(1,lid)!=0
            continue;
        end
        display('new landmark');
        display(lid);

        s = find(mapspace, LM_SIZE);
        if ~isempty(s)
            mapspace(s) = 0;
            l(:,lid) = s'; % ' is the transpose operator'

            % measurement
            yi = y(lid);

            [x(l(:,lid)), L_r, L_y] = backProject(x(r), yi); % 
            P(s,:) = L_r * P(r,:);
            P(:,s) = P(s,:)';
            P(s,s) = L_r * P(r,r) * L_r' + L_y * M * L_y';
        end
    end

    % 3. Graphics

    for i = 1:(t-1)
        set(prG(i), 'xdata', past_real_pos(1,i), 'ydata', past_real_pos(2,i));
        set(pnG(i), 'xdata', past_no_slam_pos(1,i), 'ydata', past_no_slam_pos(2,i));
        set(poG(i), 'xdata', past_our_pos(1,i), 'ydata', past_our_pos(2,i));
    end
    set(RG, 'xdata', R(1), 'ydata', R(2));
    set(rG, 'xdata', x(r(1)), 'ydata', x(r(2)));
    past_real_pos = [past_real_pos R(1:2)];
    past_our_pos = [past_our_pos x(r(1:2))];
    past_no_slam_pos = [past_no_slam_pos x_no_slam(1:2)];

    lids = find(l(1,:));
    lx = x(l(1,lids));
    ly = x(l(2,lids));
    set(lG, 'xdata', lx, 'ydata', ly);
    for lid = lids
        le = x(l(:,lid))
        LE = P(l(:,lid),l(:,lid));
        [X,Y] = cov2elli(le,LE,3,16);
        set(eG(lid),'xdata',X,'ydata',Y);
    end
    if t > 1
        re = x(r(1:2));
        RE = P(r(1:2),r(1:2));
        [X,Y] = cov2elli(re,RE,3,16);
        set(reG,'xdata',X,'ydata',Y);
    end
    drawnow;
    pause(2);
end









