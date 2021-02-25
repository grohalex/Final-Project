%plotting the relation between rho and gamma for the PERIODIC BOUNDARY
%CONDITIONS
%% plot one
xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case



plot(xs,ys, "-", "LineWidth", 3.0)
%hold on
%plot(sim1,"-")
l = legend("Relation γ(ρ) = ρ^2/(ρ^2-ρ+1) ", "Location",'northwest');
%title(strcat("",num2str(a),",b=",num2str(b)))
t = title({"The relation between lattice 1 and lattice 2 avg. occupancies", "(with periodic boundary conditions)"});
lx = xlabel("ρ, lattice 1 occupancy ");
ly = ylabel("γ, lattice 2 occupancy ");
l.FontSize = 15; 
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;

%% plot two

xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case

xs_ident = [0:0.1:1];
ys_ident = [0:0.1:1];

plot(xs_ident,ys_ident, "-.", "LineWidth", 2.0)
hold on
plot(xs,ys, "-", "LineWidth", 3.0)
%hold on
%plot(sim1,"-")

%title(strcat("",num2str(a),",b=",num2str(b)))
l = legend("y = x", "Relation γ(ρ) = ρ^2/(ρ^2-ρ+1) ", "Location",'northwest');
t = title({"The relation between lattice 1 and lattice 2 avg. occupancies", "(with periodic boundary conditions)"});
lx = xlabel("ρ, lattice 1 occupancy ");
ly = ylabel("γ, lattice 2 occupancy ");
l.FontSize = 15; 
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;

%% plot two

xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case

% to show the trends
xs_long = [-5:0.001:5];
ys_long = xs_long.*xs_long./(xs_long.*xs_long-xs_long+1);

shade = fill([0,1, 1, 0 ], [0,0, 2, 2], [0.95 0.95 0.95], 'LineStyle','none');
hold on


plot(xs_long,ys_long,"blue", "LineWidth", 3.0)
plot(xs,ys,"red", "LineWidth", 3.0)



ylim([0 1.6])
l = legend("","Relation γ(ρ) = ρ^2/(ρ^2-ρ+1) ");
t = title({"The relation between lattice 1 and lattice 2 avg. occupancies", "(with periodic boundary conditions)"});
lx = xlabel("ρ, lattice 1 occupancy ");
ly = ylabel("γ, lattice 2 occupancy ");
l.FontSize = 15; 
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;
annots = get(shade,'Annotation');
set(get(annots(1),'LegendInformation'),'IconDisplayStyle','off')

%% Plot four - second derivative

xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case

xs_ident = [0:0.1:1];
ys_ident = [0:0.1:1];

ys_diff = diff(ys)./diff(xs);
xs_diff = (xs(2:end)+xs(1:(end-1)))/2;

plot(xs_ident,ys_ident, "-.", "LineWidth", 2.0)
hold on
plot(xs,ys, "-", "LineWidth", 3.0)
plot(xs_diff,ys_diff, ":", "LineWidth", 2.0)
%hold on
%plot(sim1,"-")

%title(strcat("",num2str(a),",b=",num2str(b)))
l = legend("y = x", "Relation γ(ρ) = ρ^2/(ρ^2-ρ+1) ", "γ'(ρ)" , "Location",'northwest');
t = title({"The relation between lattice 1 and lattice 2 avg. occupancies", "(with periodic boundary conditions)"});
lx = xlabel("ρ, lattice 1 occupancy ");
ly = ylabel("γ, lattice 2 occupancy ");
l.FontSize = 15; 
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;

%% plot five - total particles in the system

xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case

sum = xs + ys;  %sum of rhos and gammas: total part. in the system

hold on
plot(xs,ys, "-", "LineWidth", 3.0)
plot(xs,sum, ":", "LineWidth", 3.0)

%title(strcat("",num2str(a),",b=",num2str(b)))
l = legend( "Relation γ(ρ) = ρ^2/(ρ^2-ρ+1) ","Total particles in the system, γ+ρ ", "Location",'northwest');
t = title({"The relation between ρ and γ and total number of particles", "(with periodic boundary conditions system)"});
lx = xlabel("ρ, lattice 1 occupancy ");
ly = ylabel("γ, lattice 2 occupancy ");
l.FontSize = 15; 
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;

%% plot six - triplots for J_tot


xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case
rh_t = xs + ys;
J_tot = xs.*(1-xs).*(1+2.*xs./(xs.*xs-xs+1)+xs.*xs./(xs.*xs-xs+1));

