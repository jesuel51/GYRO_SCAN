# this script is used to setup the best resolution family according to the comments by Jeff in 
# https://fusion.gat.com/theory/Gyrousermanual
# normally there are two types, linear initial value&nonlinear run and linear eigenvalue
# 1st type, linear initical value or nonlinear run
input_gyro=root['INPUTS']['input.gyro']
reso_para=root['SETTINGS']['SETUP']['reso_para'] # they are a set of m,n and p 
m=reso_para[0]
n=reso_para[1]
p=reso_para[2]

# radial resolution
# normally, n = 3 is enough
if not input_gyro.has_key('NONLINEAR_FLAG'):
    input_gyro['NONLINEAR_FLAG']=0
if not input_gyro.has_key('LINSOLVE_METHOD'):
    input_gyro['LINSOLVE_METHOD']=1
if input_gyro['NONLINEAR_FLAG']==1 or (input_gyro['NONLINEAR_FLAG']==0 and input_gyro['LINSOLVE_METHOD']==1):
    input_gyro['RADIAL_GRID'] = 2*m
    input_gyro['RADIAL_DERIVATIVE_BAND'] = m-1
    input_gyro['RADIAL_GYRO_BAND'] = m
    input_gyro['RADIAL_UPWIND'] = 1.0
else:
    input_gyro['RADIAL_GRID'] = 2*m
    input_gyro['RADIAL_DERIVATIVE_BAND'] = m
    input_gyro['RADIAL_GYRO_BAND'] = m
    input_gyro['RADIAL_UPWIND'] = 2.0

# poloidal resolution, normally n =4 is enough
input_gyro['ORBIT_GRID']=2*n
input_gyro['BLEND_GRID']=2*n
input_gyro['PASS_GRID']=n
input_gyro['TRAP_GRID']=n

# energy resolution, normally p =0 is enough
input_gyro['ENERGY_GRID']=8+p
input_gyro['ENERGY_MAX']=6+sqrt(p)
