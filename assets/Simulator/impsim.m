function yy=impsim(fs,nx,fmod,amp_imp,f_center,bandwidth,shift)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
fnx = @(x,fn,dn) sin(2*pi*fn*x).*exp(-dn*x);
tp = 0:1/fs:0.05;
% pp = fnx(tp,30);
pnx=numel(tp);

t=(1:nx)/fs;
dt=t(3)-t(2);
yy=zeros(nx,1);
for j=1:numel(fmod) % ka¿de uszkodzenie
    bpFilt = designfilt('bandpassfir','FilterOrder',80, ...
         'CutoffFrequency1',f_center(j)-bandwidth(j),...
         'CutoffFrequency2',f_center(j)+bandwidth(j), ...
         'SampleRate',fs);
    syg_c=zeros(nx,1);
    fault_samples=round(fs/fmod(j));
%     if cyclic(j)
        gdzie=1:fault_samples:(ceil(nx/fault_samples))*fault_samples;
%     else
%         gdzie=floor(pnx+rand(10,1)*(length(t)-pnx));
%     end
    gdzie(gdzie+pnx+1>length(t))=[];
%     gdzie=gdzie+shift(j);
    
    for i=1:length(gdzie) % ka¿dy impuls 
        y = amp_imp(j)*fnx(tp,f_center(j),3000);%800
        syg_c(gdzie(i):gdzie(i)+pnx-1)=syg_c(gdzie(i):gdzie(i)+pnx-1)+y';    
    end
%     kurtosis(circshift(filter(bpFilt,syg_c),shift(j)))
    yy=yy+circshift(filter(bpFilt,syg_c),shift(j));
end
% figure;plot(yy);grid on;
end

