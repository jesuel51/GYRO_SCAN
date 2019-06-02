# this script is used to plot the eigenfrequency and growth rate for all the scanning cases, 
# the parameters and the value is specified in root['SETTINGS']['PLOTS']['Para'] and root['SETTINGS']['PLOTS']['Range']
# note the stability analyis should be performed by GYRO before running this plot scrip
# first we should define a function to read the date of out.gyro.freq & fieldeigen.out, which contains the frequency and growth rate
#plt.close()
import numpy as np
def readfile(filename):
    f=open(filename,'Ur')
    fread=f.readlines()
    temp=[float(item) for item in fread[-1].split()]
    w=zeros([2,1])  	# frequency and gamma
    err_w=zeros([2,1])	# error in frequency and gamma
    w[0]=temp[0]
    w[1]=temp[1]
    err_w[0]=temp[2]
    err_w[1]=temp[3]
    return w,err_w
    f.close()
# then read all the data
effnum=root['SETTINGS']['PLOTS']['effnum']
input_gyro=root['INPUTS']['input.gyro']
# note that it make no sense that scale the gamma_e in the linear run
# also, it's recommended that when doing linear calculation ,set the doppler_scale instead of gamma_e to be 0;
gamma_e=input_gyro['GAMMA_E']
kappa=input_gyro['KAPPA']
plots=root['SETTINGS']['PLOTS']
csda=plots['csda']
# set a default for the parameters
if plots['iflwphy']==1:
    plots['Para']=root['SETTINGS']['PHYSICS']['Para']
    plots['Range']=root['SETTINGS']['PHYSICS']['Range']
    plots['kyarr']=root['SETTINGS']['PHYSICS']['kyarr']
kyarr=plots['kyarr']
para=plots['Para']
Range=plots['Range']
# determine whether plot the ExB shearing rate
ipltExB=plots['ipltExB']
gammae_eff = 0.3*sqrt(kappa)*gamma_e
num_ky=len(kyarr)
#nRange=len(root['INPUTS']['TGYRO']['input.tgyro']['DIR'])
nRange=len(Range)
w_arr=zeros([nRange,num_ky])     # dominate mode frequency
err_w_arr=zeros([nRange,num_ky])     # error in dominate mode frequency
gamma_arr=zeros([nRange,num_ky]) # dominate mode growth rate
err_gamma_arr=zeros([nRange,num_ky]) # error in dominate mode growth rate
# all the information about frequency and growth rate can be get
for k in range(0,nRange):
    count2=0
#    print(str(Range[k]))
    for item in kyarr:
        if input_gyro['LINSOLVE_METHOD']==1 or not input_gyro.has_key('LINSOLVE_METHOD'):
            filename=root['OUTPUTScan'][para][str(Range[k])[0:effnum]]['lin'][str(item)[0:effnum]]['out.gyro.freq'].filename
        else:
            filename=root['OUTPUTScan'][para][str(Range[k])[0:effnum]]['lin'][str(item)[0:effnum]]['fieldeigen.out'].filename
        w,err_w=readfile(filename)
        w_arr[k][count2]=w[0]
        gamma_arr[k][count2]=w[1]
        err_w_arr[k][count2]=err_w[0]
        err_gamma_arr[k][count2]=err_w[1]
        count2=count2+1
########################################
# based on the profiles we get, then all the linear information can be plotted
figure('micro-turbulence linear stability property',figsize=[12,9])
#lab=['-kd','-ko','-k*','-md','-mo','-m*','-bd','-bo','-b*','-rd','-ro','-r*','-gd','go','-g*']
lab=['-kd','-md','-bd','-rd','-gd','-ko','-mo','-bo','-ro','-go','-k*','-m*','-b*','-r*','-g*'];#       '-ko','-k*','-md','-mo','-m*','-bd','-bo','-b*','-rd','-ro','-r*','-gd','go','-g*']
lw=2
fs1=20
fs2=16
fs3=24
ms=12
if csda[0]==1:
    w_arr=w_arr*csda[1]
    gamma_arr=gamma_arr*csda[1]
