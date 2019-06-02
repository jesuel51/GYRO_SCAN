# LM3_SCAN2 : the input is the (guess)wr&wi for a fixed ky(eg,ky=0.3) for different scanned parameter value, using holland method for different ky, the interval of ky should be very small
# LM3_SCAN3 : the input is the (guess)wr&wi for a fixed parameter value (eg, betaE=0) for different ky, using holland method for diffent parameter value, interval of parameter value should be very small
# LM3_SCAN_2d : the input is the (guess)wr&wi for a fixed para_y and various para_x, len(wr)=len(wi)=len(Range_x) should be satisfied.
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
# record the original values
para_rang_orig=root['SETTINGS']['PHYSICS']['Range']
kyarr=root['SETTINGS']['PHYSICS']['kyarr'] # actually only 1 ky is allowed for this script
para_x=root['SETTINGS']['PHYSICS']['2d']['Para_x']  # similar to ky in LM3_SCAN3
para_y=root['SETTINGS']['PHYSICS']['2d']['Para_y']  
Range_x=root['SETTINGS']['PHYSICS']['2d']['Range_x']
Range_y=root['SETTINGS']['PHYSICS']['2d']['Range_y']
nrangex=len(Range_x)
nrangey=len(Range_y)
# we need to get the initial guess of wr and wi for different para_x values
# note the len(wr_guess_orig)=len(para_x) should be satisfied and should be checked
wr_guess_orig=root['SETTINGS']['PHYSICS']['wr_guess']
wi_guess_orig=root['SETTINGS']['PHYSICS']['wi_guess']
if not len(wr_guess_orig)==nrangex:
    print('length of wr_guess must be identical to len(Range_x)')
    raise Exception('length of wr_guess must be identical to len(Range_x)')
#    os._exit()
case_tag=root['SETTINGS']['PHYSICS']['case_tag']
# we have 2 method to do the run
# imthd=root['SETTINGS']['PLOTS']['2d']['imthd']
# imthd = 1, use the output the previous iteration as the input of next iteration
# imthd = 2, the input are the same for each element in range_y
# for both the 2 methods, len(range_x)=len(wr_guess) should be satisfied
# start iteration
imthd=root['SETTINGS']['PHYSICS']['2d']['imthd']
if imthd == 1:
    wr_temp=zeros(nrangex)
    wi_temp=zeros(nrangex)
    for para_val_y in Range_y:
        root['SETTINGS']['PHYSICS']['Range']=array([para_val_y])
        count=0
        root['SCRIPTS']['subscan_lin4.py'].run()
        for para_val_x in Range_x:
            line_last=readfreq(root['Cases'][case_tag][para_y+'~'+str(para_val_y)[0:effnum]+'~'+para_x+'~'+str(para_val_x)[0:effnum]]['fieldeigen.out'].filename)
            wr_temp[count]=line_last[0]
            wi_temp[count]=line_last[1]
            count=count+1
        # prepare for the next iteration
        root['SETTINGS']['PHYSICS']['wr_guess']=wr_temp
        root['SETTINGS']['PHYSICS']['wi_guess']=wi_temp
    #    root['SETTINGS']['PHYSICS']['Range'+str(nPara+1)]=wi_temp
    # Cha pi gu
    #del root['SETTINGS']['PHYSICS']['Para'+str(nPara)]
    #del root['SETTINGS']['PHYSICS']['Range'+str(nPara)]
    #del root['SETTINGS']['PHYSICS']['Para'+str(nPara+1)]
    #del root['SETTINGS']['PHYSICS']['Range'+str(nPara+1)]
    #del  root['SETTINGS']['SETUP']['iscan_3']
    root['SETTINGS']['PHYSICS']['wr_guess']=wr_guess_orig
    root['SETTINGS']['PHYSICS']['wi_guess']=wi_guess_orig
    root['SETTINGS']['PHYSICS']['Range']=para_rang_orig
else:
    root['SCRIPTS']['subscan_lin_2d.py'].run()
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

