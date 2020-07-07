T1 = readtable('input.csv');
T2 = readtable('snr.csv');

figure;
hold on;
CMap = parula(4);

K = -20 * log10((4 * pi) / (3 * 10 ^ 8)) - 20 * log10(5250 * 10 ^ 6) + 85;
PT = 0;

for i = 1:height(T)
    % Make unit sphere
    [x,y,z] = sphere;
    
    traffic = T1{i, 5};
    
    SNR = 0;

    for j = 1:height(T2)
        if T2{j, 1} <= traffic
            SNR = T2{j, 2};
        end
    end

    % Scale to desire radius.
    radius = 10 ^ ((K + PT - SNR) / 20);
    x = x * radius;
    y = y * radius;
    z = z * radius;

    surface(x + T{i, 2}, y + T{i, 3}, z + T{i, 4}, 'FaceAlpha', 0.5, 'FaceColor', CMap(i, :), ...
          'EdgeColor', [0.4, 0.4, 0.4]);
end

% Label axes.
xlabel('X', 'FontSize', 20);
ylabel('Y', 'FontSize', 20);
zlabel('Z', 'FontSize', 20);

axis equal;
view(3);
