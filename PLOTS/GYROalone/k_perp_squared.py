# this script is used to plot the file out.gyro.k_perp_squared, which is the flux-surface and radial average of k_perp
# the format of the file is 
# n_n, n_time
# it's highly recommended that the scripts should be named after the gyro ouput file name
# before reading such a file, we should run one script which offer the dimentional parameter
root['PLOTS']['GYROalone']['getdim.py'].run()
dim=root['SETTINGS']['DEPENDENCIES']['dim']
#n_kinetic = dim['n_kinetic']
#n_theta_plot = dim['n_theta_plot']
#n_x       = dim['n_x']
#n_field      = dim['n_field']
n_n          = dim['n_n']
n_time    = dim['n_time']
time_max  = dim['time_max']
# read the data
f_k_perp_squared=open(root['OUTPUTS']['out.gyro.k_perp_squared'].filename,'Ur')
data_k_perp_squared = f_k_perp_squared.readlines()
data_k_perp_squared =array([float(item) for item in data_k_perp_squared])
# transfrom into array
#data_gbflux_array=data_gbflux.reshape((n_kinetic,n_field,4,n_time))
data_k_perp_squared_array=data_k_perp_squared.reshape((n_time,n_n))
# let's plot, note here we only plot the main parts, the others can be plotted similarly if needed
#time_max=root['INPUTS']['input.gyro']['TIME_MAX']
t=linspace(0,time_max,n_time)
figure(figsize=[6,6])
lw=2
fs1=24
fs2=20

inputgyro=root['INPUTS']['input.gyro']
rho_s=inputgyro['RHO_STAR']  # the rho_s maybe not accurate
n_min=inputgyro['TOROIDAL_MIN']
n_sep=inputgyro['TOROIDAL_SEP']
#n=n_min+n_sep*arange(n_n)
n=n_min+n_sep*arange(n_n)
q=inputgyro['SAFETY_FACTOR']
rmin=inputgyro['RADIUS']
kyarr=n*q/rmin*rho_s

# the intensity is averaged over the last 1/3 evolution time
ratio_time=root['SETTINGS']['SETUP']['ratio_time']
k_perp_squared_arr=zeros(n_n)
for n_n_k in arange(n_n):
    k_perp_squared_k_arr=[mean(data_k_perp_squared_array[n_time_k][n_n_k]) for n_time_k in arange(n_time)]
    k_perp_squared_arr[n_n_k]=mean(k_perp_squared_k_arr[int(ratio_time*n_time):-1])
# then plot the electrostatic potential over ky
plot(kyarr[1:],k_perp_squared_arr[1:],'-ko',linewidth=lw) 
#plot(kyarr[1:],k_perp_squared_arr[1:],'-ko',linewidth=lw,label='$k_{perp}$') # normally, the n=0 mode is not required to be plotted
#plot(kyarr[1:],k_perp_squared_arr[1:]-kyarr[1:]**2,'-ro',linewidth=lw,label='$k_r$') 
#plot(kyarr[1:],kyarr[1:]**2,'-bo',linewidth=lw,label='$k_{\\theta}$') 
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
xlabel('$k_y\\rho_s$',fontsize=fs2,fontname='serif')
#ylabel('$\phi-a.u.$',fontsize=fs2,fontname='serif')
legend(loc=0,fontsize=fs2).draggable(True)
title('$k_{perp}^2$',fontsize=fs1,family='serif')
