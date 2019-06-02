# this script is used to get the dimensional parameter which will be stored in root['STTINGS']['DEPENDENCIES']
# the parameters are : n_time, n_field, n_spec, n_kinetic, n_x, n_theta_plot, n_n, n_energy, n_pass, n_trap
# please refer to https://fusion.gat.com/theory/Gyrooutput#out.gyro.gbflux for more detailes about the meaning of the parameters
# first let's get the n_time from out.gyro.t
outt=root['OUTPUTS']['out.gyro.t']
f_t=open(root['OUTPUTS']['out.gyro.t'].filename,'Ur')
data_t=f_t.readlines()
n_time=len(data_t)
time_max=float(data_t[-1].split()[-1])
# then get the others from out.gyro.profile
f_profile=open(root['OUTPUTS']['out.gyro.profile'].filename,'Ur')
data_profile=f_profile.readlines()
##
n_field       = int(data_profile[13-1])
n_spec        = int(data_profile[16-1])
n_kinetic     = int(data_profile[15-1])
n_x           = int(data_profile[1-1])
n_theta_plot  = int(data_profile[6-1])
n_n           = int(data_profile[8-1])
n_energy      = int(data_profile[5-1])
n_pass        = int(data_profile[3-1])
n_trap        = int(data_profile[4-1])
# store the dim_data
depend=root['SETTINGS']['DEPENDENCIES']
depend['dim']=OMFITnamelist('')
dim_data={'n_time':n_time,\
          'n_field':n_field,\
          'n_spec':n_spec,\
          'n_kinetic':n_kinetic,\
          'n_x':n_x,\
          'n_theta_plot':n_theta_plot,\
          'n_n':n_n,\
          'n_energy':n_energy,\
          'n_pass':n_pass,\
          'n_trap':n_trap,\
          'time_max': time_max\
}
for item in dim_data.keys():
    depend['dim'][item]=dim_data[item]
# in addition, the rho_s should also be read fro out.gyro.run and put into the input.gyro
f_run=open(root['OUTPUTS']['out.gyro.run'].filename,'Ur')
for line in f_run:
    if line.find('RHO_STAR')!=-1:
        print(line)
        rho_s=float(line.split()[-1])
root['INPUTS']['input.gyro']['RHO_STAR']=rho_s
