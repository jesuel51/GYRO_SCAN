# this script is used to plot the file out.gyro.moment_zero, which is is flux-surface averaged n = 0 component of density and energy moments
# the format of the file is 
# n_x, n_kinetic, n_moment=2, n_time
# it's highly recommended that the scripts should be named after the gyro ouput file name
# before reading such a file, we should run one script which offer the dimentional parameter
root['PLOTS']['GYROalone']['getdim.py'].run()
dim=root['SETTINGS']['DEPENDENCIES']['dim']
n_kinetic = dim['n_kinetic']
#n_theta_plot = dim['n_theta_plot']
n_x       = dim['n_x']
#n_field      = dim['n_field']
#n_n          = dim['n_n']
n_time    = dim['n_time']
time_max  = dim['time_max']
# read the data
f_moment_zero=open(root['OUTPUTS']['out.gyro.moment_zero'].filename,'Ur')
data_moment_zero = f_moment_zero.readlines()
data_moment_zero =array([float(item) for item in data_moment_zero])
# transfrom into array
#data_gbflux_array=data_gbflux.reshape((n_kinetic,n_field,4,n_time))
data_moment_zero_array=data_moment_zero.reshape((n_time,2,n_kinetic,n_x))
# let's plot, note here we only plot the main parts, the others can be plotted similarly if needed
#time_max=root['INPUTS']['input.gyro']['TIME_MAX']
t=linspace(0,time_max,n_time)
#figure(figsize=[12,8],figname='ZF componment evoluation')
figure(figsize=[12,8])
lw=2
fs1=24
fs2=20
# time traces of the density fluctuation 
delta_n_i=[sqrt(mean([data_moment_zero_array[n_time_k][0][0][n_x_k]**2 for n_x_k in arange(n_x)])) for n_time_k in arange(n_time)]
delta_n_e=[sqrt(mean([data_moment_zero_array[n_time_k][0][-1][n_x_k]**2 for n_x_k in arange(n_x)])) for n_time_k in arange(n_time)]
delta_E_i=[sqrt(mean([data_moment_zero_array[n_time_k][1][0][n_x_k]**2 for n_x_k in arange(n_x)])) for n_time_k in arange(n_time)]
delta_E_e=[sqrt(mean([data_moment_zero_array[n_time_k][1][-1][n_x_k]**2 for n_x_k in arange(n_x)])) for n_time_k in arange(n_time)]

subplot(1,2,1)
plot(t,delta_n_i,'-b',linewidth=lw,label='Ion')
plot(t,delta_n_e,'-r',linewidth=lw,label='Electron')
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
xlabel('$t(a/c_s)$',fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
legend(loc=0,fontsize=fs2).draggable(True)
title('$\delta n$',fontsize=fs1,family='serif')

subplot(1,2,2)
plot(t,delta_E_i,'-b',linewidth=lw)
plot(t,delta_E_e,'-r',linewidth=lw)
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
xlabel('$t(a/c_s)$',fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('$\delta E$',fontsize=fs1,family='serif')
