from reliability import *
import reliability as OptLLM

# folder with the dataset to be used
dataFolder="Used Datasets/"

# define the inputs needed in reliability methods
# uncomment the desired block

'''
# UNDER 40 REAL OUTSIDE
# training set filename
filename=dataFolder+"under40_real_training.xlsx"
# name of the target 
class_label='fatiguestate1'
# number of features to be used in safety regions (by now, only 2)
Nf=2 # number of features
# names of the Nf most important features 
flabels=['back rotation position in sag plane','leg rotational velocity sag plane']
# file with logs of results for all the candidate modified thresholds tried during the execution
results_file="under40_real_outside.csv"
# indicate the method for the safety region design ('outside' or 'inside')
method='outside'
# test set filename (for the evaluation phase)
filename_test=dataFolder+"under40_real_test.xlsx"
# case is a parameter used to track the kind of safety region (v. readme)
case=1 
'''
'''
# UNDER 40 REAL INSIDE
filename=dataFolder+"under40_real_training.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['back rotation position in sag plane','leg rotational velocity sag plane']
results_file="results_file=under40_real_inside.csv"
method='inside'
filename_test=dataFolder+"under40_real_test.xlsx"
case=2
'''
'''
# OVER 40 REAL OUTSIDE
filename=dataFolder+"over40_real_training.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Hip.ACC.Mean','Hip.yposture.Mean']
results_file="over40_real_outside.csv"
method='outside'
filename_test=dataFolder+"over40_real_test.xlsx"
case=2
'''
'''
# OVER 40 REAL INSIDE
filename=dataFolder+"over40_real_training.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['back rotation position in sag plane','leg rotational velocity sag plane']
results_file="results_file=over40_real_inside.csv"
method='inside'
filename_test=dataFolder+"over40_real_test.xlsx"
case=1
'''

'''
# UNDER 40 FAKE+REAL OUTSIDE nearest
filename=dataFolder+"under40_nearest_train.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Wrist.jerk.coefficient.of.variation','Chest.zposture.Mean']
results_file="under40_nearest_outside.csv"
method='outside'
filename_test=dataFolder+"under40_nearest_test.xlsx"
case=1
'''
'''
# UNDER 40 FAKE+REAL INSIDE nearest
filename=dataFolder+"under40_nearest_train.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Chest.zposture.Mean', 'mean foot osicllation']
results_file="under40_nearest_inside.csv"
method='inside'
filename_test=dataFolder+"under40_nearest_test.xlsx"
case=1
'''

'''
# UNDER 40 FAKE+REAL OUTSIDE farthest
filename=dataFolder+"under40_farthest_train.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Ankle.jerk.coefficient.of.variation','Chest.zposture.Mean']
results_file="under40_lontano_outside.csv"
method='outside'
filename_test=dataFolder+"under40_farthest_test.xlsx"
case=1
'''
'''
# UNDER 40 FAKE+REAL INSIDE farthest
filename=dataFolder+"under40_farthest_train.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Ankle.jerk.coefficient.of.variation','Chest.jerk.coefficient.of.variation']
results_file="under40_lontano_inside.csv"
method='inside'
filename_test=dataFolder+"under40_farthest_test.xlsx"
case=4
'''

# OVER 40 FAKE+REAL OUTSIDE nearest
'''
filename=dataFolder+"over40_nearest_train.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Wrist.jerk.Mean','Hip.yposture.Mean']
results_file="over40_nearest_outside.csv"
method='outside'
filename_test=dataFolder+"over40_nearest_test.xlsx"
case=2
'''
'''
# OVER 40 FAKE+REAL INSIDE nearest
filename=dataFolder+"over40_nearest_train.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Wrist.jerk.Mean','Hip.yposture.Mean']
results_file="over40_nearest_inside.csv"
method='inside'
filename_test=dataFolder+"over40_nearest_test.xlsx"
case=1
'''


'''
# OVER 40 FAKE+REAL OUTSIDE farthest

filename=dataFolder+"over40_farthest_training.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['Ankle.yposture.coefficient.of.variation','average step distance']
results_file="over40_fakereal_outside.csv"
method='outside'
filename_test=dataFolder+"over40_farthest_test.xlsx"
case=2
'''
'''
# OVER 40 FAKE+REAL INSIDE farthest
filename=dataFolder+"over40_farthest_training.xlsx"
class_label='fatiguestate1'
Nf=2 # N.B. per ora non funziona con più di 2
flabels=['average step distance','Ankle.yposture.coefficient.of.variation']
results_file="over40_fakereal_inside.csv"
method='inside'
filename_test=dataFolder+"over40_farthest_test.xlsx"
case=2
'''

# main

if __name__ == '__main__':
	# create the object for LLM reliability
	safetyReg=OptLLM.ReliabilityLLM(filename,class_label,Nf,flabels,results_file,method,case)
	# get the safety region
	output=safetyReg.get_safety_regions()
	#output.to_excel('optres.xlsx')
	# result of training phase; print the new thresholds for the individuated region and the obtained performance metrics 
	print(output)
	# evaluate the safety region on the test set
	evaluated=safetyReg.evaluate_safety_regions(filename_test,float(output['th1_new']),float(output['th2_new']))
	# print results
	print(evaluated)