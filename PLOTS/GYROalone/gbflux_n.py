# this script is used to plot the file out.gyro.gbflux_n, the format of the file is 
# n_kinetic, n_field,4=i, n_n, n_time
# it's highly recommended that the scripts should be named after the gyro ouput file name
# before reading such a file, we should run one script which offer the dimentional parameter
root['PLOTS']['GYROalone']['getdim.py'].run()
dim=root['SETTINGS']['DEPENDENCIES']['dim']
n_kinetic = dim['n_kinetic']
n_field   = dim['n_field']
n_n       = dim['n_n']
n_time    = dim['n_time']
time_max  = dim['time_max']
# read the data
f_gbflux_n=open(root['OUTPUTS']['out.gyro.gbflux_n'].filename,'Ur')
data_gbflux_n = f_gbflux_n.readlines()
data_gbflux_n =array([float(item) for item in data_gbflux_n])
# transfrom into array
data_gbflux_n_array=data_gbflux_n.reshape((n_time,n_n,4,n_field,n_kinetic))
# let's plot, note here we only plot the main parts, the others can be plotted similarly if needed
#time_max=root['INPUTS']['input.gyro']['TIME_MAX']
t=linspace(0,time_max,n_time)
figure(figsize=[10,10])
lw=2
fs1=24
fs2=20
# get the kyarr
inputgyro=root['INPUTS']['input.gyro']
rho_s=inputgyro['RHO_STAR']  # the rho_s maybe not accurate
n_min=inputgyro['TOROIDAL_MIN']
n_sep=inputgyro['TOROIDAL_SEP']
#n=n_min+n_sep*arange(n_n)
n=n_min+n_sep*arange(n_n)
q=inputgyro['SAFETY_FACTOR']
rmin=inputgyro['RADIUS']
kyarr=n*q/rmin*rho_s

lab=array(['-bo','-ko','-mo','-go'])
# average over the time
ratio_time=root['SETTINGS']['SETUP']['ratio_time']
time_avg=range(int(ratio_time*n_time),n_time)
len_time_avg=len(time_avg)
# get the total ion flux
data_gbflux_n_array_ion=zeros([n_time,n_n,4,n_field])
#for nt in arange(n_time):
#    for nn in arange(n_n):
#        for nc in arange(4):  # c means flux channel
#            for nf in arange(n_field):
#                data_gbflux_n_array_ion[nt][nn][nc][nf]=sum([data_gbflux_n_array[nt][nn][nc][nf][ni] for ni in arange(n_kinetic-1)])
# named the fluxes which is more convinient for writting out to the file
Pi=zeros([n_field,n_kinetic,n_n])      # momentum flux
S=zeros([n_field,n_kinetic,n_n])        # exchange flux
Q=zeros([n_field,n_kinetic,n_n])       # energy flux
Gamma=zeros([n_field,n_kinetic,n_n])   # particle flux
for n_k in arange(n_kinetic):
    for n_f in arange(n_field):
        Pi[n_f][n_k]=[mean([data_gbflux_n_array[n_time_k][n_n_k][2][n_f][n_k] for n_time_k in time_avg]) for n_n_k in arange(n_n)]
        S[n_f][n_k]=[mean([data_gbflux_n_array[n_time_k][n_n_k][3][n_f][n_k] for n_time_k in time_avg]) for n_n_k in arange(n_n)]
        Gamma[n_f][n_k]=[mean([data_gbflux_n_array[n_time_k][n_n_k][0][n_f][n_k] for n_time_k in time_avg]) for n_n_k in arange(n_n)]
        Q[n_f][n_k]=[mean([data_gbflux_n_array[n_time_k][n_n_k][1][n_f][n_k] for n_time_k in time_avg]) for n_n_k in arange(n_n)]

