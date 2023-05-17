function [landmarks, u, NUMBER_OF_LANDMARKS] = data(dataObs, i=0)
% DATA Returns a map of observed landmarks for the i-th image,
% the number of all landmarks and the control vector u.
% the map is a containers.Map object, where the key is the landmark id 
% and value is the landmark coordinates[dx, alpha, dz] from robots perspective.
% ids in the map are in the range [1, NUMBER_OF_LANDMARKS].

% for i=0 returns empty landmarks map 


% dataObs is a matrix of size 2+NUMBER_OF_LANDMARKS x NUMBER_OF_IMAGES that is read from the file.
dataObs=dataObs';

u = (dataObs(1:2, 1));
NUMBER_OF_LANDMARKS = dataObs(1, 2);
landmarks = containers.Map('KeyType','int32','ValueType','any');

% so we start from 1 so zero is just to ask for max number of landmarks.
if i == 0
    return;
end

first_index = 3;
size_of_one_image_data = 4; %(indexes + 3 coordinates for each landmark)

% number of first line of data for i-th image
begining = first_index + (i-1)*size_of_one_image_data;
indexes = dataObs(:, begining);

% find first zero in indexes cause this marks the end of actual data.
last = find(indexes(:) == 0 , 1);
if  numel(last)==0
    last = numel(indexes) + 1;
end

indexes = indexes(1:last-1);
observed_coordinates = dataObs(1:last-1, begining+1:begining+3);

for j = 1:numel(indexes)
    landmark = observed_coordinates(j,:);
    landmarks(j) = landmark';
end


end 