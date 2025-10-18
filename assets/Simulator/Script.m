B = 40; % amplituda impulsów
fs=25000; % częstotliwość próbkowania
t = -0.1:0.0001:0.01;
varsize = fs; % sygnał 1s
fmod=30; % fault_freq
f_center=5000; % środek pasma informacyjnego
bandwidth=1500; % zakres pasma informacyjnego (f_center +- bandwidth)
shift=0; % przesunięcie impulsow
y = B*impsim(fs,varsize,fmod,1,f_center,bandwidth,shift);
sigma = 3; % sigma szumu
noise = normrnd(0,sigma,1,varsize); % szum Gauss
signal = noise + y';
figure;plot(signal)