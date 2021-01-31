function  xs = recursion(x_start, C, steps);
xs = zeros(0,steps);
xs(1) = x_start;
for i = 2:steps
    xs(i) = x_next(xs(i-1),C);
end
figure;
plot(xs, "o-")
tit = strcat("Recursion, SEED: ", num2str(x_start), " with C=", num2str(C));
title(tit)
xlabel("step")
ylabel("x+1")
end

