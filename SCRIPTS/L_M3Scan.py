# this script is used to scan the linear stability of different ky using Holland's method
# this script can be used for scan of multiple parameter value, just like the initial value scan
# so the output of this script should be comptible to the PLOTS script, 
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
root['INPUTS']['input.gyro_bak']=root['INPUTS']['input.gyro'].duplicate()
para_name=root['SETTINGS']['PHYSICS']['Para']
para_rang=root['SETTINGS']['PHYSICS']['Range']
ncount=-1
root['OUTPUTS']=OMFITtree()
# we need to get the initial guess of wr and wi for different parameter value
# note the length of wr_guess should be identical to length of root['SETTINGS']['PHYSICS']['Range']
wr_guess=root['SETTINGS']['PHYSICS']['wr_guess']
wi_guess=root['SETTINGS']['PHYSICS']['wi_guess']
# we are going to give a check of length(wr_guess)=length(Range), if this is not satified, the simulation will be aborted
if not len(wr_guess)==len(para_rang):
    print('length of wr_guess must be identical to Range')
    os._exit()
for para_val in para_rang:
    ncount=ncount+1
    inputgyro[para_name]=para_val
    inputgyro['FIELDEIGEN_WR']=wr_guess[ncount-1]
    inputgyro['FIELDEIGEN_WI']=wi_guess[ncount-1]
    nPara=2
    while root['SETTINGS']['PHYSICS'].has_key('Para'+str(nPara)) and root['SETTINGS']['PHYSICS'].has_key('Range'+str(nPara)):
        inputgyro[root['SETTINGS']['PHYSICS']['Para'+str(nPara)]]=root['SETTINGS']['PHYSICS']['Range'+str(nPara)][ncount]
        nPara=nPara+1
    if not root['OUTPUTScan'].has_key(para_name):
        root['OUTPUTScan'][para_name]=OMFITtree()
    if not root['OUTPUTScan'][para_name].has_key(str(para_val)[0:effnum]):
        root['OUTPUTScan'][para_name][str(para_val)[0:effnum]]=OMFITtree()
    if not root['OUTPUTScan'][para_name][str(para_val)[0:effnum]].has_key('lin'):
        root['OUTPUTScan'][para_name][str(para_val)[0:effnum]]['lin']=OMFITtree()
    count2=0
    for ky in kyarr:
        count2=count2+1
        inputgyro['L_Y']=ky
    # before runing ,we need to get the output of the previous run when it's not a first run for a new para value
    # for the first run of a new para, the initial guess of wr and wi should be obtained from root['SETTINGS']['PHYSICS']['wr(i)_guess']
        if count2>1:
            line_last=readfreq(root['OUTPUTS']['fieldeigen.out'].filename)
            inputgyro['FIELDEIGEN_WR']=line_last[0]
            inputgyro['FIELDEIGEN_WI']=line_last[1]
        root['SCRIPTS']['runGYRO.py'].run()
    # now we need to store the data
        if not root['OUTPUTScan'][para_name][str(para_val)[0:effnum]]['lin'].has_key(str(ky)[0:effnum]):
            root['OUTPUTScan'][para_name][str(para_val)[0:effnum]]['lin'][str(ky)[0:effnum]]=OMFITtree()
        root['OUTPUTScan'][para_name][str(para_val)[0:effnum]]['lin'][str(ky)[0:effnum]]['input.gyro']=inputgyro.duplicate()
        for item in root['OUTPUTS'].keys():
            root['OUTPUTScan'][para_name][str(para_val)[0:effnum]]['lin'][str(ky)[0:effnum]][item]=root['OUTPUTS'][item].duplicate()