idimplt = root['SETTINGS']['PLOTS']['idimplt']  # decide using which dim to plot
# idimplt=0, default, xlabel ky, legend range
# idimplt = 1, xlabel range, legend ky
if idimplt==0:
    subplot(221)
    for k in range(0,nRange):
        plot(kyarr,w_arr[k],lab[k],linewidth=lw+1,label=str(Range[k])[0:effnum])
    plot(array([min(kyarr),max(kyarr)]),array([0,0]),'--r',linewidth=lw)
    legend(loc=1,fontsize=fs2).draggable(True)
    xlim([0.8*min(kyarr),1.2*max(kyarr)])
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    ylabel('$\omega$',fontsize=fs1)
    subplot(223)
    for k in range(0,nRange):
        plot(kyarr,gamma_arr[k],lab[k],linewidth=lw+1)
    plot(array([min(kyarr),max(kyarr)]),array([0,0]),'--r',linewidth=lw)
    if ipltExB == 1:
        plot(array([min(kyarr),max(kyarr)]),array([gammae_eff,gammae_eff]),'--m',linewidth=lw,label='$\gamma_E$')
    #legend(loc=1,fontsize=fs2).draggable(True)
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    xlim([0.8*min(kyarr),1.2*max(kyarr)])
    #ylim([1.e-3,1.e0])
    xlabel('$k_y$*$\\rho_s$',fontsize=fs1)
    ylabel('$\gamma$',fontsize=fs1)
    legend(loc=0,fontsize=fs2).draggable(True)
    #plot the error of w and gamma
    subplot(222)
    for k in range(0,nRange):
        semilogy(kyarr,err_w_arr[k],lab[k],linewidth=lw+1)
    plot(array([min(kyarr),max(kyarr)]),array([1.e-4,1.e-4]),'--r',linewidth=lw)
    #legend(loc=1,fontsize=fs2).draggable(True)
    xlim([0.8*min(kyarr),1.2*max(kyarr)])
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    ylabel('$\omega_{err}$',fontsize=fs1)
    subplot(224)
    for k in range(0,nRange):
        semilogy(kyarr,err_gamma_arr[k],lab[k],linewidth=lw+1)
    plot(array([min(kyarr),max(kyarr)]),array([1.e-4,1.e-4]),'--r',linewidth=lw)
    #legend(loc=1,fontsize=fs2).draggable(True)
#    legend(loc=1,fontsize=fs2).draggable(True)
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    xlim([0.8*min(kyarr),1.2*max(kyarr)])
    #ylim([1.e-3,1.e0])
    xlabel('$k_y$*$\\rho_s$',fontsize=fs1)
    ylabel('$\gamma_{err}$',fontsize=fs1)
else:
    numky=len(kyarr) 
    subplot(221)
    for k in range(0,numky):
        plot(Range,w_arr.T[k],lab[k],linewidth=lw+1,label=kyarr[k])
    plot(array([min(Range),max(Range)]),array([0,0]),'--r',linewidth=lw)
    legend(loc=1,fontsize=fs2).draggable(True)
#    xlim([0.8*min(kyarr),1.2*max(kyarr)])
    xlim([0.8*min(Range),1.2*max(Range)])
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    ylabel('$\omega$',fontsize=fs1)
    subplot(223)
    for k in range(0,numky):
        plot(Range,gamma_arr.T[k],lab[k],linewidth=lw+1)
    plot(array([min(Range),max(Range)]),array([0,0]),'--r',linewidth=lw)
    #legend(loc=1,fontsize=fs2).draggable(True)
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    xlim([0.8*min(Range),1.2*max(Range)])
    #ylim([1.e-3,1.e0])
    xlabel(root['SETTINGS']['PLOTS']['Para'],fontsize=fs1)
    ylabel('$\gamma$',fontsize=fs1)
    #legend(loc=0,fontsize=fs2).draggable(True)
    #plot the error of w and gamma
    subplot(222)
    for k in range(0,numky):
        semilogy(Range,err_w_arr.T[k],lab[k],linewidth=lw+1)
    plot(array([min(Range),max(Range)]),array([1.e-4,1.e-4]),'--r',linewidth=lw)
    #legend(loc=1,fontsize=fs2).draggable(True)
    xlim([0.8*min(Range),1.2*max(Range)])
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    ylabel('$\omega_{err}$',fontsize=fs1)
    subplot(224)
    for k in range(0,numky):
        semilogy(Range,err_gamma_arr.T[k],lab[k],linewidth=lw+1)
    plot(array([min(Range),max(Range)]),array([1.e-4,1.e-4]),'--r',linewidth=lw)
#    legend(loc=1,fontsize=fs2).draggable(True)
    xticks(fontsize=fs2)
    yticks(fontsize=fs2)
    xlim([0.8*min(Range),1.2*max(Range)])
    #ylim([1.e-3,1.e0])
    xlabel(root['SETTINGS']['PLOTS']['Para'],fontsize=fs1)
    ylabel('$\gamma_{err}$',fontsize=fs1)
# # ===================================
iwritelin=root['SETTINGS']['PLOTS']['iwritelin']  # determine whether to write out to a file
numky=len(kyarr) 
nmodes=1
if iwritelin==1 and root['SETTINGS']['DEPENDENCIES'].has_key('linout'):
    eigenout=root['SETTINGS']['DEPENDENCIES']['linout']
    fid=open(eigenout,'w')
# first write the scanned parameter name into the file
    fid.write(para)
    fid.write('\n')
# write the nRange and the para_val into the file
    fid.write(str(nRange))
    fid.write('\n')
    line=''
    for m in range(nRange):
        line=line+str(Range[m])+'    '
    fid.write(line)
    fid.write('\n')
# write nmodes into the file    
    fid.write(str(nmodes)+'    '+str(numky))
    fid.write('\n')
    for k in range(numky):
        line=str(kyarr[k])
        for p in range(nRange):
#            line=line+'    '+str(w_arr[p][k])+'    '+str(gamma_arr[p][k])+'    '+str(err_w_arr[p][k])+'    '+str(err_gamma_arr[p][k])
            line=line+'    '+str(w_arr[p][k])+'    '+str(gamma_arr[p][k])
        fid.write(line)
        fid.write('\n')
    fid.close()
