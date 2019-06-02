# LM3_SCAN2 : the input is the (guess)wr&wi for a fixed ky(eg,ky=0.3) for different scanned parameter value, using holland method for different ky, the interval of ky should be very small
# LM3_SCAN3 : the input is the (guess)wr&wi for a fixed parameter value (eg, betaE=0) for different ky, using holland method for diffent parameter value, interval of parameter value should be very small
# imthd = 1: use the output of previous iteration as the next initial guess
# imthd = 2, the initial guess will not be changed but stays to the one which is initially setup
# first we need to define a function to read the fieldeigen.out
def readfreq(filename):
    f=open(filename,'Ur')
    fread=f.readlines()
    line_last=[float(item) for item in fread[-1].split()]     # the format is wr, wi, err_wr, err_wi
    return line_last
    f.close()
# before using this method, some parameters should be set accordingly
effnum=root['SETTINGS']['PLOTS']['effnum']
inputgyro=root['INPUTS']['input.gyro']
inputgyro['NONLINEAR_FLAG'] = 0
inputgyro['BOX_MULTIPLIER'] = -1
inputgyro['LINSOLVE_METHOD'] = 3
root['SCRIPTS']['set_resolution.py'].run()
inputgyro['ELECTRON_METHOD']=4
kyarr=root['SETTINGS']['PHYSICS']['kyarr']
para_name=root['SETTINGS']['PHYSICS']['Para']
para_rang_orig=root['SETTINGS']['PHYSICS']['Range']
nrang=len(para_rang_orig)
nky=len(kyarr)
# we need to get the initial guess of wr and wi for different parameter value
# note the length of wr_guess should be identical to length of root['SETTINGS']['SETUP']['kyarr']
wr_guess_orig=root['SETTINGS']['PHYSICS']['wr_guess']
wi_guess_orig=root['SETTINGS']['PHYSICS']['wi_guess']
# we are going to give a check of length(wr_guess)=length(kyarr), if this is not satified, the simulation will be aborted
#if not len(wr_guess)==nrang:
if not len(wr_guess_orig)==nky:
    print('length of wr_guess must be identical to nky')
    raise Exception('length of wr_guess must be identical to nky')
#    os._exit()
# set one tag for the run in subscan_lin.py
root['SETTINGS']['SETUP']['iscan_3']=1
case_tag=root['SETTINGS']['PHYSICS']['case_tag']
# find the nPara, the parameter number to scan
nPara=2
while root['SETTINGS']['PHYSICS'].has_key('Para'+str(nPara)) and root['SETTINGS']['PHYSICS'].has_key('Range'+str(nPara)):
    nPara=nPara+1
## prepare for the first run
#root['SETTINGS']['PHYSICS']['Para'+str(nPara)]='FIELDEIGEN_WR'
#root['SETTINGS']['PHYSICS']['Para'+str(nPara+1)]='FIELDEIGEN_WI'
#root['SETTINGS']['PHYSICS']['Range'+str(nPara)]=wr_guess
#root['SETTINGS']['PHYSICS']['Range'+str(nPara+1)]=wi_guess
# start iteration
#wr_temp=zeros(nrang)
wr_temp=zeros(nky)
#wi_temp=zeros(nrang)
wi_temp=zeros(nky)
#for ky in kyarr:
#    root['SETTINGS']['SETUP']['kyarr']=array([ky])
#    count=0
#    root['SCRIPTS']['subscan_lin.py'].run()
#    for para_val in para_rang:
#        line_last=readfreq(root['Cases'][case_tag][para_name+'~'+str(para_val)[0:effnum]+'~ky~'+str(ky)[0:effnum]]['fieldeigen.out'].filename)
#        wr_temp[count]=line_last[0]
#        wi_temp[count]=line_last[1]
#        count=count+1
##
for para_val in para_rang_orig:
    root['SETTINGS']['PHYSICS']['Range']=array([para_val])
    count=0
    root['SCRIPTS']['subscan_lin.py'].run()
    for ky in kyarr:
        line_last=readfreq(root['Cases'][case_tag][para_name+'~'+str(para_val)[0:effnum]+'~ky~'+str(ky)[0:effnum]]['fieldeigen.out'].filename)
        wr_temp[count]=line_last[0]
        wi_temp[count]=line_last[1]
        count=count+1
    # prepare for the next iteration
#    root['SETTINGS']['PHYSICS']['Range'+str(nPara)]=wr_temp
    if root['SETTINGS']['PHYSICS']['imthd']==1:
        root['SETTINGS']['PHYSICS']['wr_guess']=wr_temp
        root['SETTINGS']['PHYSICS']['wi_guess']=wi_temp
#    root['SETTINGS']['PHYSICS']['Range'+str(nPara+1)]=wi_temp
# Cha pi gu
#del root['SETTINGS']['PHYSICS']['Para'+str(nPara)]
#del root['SETTINGS']['PHYSICS']['Range'+str(nPara)]
#del root['SETTINGS']['PHYSICS']['Para'+str(nPara+1)]
#del root['SETTINGS']['PHYSICS']['Range'+str(nPara+1)]
del  root['SETTINGS']['SETUP']['iscan_3']
root['SETTINGS']['PHYSICS']['wr_guess']=wr_guess_orig
root['SETTINGS']['PHYSICS']['wi_guess']=wi_guess_orig
root['SETTINGS']['PHYSICS']['Range']=para_rang_orig
#root['SETTINGS']['SETUP']['kyarr']=kyarr
# store the data
for item in root['Cases'][case_tag].keys():
    item_temp=item.split('~')
    if not  root['OUTPUTScan'].has_key(item_temp[0]):
        root['OUTPUTScan'][item_temp[0]]=OMFITtree()
    if not  root['OUTPUTScan'][item_temp[0]].has_key(item_temp[1]):
        root['OUTPUTScan'][item_temp[0]][item_temp[1]]=OMFITtree()
    if not root['OUTPUTScan'][item_temp[0]][item_temp[1]].has_key('lin'):
        root['OUTPUTScan'][item_temp[0]][item_temp[1]]['lin']=OMFITtree()
    root['OUTPUTScan'][item_temp[0]][item_temp[1]]['lin'][item_temp[3]]=OMFITtree()
    for files in root['Cases'][case_tag][item]:
        root['OUTPUTScan'][item_temp[0]][item_temp[1]]['lin'][item_temp[3]][files]=root['Cases'][case_tag][item][files]

