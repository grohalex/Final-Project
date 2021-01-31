function thirty_site_plot(sim1, sim2)
a = 0.4; %to print the pars
b = 1; %adjust
x = fsolve(@thirty_site,rand(1,59));   %to solve the equations given by ftion ten_site

xs = x(1:30);           %lattice 1 average occupancies
ys = [0 x(31:end)];     %lattice 2 average occupancies

%plotting:
subplot(2,1,1)
plot(xs, "-o")
hold on
plot(sim1,"-o")
legend("M-F Approx. prediction","simulation values")
title(strcat("Mathematical model vs. Simulation, Lattice 1, a=",num2str(a),",b=",num2str(b)))
xlabel("site")
ylabel("average occupancy")
%ylim([0,0.1])
subplot(2,1,2)
plot(ys, "-o")
hold on
plot(sim2,"-o")
title(strcat("Mathematical model vs. Simulation, Lattice 2, a=",num2str(a),"b=",num2str(b)))
xlabel("site")
ylabel("average occupancy")
legend("M-F Approx. prediction","simulation values")
%ylim([0,0.01])
end

