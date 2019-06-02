##===================================
### input
##==================================
input_gyro=root['INPUTS']['input.gyro']
inputs=[input_gyro,'input.gyro']
if root['SETTINGS']['PHYSICS']['mode']=='nonlin':
    input_gyro['NONLINEAR_FLAG'] = 1
else:
    input_gyro['NONLINEAR_FLAG'] = 0
# to plot the ballooning mode
input_gyro['PLOT_U_FLAG']=1
if input_gyro['THETA_PLOT']==1 or not input_gyro.has_key('THETA_PLOT'):
    input_gyro['THETA_PLOT']=24
##----------------------
### output
##----------------------
if not input_gyro.has_key('LINSOLVE_METHOD'):
    input_gyro['LINSOLVE_METHOD']=1
if root['INPUTS']['input.gyro']['NONLINEAR_FLAG']==0:
    if input_gyro['LINSOLVE_METHOD']==1:
        outputs=['out.gyro.freq','out.gyro.balloon_phi','out.gyro.balloon_a','out.gyro.balloon_epar','out.gyro.balloon_b','out.gyro.run']
    else:
        outputs=['fieldeigen.out','out.gyro.balloon_phi','out.gyro.balloon_a','out.gyro.balloon_epar','out.gyro.balloon_b','out.gyro.run']
else:
    outputs = [ 'out.gyro.profile' , \
                'out.gyro.gbflux' , 'out.gyro.gbflux_i' , 'out.gyro.gbflux_mom' , 'out.gyro.gbflux_n' , \
                'out.gyro.k_perp_squared' , 'out.gyro.kxkyspec' , \
                'out.gyro.moment_zero','out.gyro.moment_u' \
               ]
executable=root['SETTINGS']['SETUP']['executable']
ncore=int(executable.split()[-1])  # cores needed
jn=int(ceil(ncore/24.))              # get the number of nodes
if ncore<24:
    cn=ncore
else:
    cn=24
preexecutable ='mv out.gyro.localdump input.gyro; '
executable =preexecutable + 'pbsMonitor -jn '+str(jn)+' -cn '+str(cn)+' -exe  '+executable
ret_code=OMFITx.executable(root, inputs=inputs, outputs=outputs, executable=executable)
#-----------------------
# load the results
#-----------------------
for item in outputs:
    root['OUTPUTS'][item]=OMFITasciitable(item)
