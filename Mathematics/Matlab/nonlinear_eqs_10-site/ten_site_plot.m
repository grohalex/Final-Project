function ten_site_plot(sim1, sim2)
a = 0.1; %to print the pars
b =0.9; %adjust
x = fsolve(@ten_site,rand(1,19));   %to solve the equations given by ftion ten_site

xs = x(1:10);           %lattice 1 average occupancies
ys = [0 x(11:end)];     %lattice 2 average occupancies

%absolute errors
err1 = abs(xs-sim1);
err2 = abs(ys-sim2);
%rel.errors
rel1 = err1./sim1;disp(rel1);
rel2 = err2./sim2;disp(rel2);
%plotting:
fig = figure;
subplot(2,1,1)

yyaxis right
bar(rel1, 0.3,'FaceColor', 'None', 'EdgeColor','r', 'LineWidth',0.5);
ylabel("relative error")
ylim([0,0.52])


yyaxis left
plot(xs, "-o",'LineWidth',1.5, 'Color', 'magenta');
hold on
plot(sim1,"-o")
%ylim([0.65,1])

legend("M-F Approx. prediction","simulation values", "relative error",'Position', [0.7 0.64 0.1 0.04])
title(strcat("Mathematical model vs. Simulation, Lattice 1, a=",num2str(a),",b=",num2str(b)))
xlabel("site")
ylabel("average occupancy")

subplot(2,1,2)
yyaxis right
bar(rel2, 0.3,'FaceColor', 'None', 'EdgeColor','r', 'LineWidth',0.5);
ylabel("relative error")
ylim([0,0.52])

yyaxis left
plot(ys, "-o", 'LineWidth',1.5, 'Color', 'magenta')
hold on
plot(sim2,"-o")
%bar(rel2, 0.4,'LineWidth',1.5)
title(strcat("Mathematical model vs. Simulation, Lattice 2, a=",num2str(a),",b=",num2str(b)))
xlabel("site")
ylabel("average occupancy")
legend("M-F Approx. prediction","simulation values","relative error", 'Position', [0.7 0.17 0.1 0.04])


set(fig,'position',[10,10,580,460])

%ylim([0,0.01]
end


