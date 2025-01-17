function fifty_site_plot(sim1, sim2)
a = 0.21; %to print the pars
b = 0.21; %adjust

    % alternative methods
% options = optimoptions('fsolve'); 
% options.MaxIterations = 100000;
% options.MaxFunctionEvaluations = 500000000000000000000000000;
% x = fsolve(@fifty_site,rand(1,99), options);   %to solve the equations given by ftion fifty_site
%x = fsolve(@fifty_site,ones(1,99));   %to solve the equations given by ftion fifty_site

x = fsolve(@fifty_site,rand(1,99));   %to solve the equations given by ftion fifty_site
xs = x(1:50);           %lattice 1 average occupancies
ys = [0 x(51:end)];     %lattice 2 average occupancies

%plotting:
subplot(2,1,1)
plot(xs, "-o")
hold on
plot(sim1,"-o")
legend("M-F Approx. prediction","simulation values")
title(strcat("Mathematical model vs. Simulation, Lattice 1, a=",num2str(a),",b=",num2str(b)))
xlabel("site")
ylabel("average occupancy")
%ylim([0.006,0.014])
subplot(2,1,2)
plot(ys, "-o")
hold on
plot(sim2,"-o")
title(strcat("Mathematical model vs. Simulation, Lattice 2, a=",num2str(a),",b=",num2str(b)))
xlabel("site")
ylabel("average occupancy")
legend("M-F Approx. prediction","simulation values")
%ylim([0,0.001])
end

