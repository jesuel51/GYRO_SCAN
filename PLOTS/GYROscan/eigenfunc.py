# this script is used to give the linear information of gyro
# including 2 part, 1, plot the eigenfunction, 2, print the eigenfrequency and growth rate
# first we define a function to read the out.gyro.freq
# next step we would like to put those files to be independent files
def readfreq(filename):
    f=open(filename,'Ur')
    fread=f.readlines()
    return fread[-1]     # the format is wr, wi, err_wr, err_wi
    f.close()
# then we define a function to read the out.gyro.balloon_phi
def readballoon(filename,ntheta,nr):
# ntheta is ntheta_plot, nr is the radial grid
    f=open(filename,'Ur')
    fread=f.readlines()
    Rephi=zeros(ntheta*nr)
    Imphi=zeros(ntheta*nr)
    for k in arange(ntheta*nr):
        Rephi[k]=float(fread[-ntheta*nr+k].split()[0])
        Imphi[k]=float(fread[-ntheta*nr+k].split()[1])
    return Rephi,Imphi
    f.close()
# let's get the important parameter
inputgyro=root['INPUTS']['input.gyro']
if inputgyro.has_key('THETA_PLOT'):
    ntheta = inputgyro['THETA_PLOT']
else:
    ntheta = 1
if inputgyro.has_key('RADIAL_GRID'):
    nr = inputgyro['RADIAL_GRID']
else:
    nr = 6
# the name, value and ky should be specified 
plots=root['SETTINGS']['PLOTS']
effnum=plots['effnum']
para=plots['Para']
paraval_eigen=plots['paraval_eigen']
ky_eigen=plots['ky_eigen']
datanode=root['OUTPUTScan'][para][str(paraval_eigen)[0:effnum]]['lin'][str(ky_eigen)[0:effnum]]
# let's get the data and plot
fieldon=array([0,0,0,0])
# balloon data
if os.path.getsize(datanode['out.gyro.balloon_phi'].filename):
    Rephi,Imphi=readballoon(datanode['out.gyro.balloon_phi'].filename,ntheta,nr)
    fieldon[0]=1
if datanode.has_key('out.gyro.balloon_epar') and os.path.getsize(datanode['out.gyro.balloon_epar'].filename):
    Reepar,Imepar=readballoon(datanode['out.gyro.balloon_epar'].filename,ntheta,nr)
    fieldon[1]=1
if datanode.has_key('out.gyro.balloon_a') and os.path.getsize(datanode['out.gyro.balloon_a'].filename):
    Rea,Ima=readballoon(datanode['out.gyro.balloon_a'].filename,ntheta,nr)
    fieldon[2]=1
if datanode.has_key('out.gyro.balloon_b') and os.path.getsize(datanode['out.gyro.balloon_b'].filename):
    Reb,Imb=readballoon(datanode['out.gyro.balloon_b'].filename,ntheta,nr)
    fieldon[3]=1
theta=-1*(nr+1)+2*nr*linspace(0,nr*ntheta-1,nr*ntheta)/nr/ntheta
figure(figsize=[8,8])
lw=2
fs1=24
fs2=20
subplot(221)
if fieldon[0]==1:
    plot(theta,Rephi,'-b',linewidth=lw,label='Re')
    plot(theta,Imphi,'-r',linewidth=lw,label='Im')
    plot(array([min(theta),max(theta)]),array([0,0]),'--r',linewidth=lw/2.)
    xlim([1-nr,nr-1])
#    xlim([-3,3])  # for better comparison with TGLF
    #xlabel('$\\theta\\pi$',fontsize=fs1,family='serif')
    xticks(fontsize=fs2,family='serif')
    ylabel('au',fontsize=fs1,family='serif')
    yticks(fontsize=fs2,family='serif')
    title('$\phi$',fontsize=fs1,family='serif')
    legend(loc=0,fontsize=fs2).draggable(True)
subplot(222)
if fieldon[1]==1:
    plot(theta,Reepar,'-b',linewidth=lw,label='Re')
    plot(theta,Imepar,'-r',linewidth=lw,label='Im')
    plot(array([min(theta),max(theta)]),array([0,0]),'--r',linewidth=lw/2.)
xlim([1-nr,nr-1])
#xlim([-3,3])
#xlabel('$\\theta\\pi$',fontsize=fs1,family='serif')
xticks(fontsize=fs2,family='serif')
#ylabel('au',fontsize=fs1,family='serif')
yticks([],fontsize=fs2,family='serif')
title('$E_{||}$',fontsize=fs1,family='serif')
subplot(223)
if fieldon[2]==1:
    plot(theta,Rea,'-b',linewidth=lw,label='Re')
    plot(theta,Ima,'-r',linewidth=lw,label='Im')
    plot(array([min(theta),max(theta)]),array([0,0]),'--r',linewidth=lw/2.)
xlim([1-nr,nr-1])
#xlim([-3,3])
xlabel('$\\theta\\pi$',fontsize=fs1,family='serif')
xticks(fontsize=fs2,family='serif')
ylabel('au',fontsize=fs1,family='serif')
yticks(fontsize=fs2,family='serif')
title('$A_{||}$',fontsize=fs1,family='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
#legend(loc=0,fontsize=fs2).draggable(True)
subplot(224)
if fieldon[3]==1:
    plot(theta,Reb,'-b',linewidth=lw,label='Re')
    plot(theta,Imb,'-r',linewidth=lw,label='Im')
    plot(array([min(theta),max(theta)]),array([0,0]),'--r',linewidth=lw/2.)
xlim([1-nr,nr-1])
#xlim([-3,3])
xlabel('$\\theta\\pi$',fontsize=fs1,family='serif')
xticks(fontsize=fs2,family='serif')
#ylabel('au',fontsize=fs1,family='serif')
yticks([],fontsize=fs2,family='serif')
title('$B_{||}$',fontsize=fs1,family='serif')
#legend(loc=0,fontsize=fs2).draggable(True)

# growth data
if datanode.has_key('out.gyro.freq'):
    wrwi=readfreq(datanode['out.gyro.freq'].filename)
else:
    wrwi=readfreq(datanode['fieldeigen.out'].filename)
wrwi=[float(ele) for ele in wrwi.split()]
print('wr = %f, wi = %f'%(wrwi[0],wrwi[1]))
print('err_wr = %f, err_wi = %f'%(wrwi[2],wrwi[3]))
