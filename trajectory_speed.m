load('test_unclassified_bin_principal_component.mat');
pc=cell(1,4);
pc{1}=coordinates(1:650,:);
pc{2}=coordinates(651:1600,:);
pc{3}=coordinates(1601:2250,:);
pc{4}=coordinates(2251:3200,:);

dists=cell(1,4);
for t=1:4
    dist=[];
    for i=1:(length(pc{t})-1)
        D=pdist2(pc{t}(i,:),pc{t}(i+1,:));
        dist=[dist D];
    end
    dists{t}=dist;
end

for k=1:4
    x=(-250:length(dists{k})-250-1)*0.01;
    y=dists{k}/0.01;
    plot(x,y);
    hold on
end
legend('sample1,delay3s','sample1,delay6s','sample2,delay3s','sample2,delay6s');
xlabel('\fontsize{15Ttime from sample onset(s)'),ylabel('\fontsize{15}Speed in principal components space')


        
        
