# this script is used to plot the file out.gyro.moment_u, the format of the file is 
# 2, n_theta_plot, n_x, n_field, n_n, n_time
# it's highly recommended that the scripts should be named after the gyro ouput file name
# before reading such a file, we should run one script which offer the dimentional parameter
root['PLOTS']['GYROalone']['getdim.py'].run()
dim=root['SETTINGS']['DEPENDENCIES']['dim']
#n_kinetic = dim['n_kinetic']
n_theta_plot = dim['n_theta_plot']
n_x          = dim['n_x']
n_field      = dim['n_field']
n_n          = dim['n_n']
n_time       = dim['n_time']
time_max  = dim['time_max']
ratio_time=root['SETTINGS']['SETUP']['ratio_time']
# define a easy function to take the length square of a vector
def modde(vec):
#    len_vec=len(vec)
    mod_len=sum([val**2 for val in vec])
    return mod_len
# read the data
f_moment_u=open(root['OUTPUTS']['out.gyro.moment_u'].filename,'Ur')
data_moment_u = f_moment_u.readlines()
data_moment_u =array([float(item) for item in data_moment_u])
# transfrom into array
#data_gbflux_array=data_gbflux.reshape((n_kinetic,n_field,4,n_time))
data_moment_u_array=data_moment_u.reshape((n_time,n_n,n_field,n_x,n_theta_plot,2))
# let's plot, note here we only plot the main parts, the others can be plotted similarly if needed
#time_max=root['INPUTS']['input.gyro']['TIME_MAX']
t=linspace(0,time_max,n_time)
figure(figsize=[12,8])
lw=2
fs1=24
fs2=20
time_avg=range(int(ratio_time*n_time),n_time)
len_time_avg=len(time_avg)
subplot(1,2,1)
# time trace of zonal flow and non zonal flow evoluation
# n=0 part
##phi_zf=[sqrt(mean([[data_moment_u_array[k][0][0][n_x_k][n_theta_plot_k][0]**2 for n_x_k in arange(n_x)] for n_theta_plot_k in arange(n_theta_plot)])) for k in arange(n_time)]
#phi_zf=[sqrt(mean([data_moment_u_array[k][0][0][n_x_k][0][0]**2 for n_x_k in arange(n_x)])) for k in arange(n_time)]
phi_zf=[sqrt(mean([modde(data_moment_u_array[k][0][0][n_x_k][0]) for n_x_k in arange(n_x)])) for k in arange(n_time)]
plot(t,phi_zf,'-b',linewidth=lw,label='n=0')
# n>0 part
#phi_nonzf=[sqrt(sum([mean([[data_moment_u_array[k][n_n_k][0][n_x_k][n_theta_plot_k][0]**2 for n_x_k in arange(n_x)] for n_theta_plot_k in arange(n_theta_plot)]) for n_n_k in range(0,n_n)])) for k in arange(n_time)]
#phi_nonzf=[sqrt(sum([mean([data_moment_u_array[k][n_n_k][0][n_x_k][0][0]**2 for n_x_k in arange(n_x)]) for n_n_k in range(1,n_n)])) for k in range(0,n_time)]
phi_nonzf=[sqrt(sum([mean([modde(data_moment_u_array[k][n_n_k][0][n_x_k][0]) for n_x_k in arange(n_x)]) for n_n_k in range(1,n_n)])) for k in range(0,n_time)]
#phi_nonzf=[sum([sqrt(mean([[data_moment_u_array[k][n_n_k][0][n_x_k][n_theta_plot_k][0]**2 for n_x_k in arange(n_x)] for n_theta_plot_k in arange(n_theta_plot)])) for n_n_k in range (1,n_n)]) for k in arange(n_time)]
#phi_nonzf=[sqrt(mean(sum([[[data_moment_u_array[k][n_n_k][0][n_x_k][n_theta_plot_k][0]**2 for n_x_k in arange(n_x)] for n_theta_plot_k in arange(n_theta_plot)] for n_n_k in range(1,n_n)]))) for k in arange(n_time)]
plot(t,phi_nonzf,'-r',linewidth=lw,label='n>0')
#for n_n_k in range(1,n_n):
#    plot(t,[sqrt(mean([[data_moment_u_array[k][n_n_k][0][n_x_k][n_theta_plot_k][0]**2 for n_x_k in arange(n_x)] for n_theta_plot_k in arange(n_theta_plot)])) for k in arange(n_time)],'-',linewidth=lw)
#for n_x_k in arange(n_x):
#    plot(t,[data_moment_u_array[k][0][0][n_x_k][0][0] for k in arange(n_time)],linewidth=lw)
# get the time_averaged zonal and non-zonal flow
phi_zf_mean=mean([phi_zf[k]for k in time_avg])
phi_nonzf_mean=mean([phi_nonzf[k] for k in time_avg])
plot(t[time_avg],phi_zf_mean*ones(len_time_avg),'-b',linewidth=lw)
plot(t[time_avg],phi_nonzf_mean*ones(len_time_avg),'-r',linewidth=lw)
print('phi_zf=%5.3f,phi_nonzf=%5.3f'%(phi_zf_mean,phi_nonzf_mean))
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
xlabel('$t(a/c_s)$',fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
legend(loc=0,fontsize=fs2).draggable(True)
title('$\phi$',fontsize=fs1,family='serif')

subplot(1,2,2)
lab=['-kd','-md','-bd','-rd','-gd','-ko','-mo','-bo','-ro','-go','-k*','-m*','-b*','-r*','-g*']
# the intensity over toroidal mode n(ky*rho_s)
inputgyro=root['INPUTS']['input.gyro']
time_skip = inputgyro['TIME_SKIP']
rho_s=inputgyro['RHO_STAR']  # the rho_s maybe not accurate
n_min=inputgyro['TOROIDAL_MIN']
n_sep=inputgyro['TOROIDAL_SEP']
#n=n_min+n_sep*arange(n_n)
n=n_min+n_sep*arange(n_n)
q=inputgyro['SAFETY_FACTOR']
rmin=inputgyro['RADIUS']
kyarr=n*q/rmin*rho_s


# the intensity is averaged over the last 1/3 evolution time by default
# t_trace is used to indicate the time slice so that we can get the evolution of the flux specturm by the nonlinear run of GYRO
# the t_trace is in the unit of a/cs
time_step=inputgyro['TIME_STEP']
t_trace=root['SETTINGS']['PLOTS']['t_trace']
n_t_trace=len(t_trace)
ind_t_trace=[int(item/time_skip/time_step) for item in t_trace]
if t_trace[0]<0:
    phi_arr=zeros(n_n)
else:
    phi_arr=zeros([n_n,n_t_trace])

for n_n_k in arange(n_n):
#    phi_k_arr=[sqrt(mean([data_moment_u_array[n_time_k][n_n_k][0][n_x_k][0][0]**2 for n_x_k in arange(n_x)])) for n_time_k in arange(n_time)]
    phi_k_arr=[sqrt(mean([modde(data_moment_u_array[n_time_k][n_n_k][0][n_x_k][0]) for n_x_k in arange(n_x)])) for n_time_k in arange(n_time)]
    if t_trace[0] < 0:   # if t_trace is negative, then only the final state will be recorded and plotted
        phi_arr[n_n_k]=mean(phi_k_arr[int(ratio_time*n_time):-1])
    else:
        for k in arange(n_t_trace):
            phi_arr[n_n_k][k]=mean(phi_k_arr[ind_t_trace[k]-1:ind_t_trace[k]+1])
# then plot the electrostatic potential over ky
if t_trace[0]<0:
    plot(kyarr[1:],phi_arr[1:],'-ko',linewidth=lw) # normally, the n=0 mode is not required to be plotted
else:
    for k in arange(n_t_trace):
        plot(kyarr[1:],phi_arr.T[k][1:],lab[k],linewidth=lw,label=str(t_trace[k]))
    legend(loc=0,fontsize=fs2).draggable(True)
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
xlabel('$k_y\\rho_s$',fontsize=fs2,fontname='serif')
#ylabel('$\phi-a.u.$',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('$\phi$',fontsize=fs1,family='serif')

# try to write the finally fluctualing field spectrum averaged over the [ratio_time,1]*time range
#data_moment_u_array=data_moment_u.reshape((n_time,n_n,n_field,n_x,n_theta_plot,2))
field_arr=zeros([n_field,n_n])
for n_f in arange(n_field):
    for n_n_k in arange(n_n):
        field_temp=[sqrt(mean([modde(data_moment_u_array[n_time_k][n_n_k][n_f][n_x_k][0]) for n_x_k in arange(n_x)])) for n_time_k in arange(n_time)]
        field_arr[n_f][n_n_k]=mean(field_temp[int(ratio_time*n_time):-1])
# write the data output
if root['SETTINGS']['PLOTS']['iwrite']==1 and root['SETTINGS']['DEPENDENCIES'].has_key('moment_u_out'):
    moment_u_out=root['SETTINGS']['DEPENDENCIES']['moment_u_out']
    fid=open(moment_u_out,'w')
# write the fluctuation field amplitude to the output file
# format, row number, n_n
# column : ky, phi, (Bper,Bpar)
    for k in arange(n_n):
        line=str(kyarr[k])
        for n_f in arange(n_field):
            line=line+'    '+str(field_arr[n_f][k])
        fid.write(line)
        fid.write('\n')
    fid.close()
