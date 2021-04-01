%% PING
% Laufzeit analyse für Netzwerkanfragen

%% Konfiguration
server = '0.ch.pool.ntp.org';
if ismac
    cmd = ['ping -c 1 ', server];
elseif isunix
    cmd = ['ping -c 1 ', server];
elseif ispc
    cmd = ['ping -n 1 ', server];
end
N = 50;


%% Schleife

figure

initTime = now; 

tmVec = [];
tVec  = [];

for i=1:N
    [tm, tmin, tmax] = doPing(cmd);
    tmVec(end+1) = tm;
    tVec(end+1)  = (now-initTime)*24*3600;
    
    include = tmVec<=quantile(tmVec, .9);
    
    
    subplot(2,1,1)
    title([num2str(i) '/' num2str(N) '(' num2str(round(i/N*100)) '%)'])
    
    errorbar(tVec(end), tm, tm-tmin, tmax-tm, 'ks'); hold on;
    if i>1
        plot(tVec(end-1:end), tmVec(end-1:end),'k--');
    end
    grid on;
    xlabel('time [s]')
    ylabel('t_3 - t_0 [ms]');
    
    subplot(2,1,2)
    plot(tVec(include), tmVec(include)/2, 'ks'); hold on;
    plot(tVec(~include), min(tmVec(~include)/2, quantile(tmVec, .9)/2), 'rx');
    stairs(tVec(include),  cumsum(tmVec(include)/2)./cumsum(ones(size(tmVec(include)))), 'k--')
    plot(tVec([1, end]), mean(tmVec(include)/2)*[1 1], 'k'); hold off;
    legend('Schätzung', 'Schätzungen, ausgelassen', 'Mittelwert (Entwicklung)', 'Mittelwert')
    
    ax = gca;
    ax.YLim(2) = quantile(tmVec, .9)/2;
    ax.YLim(1) = ax.YLim(1)-.5;
    
    
    grid on;
    xlabel('time [s]')
    ylabel('\theta [ms]');
    
    drawnow
    
%     pause(10)
end



%% Anfrage und Statistik
function [tm, tmin, tmax] = doPing(cmd)
    [status, ret] = system(cmd);
    
    if status == 0
        tm = str2double(regexp(ret, 'Mittelwert = ([0-9]+)ms', 'tokens', 'once'));
        tmin = str2double(regexp(ret, 'Maximum = ([0-9]+)ms', 'tokens', 'once'));
        tmax = str2double(regexp(ret, 'Minimum = ([0-9]+)ms', 'tokens', 'once'));
    else
        tm = nan;
        tmin = nan;
        tmax = nan;
    end
    
        

end



