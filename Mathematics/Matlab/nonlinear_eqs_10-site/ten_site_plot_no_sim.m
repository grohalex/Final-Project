function ten_site_plot_no_sim()
a = 0.1; %to print the pars
b = 0.9; %adjust
x = fsolve(@ten_site,rand(1,19));   %to solve the equations given by ftion ten_site

xs = x(1:10);           %lattice 1 average occupancies
ys = [0 x(11:end)];     %lattice 2 average occupancies

%plotting:
subplot(2,1,1)
plot(xs, "-o")
hold on
%plot(sim1,"-o")
%legend("M-F Approx. prediction")
title(strcat("Mean-field approximation, Lattice 1, α=",num2str(a),", β=",num2str(b)))
xlabel("site")
ylabel("average occupancy")
ylim([0.2,0.3])
subplot(2,1,2)
plot(ys, "-o")
hold on
%plot(sim2,"-o")
title(strcat("Mean-field approximation, Lattice 2, α=",num2str(a),", β=",num2str(b)))
xlabel("site")
ylabel("average occupancy")
%legend("M-F Approx. prediction")
ylim([0,0.1])
end
