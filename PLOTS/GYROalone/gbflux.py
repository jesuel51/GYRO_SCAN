# this script is used to plot the file out.gyro.gbflux, the format of the file is 
# n_kinetic, n_field,4=i, n_time
# it's highly recommended that the scripts should be named after the gyro ouput file name
# before reading such a file, we should run one script which offer the dimentional parameter
root['PLOTS']['GYROalone']['getdim.py'].run()
dim=root['SETTINGS']['DEPENDENCIES']['dim']
n_kinetic = dim['n_kinetic']
n_field   = dim['n_field']
n_time    = dim['n_time']
time_max  = dim['time_max']
# read the data
f_gbflux=open(root['OUTPUTS']['out.gyro.gbflux'].filename,'Ur')
data_gbflux = f_gbflux.readlines()
data_gbflux =array([float(item) for item in data_gbflux])
# transfrom into array
#data_gbflux_array=data_gbflux.reshape((n_kinetic,n_field,4,n_time))
#data_gbflux_array=data_gbflux.reshape((n_time,4,n_field,n_kinetic)).T
data_gbflux_array=data_gbflux.reshape((n_time,4,n_field,n_kinetic))
# let's plot, note here we only plot the main parts, the others can be plotted similarly if needed
#time_max=root['INPUTS']['input.gyro']['TIME_MAX']
t=linspace(0,time_max,n_time)
figure(figsize=[10,10])
lw=2
fs1=24
fs2=20
#ratio_time=2./3
ratio_time=root['SETTINGS']['SETUP']['ratio_time']
ampfct=1.e2
time_avg=range(int(ratio_time*n_time),n_time)
len_time_avg=len(time_avg)
subplot(2,2,1)
plot(t,[data_gbflux_array[k][2][0][-1] for k in arange(n_time)],'-r',linewidth=lw,label='Electron')  # note the first species is the main ion and the last one is electron
#plot(t,[data_gbflux_array[k][2][0][0] for k in arange(n_time)],'-m',linewidth=lw,label='Ion')
plot(t,[sum([data_gbflux_array[k][2][0][nk] for nk in arange(n_kinetic-1)],0) for k in arange(n_time)],'-b',linewidth=lw,label='Ion_tot')
# also, we need to plot the avarage value
Pi_e=mean([data_gbflux_array[k][2][0][-1] for k in time_avg])
Pi_i=mean([sum([data_gbflux_array[k][2][0][nk] for nk in arange(n_kinetic-1)],0) for k in time_avg])
plot(t[time_avg],Pi_e*ones(len_time_avg),'-r',linewidth=lw+1)
plot(t[time_avg],Pi_i*ones(len_time_avg),'-b',linewidth=lw+1)
text(t[int(mean(time_avg))],Pi_e,int(Pi_e*ampfct)/ampfct,color='r',fontsize=fs2)
text(t[int(mean(time_avg))],Pi_i,int(Pi_i*ampfct)/ampfct,color='b',fontsize=fs2)
print('Pi_e=%5.2f,Pi_i=%5.2f'%(Pi_e,Pi_i))
#xticks(fontsize=fs2,fontname='serif')
xticks([])
yticks(fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
legend(loc=0,fontsize=fs2).draggable(True)
title('$\Pi$',fontsize=fs1,family='serif')
subplot(2,2,2)
plot(t,[data_gbflux_array[k][3][0][-1] for k in arange(n_time)],'-r',linewidth=lw)
#plot(t,[data_gbflux_array[k][3][0][0] for k in arange(n_time)],'-b',linewidth=lw)
plot(t,[sum([data_gbflux_array[k][3][0][nk] for nk in arange(n_kinetic-1)],0) for k in arange(n_time)],'-b',linewidth=lw)
# also, we need to plot the avarage value
Exch_e=mean([data_gbflux_array[k][3][0][-1] for k in time_avg])
#Exch_i=mean([data_gbflux_array[k][3][0][0] for k in time_avg])
Exch_i=mean([sum([data_gbflux_array[k][3][0][nk] for nk in arange(n_kinetic-1)],0) for k in time_avg])
plot(t[time_avg],Exch_e*ones(len_time_avg),'-r',linewidth=lw+1)
plot(t[time_avg],Exch_i*ones(len_time_avg),'-b',linewidth=lw+1)
text(t[int(mean(time_avg))],Exch_e,int(Exch_e*ampfct)/ampfct,color='r',fontsize=fs2)
text(t[int(mean(time_avg))],Exch_i,int(Exch_i*ampfct)/ampfct,color='b',fontsize=fs2)
print('Exch_e=%5.2f,Exch_i=%5.2f'%(Exch_e,Exch_i))
#xticks(fontsize=fs2,fontname='serif')
xticks([])
yticks(fontsize=fs2,fontname='serif')
#ylabel('GB',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('Exchange',fontsize=fs1,family='serif')
subplot(2,2,3)
plot(t,[data_gbflux_array[k][0][0][-1] for k in arange(n_time)],'-r',linewidth=lw)
#plot(t,[data_gbflux_array[k][0][0][0] for k in arange(n_time)],'-b',linewidth=lw)
#plot(t,[sum([data_gbflux_array[k][0][0][nk] for nk in arange(n_kinetic-1)],0) for k in arange(n_time)],'-b',linewidth=lw)
# also, we need to plot the avarage value
Gamma_e=mean([data_gbflux_array[k][0][0][-1] for k in time_avg])
#Gamma_i=mean([data_gbflux_array[k][0][0][0] for k in time_avg])
plot(t[time_avg],Gamma_e*ones(len_time_avg),'-r',linewidth=lw+1)
#plot(t[time_avg],Gamma_i*ones(len_time_avg),'-b',linewidth=lw+1)
text(t[int(mean(time_avg))],Gamma_e,int(Gamma_e*ampfct)/ampfct,color='r',fontsize=fs2)
#text(t[int(mean(time_avg))],Gamma_i,int(Gamma_i*ampfct)/ampfct,color='b',fontsize=fs2)
#print('Gamma_e=%5.2f,Gamma_i=%5.2f'%(Gamma_e,Gamma_i))
print('Gamma_e=%5.2f'%(Gamma_e))
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
xlabel('t(a/c_s)',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('$\Gamma$',fontsize=fs1,family='serif')
subplot(2,2,4)
plot(t,[data_gbflux_array[k][1][0][-1] for k in arange(n_time)],'-r',linewidth=lw)
#plot(t,[data_gbflux_array[k][1][0][0] for k in arange(n_time)],'-b',linewidth=lw)
plot(t,[sum([data_gbflux_array[k][1][0][nk] for nk in arange(n_kinetic-1)],0) for k in arange(n_time)],'-b',linewidth=lw)
# the magnetic fluttering part of Qe will also be plot
if n_field>1:
    plot(t,[data_gbflux_array[k][1][1][-1] for k in arange(n_time)],'-m',linewidth=lw)
# also, we need to plot the avarage value
Q_e_Phi=mean([data_gbflux_array[k][1][0][-1] for k in time_avg])
if n_field>1:
    Q_e_A=mean([data_gbflux_array[k][1][1][-1] for k in time_avg])
#Q_i=mean([data_gbflux_array[k][1][0][0] for k in time_avg])
Q_i=mean([sum([data_gbflux_array[k][1][0][nk] for nk in arange(n_kinetic-1)],0) for k in time_avg])
plot(t[time_avg],Q_e_Phi*ones(len_time_avg),'-r',linewidth=lw+1)
if n_field>1:
    plot(t[time_avg],Q_e_A*ones(len_time_avg),'-m',linewidth=lw+1)
plot(t[time_avg],Q_i*ones(len_time_avg),'-b',linewidth=lw+1)
text(t[int(mean(time_avg))],Q_e_Phi,int(Q_e_Phi*ampfct)/ampfct,color='r',fontsize=fs2)
if n_field>1:
    text(t[int(mean(time_avg))],Q_e_A,int(Q_e_A*ampfct)/ampfct,color='m',fontsize=fs2)
text(t[int(mean(time_avg))],Q_i,int(Q_i*ampfct)/ampfct,color='b',fontsize=fs2)
if n_field>1:
    print('Q_e=%5.2f,Q_i=%5.2f'%(Q_e_Phi+Q_e_A,Q_i))
else:
    print('Q_e=%5.2f,Q_i=%5.2f'%(Q_e_Phi,Q_i))

xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('Q',fontsize=fs1,family='serif')
xlabel('t(a/c_s)',fontsize=fs2,fontname='serif')