u1 = sin(xs);%%%
%plotting multiple plots
figure;

h(1) = subplot(3,1,1); % upper plot
plot(rh_t, J_tot, 'Color', 'r'); hold on;
[~,imx]=max(J_tot);
[~,imn]=min(J_tot);
plot([rh_t(imx);rh_t(imx)],[0;J_tot(imx)],':')

lx = xlabel('ρ_{tot}');
ly = ylabel('J_{tot}');
t = title('The relationship between ρ_{tot},ρ,γ and J_{tot}');
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;

h(2) = subplot(3,1,2); % middle plot
plot(xs, J_tot, 'Color', 'r'); hold on;
[~,imx]=max(J_tot);
[~,imn]=min(J_tot);
plot([xs(imx);xs(imx)],[0;J_tot(imx)],':')
lx = xlabel('ρ');
ly = ylabel('J_{tot}');
lx.FontSize = 15;
ly.FontSize = 15;



h(3) = subplot(3,1,3); % lower plot
plot(ys, J_tot, 'Color', 'r'); hold on;
[~,imx]=max(J_tot);
[~,imn]=min(J_tot);
plot([ys(imx);ys(imx)],[0;J_tot(imx)],':')
lx = xlabel('γ');
ly = ylabel('J_{tot}');
lx.FontSize = 15;
ly.FontSize = 15;



%% plot seven - triplots for J_11


xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case
rh_t = xs + ys;
J11 = xs.*(1-xs);      %current in lattice 1
J12 = xs.*xs.*(1-ys);  %diagonal current 1->2
J21 = ys.*(1-xs);      %diagonal current 2->1 should be the same as J12!!!
J22 = xs.*ys.*(1-ys);  %current in lattice 2

u1 = sin(xs);%%%
%plotting multiple plots
figure;

h(1) = subplot(3,1,1); % upper plot
plot(rh_t, J22, 'Color', 'r'); hold on;
[~,imx]=max(J22);
[~,imn]=min(J22);
plot([rh_t(imx);rh_t(imx)],[0;J22(imx)],':')

lx = xlabel('ρ_{tot}');
ly = ylabel('J^{22}');
t = title('The relationship between ρ_{tot},ρ,γ and J^{22}');
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;

h(2) = subplot(3,1,2); % middle plot
plot(xs, J22, 'Color', 'r'); hold on;
[~,imx]=max(J22);
[~,imn]=min(J22);
plot([xs(imx);xs(imx)],[0;J22(imx)],':')
lx = xlabel('ρ');
ly = ylabel('J^{22}');
lx.FontSize = 15;
ly.FontSize = 15;



h(3) = subplot(3,1,3); % lower plot
plot(ys, J22, 'Color', 'r'); hold on;
[~,imx]=max(J22);
[~,imn]=min(J22);
plot([ys(imx);ys(imx)],[0;J22(imx)],':')
lx = xlabel('γ');
ly = ylabel('J^{22}');
lx.FontSize = 15;
ly.FontSize = 15;

%% plot 8 - comparision J_tot with simulation

xs = [0:0.001:1]; %rhos, lattice 1 densities
ys = xs.*xs./(xs.*xs-xs+1);%gammas, lattice 2 densities derived for the periodic bound. case
rh_t = xs + ys;
J_tot = xs.*(1-xs).*(1+2.*xs./(xs.*xs-xs+1)+xs.*xs./(xs.*xs-xs+1));

u1 = sin(xs);%%%
%plotting multiple plots
figure;

%h(1) = subplot(3,1,1); % upper plot
plot(rh_t, J_tot, 'Color', 'r'); hold on;
[~,imx]=max(J_tot);
[~,imn]=min(J_tot);
plot([rh_t(imx);rh_t(imx)],[0;J_tot(imx)],':')

steps = linspace(0,2,100);
sim = sim;%simulation values
plot(steps, sim, 'Color', 'b'); hold on;

[~,imx]=max(sim);%max of simulation values
[~,imn]=min(sim);
plot([steps(imx);steps(imx)],[0;sim(imx)],':')

lx = xlabel('ρ_{tot}');
ly = ylabel('J_{tot}');
t = title('The relationship between ρ_{tot} and J_{tot} vs. simulation');
legend('MF prediction','max(MF prediction)','Simulation', 'max(Simulation)')
t.FontSize = 17;
lx.FontSize = 15;
ly.FontSize = 15;










