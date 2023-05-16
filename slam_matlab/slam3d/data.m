function [landmarks, u, NUMBER_OF_LANDMARKS] = data(i=0)
%DATA Returns a map of observed landmarks for the i-th image,
%the number of all landmarks and the control vector u.
% the map is a containers.Map object, where the key is the landmark id 
% and value is the landmark coordinates[dx, alpha, dz] from robots perspective.
% ids in the map are in the range [1, NUMBER_OF_LANDMARKS].

%example data 

%movement, can be different for each image. 
u = [1;0];

NUMBER_OF_LANDMARKS = 2;
landmarks = containers.Map('KeyType','int32','ValueType','any');


if nargout > 2
    return;
end

observed_coordinates =[[3 0 0];[4 0 0]];
observed_coordinates(:,:,2) = [[2 0 0];[3 0 0]];
observed_coordinates(:,:,3) = [[1  0  0];[2  0 0]];
observed_coordinates(:,:,4) = [[0  0  0];[1  0 0]];

for j = 1:NUMBER_OF_LANDMARKS
    if i == 2 && j == 2
        continue; 
    end
    landmark = observed_coordinates(j,:,i);
    landmarks(j) = landmark';
end

end 