subplot(2,2,1)
plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][2][0][-1] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-ro',linewidth=lw,label='Electron')  # note the first species is the main ion and the last one is electron
#plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][2][0][0] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-b',linewidth=lw,label='Main Ion') 
plot(kyarr,[mean([sum([data_gbflux_n_array[n_time_k][n_n_k][2][0][nk] for nk in arange(n_kinetic-1)],0) for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-b',linewidth=lw,label='Ion Tot') 
#plot(kyarr,[mean([data_gbflux_n_array_ion[n_time_k][n_n_k][2][0] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-bo',linewidth=lw,label='Ion_tot') 

#xticks(fontsize=fs2,fontname='serif')
xticks([])
yticks(fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
legend(loc=0,fontsize=fs2).draggable(True)
title('$\Pi$',fontsize=fs1,family='serif')
subplot(2,2,2)
plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][3][0][-1] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-ro',linewidth=lw)  
plot(kyarr,[mean([sum([data_gbflux_n_array[n_time_k][n_n_k][3][0][nk] for nk in arange(n_kinetic-1)],0) for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-b',linewidth=lw) 
#plot(kyarr,[mean([data_gbflux_n_array_ion[n_time_k][n_n_k][3][0] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-bo',linewidth=lw) 
#xticks(fontsize=fs2,fontname='serif')
xticks([])
yticks(fontsize=fs2,fontname='serif')
#ylabel('GB',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('Exchange',fontsize=fs1,family='serif')
subplot(2,2,3)
plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][0][0][-1] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-ro',linewidth=lw) 
#plot(kyarr,[mean([sum([data_gbflux_n_array[n_time_k][n_n_k][0][0][0] for nk arange(n_kinetic-1)],0) for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-b',linewidth=lw) 
#plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][0][0][0] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-bo',linewidth=lw) 
#plot(kyarr,[mean([data_gbflux_n_array_ion[n_time_k][n_n_k][0][0] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-bo',linewidth=lw) 
for ni in arange(n_kinetic-1):
    plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][0][0][ni] for n_time_k in time_avg]) for n_n_k in arange(n_n)],lab[ni],linewidth=lw,label='ni_'+str(ni)) 
legend(loc=0).draggable(True)
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
ylabel('GB',fontsize=fs2,fontname='serif')
#xlabel('t(a/c_s)',fontsize=fs2,fontname='serif')
xlabel('$k_y\\rho_s$',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('$\Gamma$',fontsize=fs1,family='serif')
subplot(2,2,4)
plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][1][0][-1] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-ro',linewidth=lw)   
plot(kyarr,[mean([sum([data_gbflux_n_array[n_time_k][n_n_k][1][0][nk] for nk in arange(n_kinetic-1)],0) for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-b',linewidth=lw) 
#plot(kyarr,[mean([data_gbflux_n_array[n_time_k][n_n_k][1][0][0] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-bo',linewidth=lw) 
#plot(kyarr,[mean([data_gbflux_n_array_ion[n_time_k][n_n_k][1][0] for n_time_k in time_avg]) for n_n_k in arange(n_n)],'-bo',linewidth=lw) 
xticks(fontsize=fs2,fontname='serif')
yticks(fontsize=fs2,fontname='serif')
#ylabel('GB',fontsize=fs2,fontname='serif')
#legend(loc=0,fontsize=fs2).draggable(True)
title('Q',fontsize=fs1,family='serif')
xlabel('$k_y\\rho_s$',fontsize=fs2,fontname='serif')
# we will try to write the file out with the format similar to that of tglf, say, nontglf.py in the TGLF_SCAN module
# the format for one line is Gamma_lowk,Gamma_highk,Qe_lowk,Qe_highk,Qi_lowk,Qi_highk,Pi_lowk,Pi_highk
iwrite=root['SETTINGS']['PLOTS']['iwrite']
para='non_specfied'  # note that here we do not scan a specified parameter but just want the output file format to match that of nontglf.py so that the file can be easily read using the same script file
nRange=1
Range=array([1])
if iwrite==1 and root['SETTINGS']['DEPENDENCIES'].has_key('gbflux_n_out'):
    fluxout=root['SETTINGS']['DEPENDENCIES']['gbflux_n_out']  # it's highly recommended that the outpuf file is named after the name of GYRO output
    fid=open(fluxout,'w')
# firstly write the scanned parameter name into the file
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
# write the number of poloidal modes into the file for flux summation
    fid.write(str(n_field)+'    '+str(n_n))
    fid.write('\n')
# both the electrostatic and electromagnetic contribution will be writen
# write the flux spectrum into the file
# fromation: row number, n_n
# colum: ky, ((pflux,Qe, Qi, Pi)*nmodes)*nRange)
#Pi=zeros([field,n_kinetic,n_n])
    for k in range(n_n):
        line=str(kyarr[k])
        for p in range(nRange):
            for n in range(n_field):
#                line=line+'    '+str(pflux[p][0][k+n*nky])+'    '+\
#                                 str(Eflux[p][0][k+n*nky])+'    '+\
#                                 str(sum([Eflux[p][m][k+n*nky] for m in range(1,ns)]))+'    '+\
#                                 str(sum([TorStrflux[p][m][k+n*nky] for m in range(1,ns)]))
                line=line+'    '+str(Gamma[n][-1][k])+'    '+\
                                str(Q[n][-1][k])+'    '+\
                                str(sum([Q[n][nk][k] for nk in arange(n_kinetic-1)]))+'    '+\
                                str(sum([Pi[n][nk][k] for nk in arange(n_kinetic)]))
        fid.write(line)
        fid.write('\n')
    fid.close()
