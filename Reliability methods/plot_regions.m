%% PLOT SAFETY REGIONS
clc
clear all
%real data
filename="Used Datasets/over40_real_test.xlsx";
%real+fake data
%filename="over40_farthest_test.xlsx";

test_data=readtable(filename);

% real data features
f1=test_data.Hip_ACC_Mean;
f2=test_data.Hip_yposture_Mean;

% real+fake data features
%f1=test_data.Ankle_yposture_coefficient_of_variation;
%f2=test_data.averageStepDistance;

labels=cell2mat(test_data.fatiguestate1);

%old and new thresholds for real data case (from python output)
th1_old=4.61;
th1_new=4.61;
th2_old=63.69;
th2_new=64.37;
% old and new thresholds for real+fake data case (from python output)
% th1_old=12.84;
% th2_old=0.65;
% th1_new=14.08;
% th2_new=0.65;

% needed to draw a patch on the safety region
x=[th1_new,max(f1),max(f1),th1_new];
y=[min(f2),min(f2),th2_new,th2_new];

% plots (change axis labels for real+fake data case)
figure
scatter(f1(labels=='0'),f2(labels=='0'),'go','filled');
hold on
scatter(f1(labels=='1'),f2(labels=='1'),'ro','filled');
hold on
xline(th1_new);
hold on
xline(th1_old);
hold on
yline(th2_new);
hold on
yline(th2_old);
patch(x,y,'b','FaceAlpha',0.2);
xlabel("Hip Acceleration Mean",'FontWeight','bold','FontSize',12);
ylabel("Hip y Posture Mean",'FontWeight','bold','FontSize',12);
legend("Not Fatigued","Fatigued",'location','best','FontWeight','bold','FontSize',11);
xlim([min(f1),max(f1)]);
%xticks([sort([th1_new,th1_old])]);
xticks(th1_new);
%xtickangle(45);
yticks([sort([th2_old,th2_new])]);
%yticks(th2_new);