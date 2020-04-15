load('test_unclassified_bin_principal_component2.mat');
pc=coordinates';
d13=pc(:,1:650);
d16=pc(:,651:1600);
d23=pc(:,1601:2250);
d26=pc(:,2251:3200);

figure('position',[200 150 858 635]);
%%
plot3(d13(1,:),d13(2,:),d13(3,:),'r.-','Linewidth',1);
hold on
plot3(d16(1,:),d16(2,:),d16(3,:),'+-','Color',[0.8500 0.3250 0.0980],'Linewidth',1,'MarkerSize',3);
hold on
plot3(d23(1,:),d23(2,:),d23(3,:),'b*-','Linewidth',1,'MarkerSize',3);
hold on
plot3(d26(1,:),d26(2,:),d26(3,:),'o-','Color',[0 0.4470 0.7410],'Linewidth',1,'MarkerSize',3);
hold on
grid on

plot3(d13(1,1:250),d13(2,1:250),d13(3,1:250),'o','MarkerSize',4,'MarkerEdgeColor',[0.4660 0.6740 0.1880],'MarkerFaceColor',[0.4660 0.6740 0.1880]);
hold on
plot3(d16(1,1:250),d16(2,1:250),d16(3,1:250),'o','MarkerSize',4,'MarkerEdgeColor',[0.4660 0.6740 0.1880],'MarkerFaceColor',[0.4660 0.6740 0.1880]);
hold on
plot3(d23(1,1:250),d23(2,1:250),d23(3,1:250),'o','MarkerSize',4,'MarkerEdgeColor',[0.4660 0.6740 0.1880],'MarkerFaceColor',[0.4660 0.6740 0.1880]);
hold on
plot3(d26(1,1:250),d26(2,1:250),d26(3,1:250),'o','MarkerSize',4,'MarkerEdgeColor',[0.4660 0.6740 0.1880],'MarkerFaceColor',[0.4660 0.6740 0.1880]);
hold on

plot3(pc(1,[250,900,1850,2500]),pc(2,[250,900,1850,2500]),pc(3,[250,900,1850,2500]),'yo','MarkerSize',5,'MarkerFaceColor','y')
hold on
plot3(pc(1,[650 1600 2250 3200]),pc(2,[650 1600 2250 3200]),pc(3,[650 1600 2250 3200]),'o','MarkerSize',5,'MarkerEdgeColor',[0.3010 0.7450 0.9330],'MarkerFaceColor',[0.3010 0.7450 0.9330])
hold on

plot3(pc(1,[350,1000,1950,2600]),pc(2,[350,1000,1950,2600]),pc(3,[350,1000,1950,2600]),'ko','MarkerSize',4,'MarkerFaceColor','k')
hold on
plot3(pc(1,[650,2250]),pc(2,[650,2250]),pc(3,[650,2250]),'ko','MarkerSize',3,'MarkerFaceColor','k')
hold on
plot3(pc(1,[1300,2900]),pc(2,[1300,2900]),pc(3,[1300,2900]),'ko','MarkerSize',5,'MarkerFaceColor','k')
hold on
% annotation('arrow',[0.4 0.5],[0.4 0.4]);
% annotation('arrow',[0.4 0.4],[0.4 0.5]);
% annotation('arrow',[0.17 0.19],[0.52 0.57]);
% annotation('arrow',[0.18 0.24],[0.51 0.58]);
quiver3(11,19,-16,22,9,-4,'k','filled','LineWidth',1,'MaxHeadSize',0.5);
quiver3(11,8,-14,23,10,-3,'k','filled','LineWidth',1,'MaxHeadSize',0.5);
text(85,-33,15,'\fontsize{15}1s');
quiver3(72,-33,16,-11,-5,7,'k','filled','LineWidth',1,'MaxHeadSize',0.8);
quiver3(65,-11,16,-12,-4,6,'k','filled','LineWidth',1,'MaxHeadSize',0.8);
% annotation('arrow',[0.48 0.45],[0.71 0.6]);
% annotation('arrow',[0.49 0.49],[0.71 0.65]);
quiver3(-16,-10,-3,-2,21,3,'k','filled','LineWidth',1,'MaxHeadSize',0.6);
quiver3(-12,0,16,-4,20,2,'k','filled','LineWidth',1,'MaxHeadSize',0.6);
text(-12,20,10,'\fontsize{15}4s');
text(10,60,10,'\fontsize{15}4s');
%%
h=zeros(7,0);
h(1)=plot3(NaN,NaN,NaN,'r.-','Linewidth',1);
h(2)=plot3(NaN,NaN,NaN,'+-','Color',[0.8500 0.3250 0.0980],'Linewidth',1,'MarkerSize',3);
h(3)=plot3(NaN,NaN,NaN,'b*-','Linewidth',1,'MarkerSize',3);
h(4)=plot3(NaN,NaN,NaN,'o-','Color',[0 0.4470 0.7410],'Linewidth',1,'MarkerSize',3);
h(5)=plot3(NaN,NaN,NaN,'yo','MarkerSize',5,'MarkerFaceColor','y');
h(6)=plot3(NaN,NaN,NaN,'o','MarkerSize',5,'MarkerEdgeColor',[0.3010 0.7450 0.9330],'MarkerFaceColor',[0.3010 0.7450 0.9330]);
h(7)=plot3(NaN,NaN,NaN,'o','MarkerSize',4,'MarkerEdgeColor',[0.4660 0.6740 0.1880],'MarkerFaceColor',[0.4660 0.6740 0.1880]);
legend(h,'sample1,delay3s','sample1,delay6s','sample2,delay3s','sample2,delay6s','sample onset','test onset','baseline');
view(120,18);
xlabel('\fontsize{15}PC1'),ylabel('\fontsize{15}PC2'),zlabel('\fontsize{15}PC3');