close;clc;clear;
%% Grids Initialization
figure(1);
xlim([0 14]);
ylim([0 14]);
hold on;
axis off;
line([0 0],[0 14]);
line([2 2],[0 14]);
line([4 4],[0 14]);
line([6 6],[0 14]);
line([8 8],[0 14]);
line([10 10],[0 14]);
line([12 12],[0 14]);
line([14 14],[0 14]);
line([0 14],[0 0]);
line([0 14],[2 2]);
line([0 14],[4 4]);
line([0 14],[6 6]);
line([0 14],[8 8]);
line([0 14],[10 10]);
line([0 14],[12 12]);
line([0 14],[14 14]);

%% Washer Location
% washer = [randi([1 13]),randi([1 13]);
%           randi([1 13]),randi([1 13]);
%           randi([1 13]),randi([1 13]);
%           randi([1 13]),randi([1 13]);];

washer = [ 1,9;
           13,13;
           7,4;
           9,7; ];
s = size(washer);
%% Path
default_path = [ 1,1;
                 1,3;
                 3,3;
                 3,11;
                 11,11;
                 11,3;
                 3,3;
                 3,7;
                 10.5,7; ];
plot(default_path(:,1), default_path(:, 2), 'k--d');

%% Find Washers and Update Path
default_path = [ 1,1;
                 1,3;
                 3,3;
                 
                 % 1st
                 3,9;
                 1,9;
                 3,9;
                 % 1st
                 
                 3,11;
                 11,11;
                 
                 % 2nd
                 13,11;
                 13,13;
                 13,11;
                 11,11;
                 % 2nd
                 
                 11,3;
                 
                 % 3rd
                 7,3;
                 7,4;
                 7,3;
                 % 3rd
                 
                 3,3;
                 3,7;
                 
                 % 4th
                 9,7;
                 % 4th
                 
                 10.5,7; ];

%% Robot 
robot = differentialDriveKinematics("TrackWidth", 1,...
    "VehicleInputs", "VehicleSpeedHeadingRate");

robotInitialLocation = default_path(1,:);
robotGoal = default_path(end,:);

initialOrientation = 90;
robotCurrentPose = [robotInitialLocation, initialOrientation]';

%% Controller
controller = controllerPurePursuit;
controller.Waypoints = default_path;
controller.DesiredLinearVelocity = 0.8;
controller.MaxAngularVelocity = 2;
controller.LookaheadDistance = 0.5;

%% Run
goalRadius = 0.1;
distanceToGoal = norm(robotInitialLocation - robotGoal);

sampleTime = 0.1;
vizRate = rateControl(1/sampleTime);

frameSize = robot.TrackWidth/0.8;

figure(2);
pause(4);
num = 0;

while(distanceToGoal > goalRadius)
    [v, omega] = controller(robotCurrentPose);
    vel = derivative(robot, robotCurrentPose, [v, omega]);
    robotCurrentPose = robotCurrentPose+vel*sampleTime;
    distanceToGoal = norm(robotCurrentPose(1:2)-robotGoal(:));
    hold off;
    plot(default_path(:,1), default_path(:,2), "k--.")
    hold on;
    plot(washer(:,1),washer(:,2),'ro');
    
    line([0 0],[0 14]);
    line([2 2],[0 14]);
    line([4 4],[0 14]);
    line([6 6],[0 14]);
    line([8 8],[0 14]);
    line([10 10],[0 14]);
    line([12 12],[0 14]);
    line([14 14],[0 14]);
    line([0 14],[0 0]);
    line([0 14],[2 2]);
    line([0 14],[4 4]);
    line([0 14],[6 6]);
    line([0 14],[8 8]);
    line([0 14],[10 10]);
    line([0 14],[12 12]);
    line([0 14],[14 14]);
    
    hold all;
    
    plotTrVec = [robotCurrentPose(1:2);0];
    plotRot = axang2quat([0, 0, 1, robotCurrentPose(3)]);
    plotTransforms(plotTrVec', plotRot, "MeshFilePath","groundvehicle.stl",...
        "Parent",gca, "View","2D", "FrameSize", frameSize);
    light;
    xlim([0 14]);
    ylim([0 14]);
    axis off;
    
    if(~isempty(washer))
        for idx = 1:s(1)
            if(sqrt((robotCurrentPose(1)-washer(idx,1))^2+...
                    (robotCurrentPose(2)-washer(idx,2))^2) <= 0.2)
                txt = "Washer Patched";
                num = num+1;
                text(1,13,txt);
                pause(1);
                washer = washer(washer ~= washer(idx,:));
                washer = reshape(washer,length(washer)/2,2);
                s = size(washer);
                if(~isempty(washer))
                    robotCurrentPose(3) = 180+robotCurrentPose(3);
                end
                break;
            else
                txt = "Default Path";
                text(1,13,txt);
            end
        end
    end
    text(1,12,"# of Washer: "+string(num));
    
    waitfor(vizRate);
end
