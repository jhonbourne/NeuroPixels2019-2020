conf=0.95;
perm_times=100000;
load('test_unclassified_bin_principal_component.mat');
pc=cell(1,4);
pc{1}=coordinates(1:650,:);
pc{2}=coordinates(651:1600,:);
pc{3}=coordinates(1601:2250,:);
pc{4}=coordinates(2251:3200,:);

load('bootstrap_principal_component.mat');
bs=cell(1,4);
bs{1}=samples_of_pc(:,1:650,:);
bs{2}=samples_of_pc(:,651:1600,:);
bs{3}=samples_of_pc(:,1601:2250,:);
bs{4}=samples_of_pc(:,2251:3200,:);

alpha=1-conf;
bs_dim=size(samples_of_pc);
bs_num=bs_dim(1);
min_sp=round(bs_num*alpha/2);
if min_sp==0
    min_sp=1;
end
max_sp=round(bs_num*(1-alpha/2));

samples=cell(1,2);
samples{1}=cell(1,length(pc{1}));
samples{2}=cell(1,length(pc{2}));

dists=cell(1,2);
CIs=cell(1,2);
for t=1:2
    dist=[];
    CI=[];
    for i=1:length(pc{t})
        D=[];
        for j=1:bs_num
            co1=reshape(bs{t}(j,i,:),1,[]);
            co2=reshape(bs{t+2}(j,i,:),1,[]);
            d=pdist2(co1,co2);
            D=[D d];
        end
        D=sort(D);
        CI=[CI;[D(min_sp),D(max_sp)]];
        tr_d=pdist2(pc{t}(i,:),pc{t+2}(i,:));
        dist=[dist tr_d];
        samples{t}{i}=[tr_d D];
    end
    dists{t}=dist;
    CIs{t}=CI;
end
%%
load('shuffles_principal_component.mat');
sf=cell(1,4);
sf{1}=shuffles_of_pc(:,1:650,:);
sf{2}=shuffles_of_pc(:,651:1600,:);
sf{3}=shuffles_of_pc(:,1601:2250,:);
sf{4}=shuffles_of_pc(:,2251:3200,:);
bs_dim=size(shuffles_of_pc);
bs_num=bs_dim(1);
min_sp=round(bs_num*alpha/2);
if min_sp==0
    min_sp=1;
end
max_sp=round(bs_num*(1-alpha/2));
shuffles=cell(1,2);
for t=1:2
    shuffle=[];
    for i=1:length(sf{t})
        D=[];
        for j=1:bs_num
            co1=reshape(sf{t}(j,i,:),1,[]);
            co2=reshape(sf{t+2}(j,i,:),1,[]);
            d=pdist2(co1,co2);
            D=[D d];
        end
        D=sort(D);
        shuffle=[shuffle;[mean(D),D(min_sp),D(max_sp)]];
        samples{t}{i}=[samples{t}{i} D];
    end
    shuffles{t}=shuffle;
end
%%
p_value=cell(1,2);
p_value{1}=zeros(1,length(pc{1}));
p_value{2}=zeros(1,length(pc{2}));
for t=1:2
    for i=1:length(samples{t})
        observe_diff=mean(samples{t}{i}(1:bs_num+1))-mean(samples{t}{i}(bs_num+2:end));
        rand_diff=zeros(1,perm_times);
        for n=1:perm_times
            perm_indices=randperm(length(samples{t}{i}));
            rand_diff(n)=mean(samples{t}{i}(perm_indices(1:bs_num+1)))-mean(samples{t}{i}(perm_indices(bs_num+1:end)));
        end
        p=(length(find(abs(rand_diff) > abs(observe_diff)))+1) / (perm_times+1);
        p_value{t}(i)=p;
    end
end
%%
Color=['m','k'];
for t=1:2
    x=(-250:size(shuffles{t},1)-250-1)*0.01;
    y_dist=shuffles{t}(:,1);
    x_fill=[x,fliplr(x)];
    y_fill=[shuffles{t}(:,2); flipud(shuffles{t}(:,3))];
    plot(x,y_dist,Color(t),'LineWidth',2);
    hold on
    fill(x_fill,y_fill,Color(t),'FaceAlpha',0.3,'EdgeAlpha',0);
end
     
color=['r','b'];
for t=1:2
    x=(-250:length(dists{t})-250-1)*0.01;
    y_dist=dists{t};
    x_fill=[x,fliplr(x)];
    y_fill=[CIs{t}(:,1); flipud(CIs{t}(:,2))];
    plot(x,y_dist,color(t),'LineWidth',2);
    hold on
    fill(x_fill,y_fill,color(t),'FaceAlpha',0.3,'EdgeAlpha',0);
    hold on 
    
end
Axis=axis;
height=Axis(4);

axis([-2.5,7.5,0,height]);   
plot([0,0],[0,height],'k--');
plot([4,4],[0,height],'k--');
plot([7,7],[0,height],'k--');
text(-0.6,8,'\fontsize{15}Sample Onset');
text(3.6,8,'\fontsize{15}Test Onset \newline (3s Delay)');
text(6.6,8,'\fontsize{15}Test Onset \newline (6s Delay)');
for t=1:2
    x=(-250:length(p_value{t})-250-1)*0.01;
    plot(x,height/80*t*ones(1,length(x)),'k-','LineWidth',2);
    idx=find(p_value{t}> (0.05/length(p_value{t})) );
    slice=[0 find(diff(idx)~=1) length(idx)];
    for i=1:length(slice)-1
        plot(x(idx( slice(i)+1 : slice(i+1) )), height/80*t*ones(1,length(slice(i)+1 : slice(i+1))),'w-','LineWidth',2);
    end
end


h=zeros(1,4);
h(1)=plot(NaN,NaN,color(1),'LineWidth',2);
h(2)=plot(NaN,NaN,color(2),'LineWidth',2);
h(3)=plot(NaN,NaN,Color(1),'LineWidth',2);
h(4)=plot(NaN,NaN,Color(2),'LineWidth',2);
legend(h,'Euclid distance between trajectory of 3s delay','Euclid distance between trajectory of 6s delay','Euclid distance between shuffled trajectory of 3s delay','Euclid distance between shuffled trajectory of 6s delay')
xlabel('\fontsize{15}Time from sample onset(s)'),ylabel('\fontsize{15}Distance in principal component space(first 20 PCs)');
% title('\fontsize{15}3s Delay Trainsent Selective Cells');    

