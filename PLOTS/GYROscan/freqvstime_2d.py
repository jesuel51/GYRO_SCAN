# this script is used to plot the time traces of the freq and gamma versus the time
# first we need a function to read the out.gyro.freq
import numpy as np
def readfile(filename):
    f=open(filename,'Ur')
    fread=f.readlines()
    num=len(fread)
    omega=zeros([num,1])
    err_omega=zeros([num,1])
    gamma=zeros([num,1])
    err_gamma=zeros([num,1])
    for k in range(num):
        temp=[float(item) for item in fread[k].split()]
        omega[k]=temp[0]
        err_omega[k]=temp[2]
        gamma[k]=temp[1]
        err_gamma[k]=temp[3]
    return omega,err_omega,gamma,err_gamma
    f.close()

## the name, value and ky should be specified 
plots=root['SETTINGS']['PLOTS']['2d']
effnum=root['SETTINGS']['PLOTS']['effnum']
para_x=plots['Para_x']
para_y=plots['Para_x']
para_x_eigen=plots['para_x_eigen']
para_y_eigen=plots['para_y_eigen']
ky_eigen=plots['kyarr']
datanode=root['OUTPUTScan'][para_y][str(para_y_eigen)[0:effnum]]['lin'][str(para_x_eigen)[0:effnum]]
time_max=abs(int(datanode['input.gyro']['TIME_MAX']))
omega,err_omega,gamma,err_gamma=readfile(datanode['out.gyro.freq'].filename)
ntime=len(omega)
time=linspace(0,time_max,ntime)
# start to plot
figure(figsize=[8,8])
lw=2
fs1=24
fs2=20
subplot(211)
plot(time,omega,'-k',linewidth=lw,label='$\omega$')
plot(time,gamma,'-g',linewidth=lw,label='$\gamma$')
plot(array([0,time_max]),array([0,0]),'-r',linewidth=lw/2.)
legend(fontsize=fs2,loc=0).draggable(True)
xticks(fontsize=fs2)
yticks(fontsize=fs2)
#xlim([0,time_max])
#xlabel('t(a/c_s)',fontsize=fs1)
ylabel('freq',fontsize=fs1)
subplot(212)
semilogy(time,err_omega,'-k',linewidth=lw,label='$err_{\omega}$')
semilogy(time,err_gamma,'-g',linewidth=lw,label='$err_{\gamma}$')
plot(array([0,time_max]),array([0,0]),'-r',linewidth=lw/2.)
legend(fontsize=fs2,loc=0).draggable(True)
xticks(fontsize=fs2)
yticks(fontsize=fs2)
xlim([0,time_max])
ylim([1.e-4,10])
xlabel('t(a/c_s)',fontsize=fs1)
ylabel('$err_{freq}$',fontsize=fs1)
