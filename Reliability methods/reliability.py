import pandas as pd 
import numpy as np 
import os
class ReliabilityLLM():
	def __init__(self,filename,class_label,Nf,flabels,results_file,method,case, *pos_class):
			# filename: file with input data
			# Nf: number of features to be used (by now, only works with Nf=2)
			# self.class_label: name of output class
			# flabels: labels of the features to be considered
			# results_file (csv): output file with error, coverage, TP, TN, FP, FN for all the perturbation values (deltas)
			# method of the optimization algorithm: 'outside' or 'inside'
			# self.case ({1,2,3,4}): format of the intervals to be perturbed; 1 if f1>=th1, f2<=th2; 2 if f1<=th1,f2>=th2; 3 if f1>=th1, f2>=th2; 4 if f1<=th1, f2<=th2 
			# optional argument (*pos_class): if output variables are categorial, insert the label for the positive class
			self.filename=filename
			self.Nf=Nf
			self.class_label=class_label
			self.flabels=flabels
			self.results_file=results_file
			self.method=method
			self.case=case
			if (pos_class==None):
				self.pos_class=None
			else:
				self.pos_class=pos_class

	def load_data(self, filename, class_label):
				
				if filename[-4:]=='.csv':
					data=pd.read_csv(filename)
					#print(data)
					y_data=data[self.class_label]
					#data.drop([self.class_label], axis=1,inplace=True)
				else:
					if filename[-5:]=='.xlsx':
						data=pd.read_excel(filename)
						y_data=data[self.class_label]
						#data.drop([self.class_label], axis=1,inplace=True)
					else:
						if filename[-4:]=='.txt':
							data=pd.read_csv(filename,delimiter="\t")
							#print(data)
							y_data=data[self.class_label]
							#data.drop([self.class_label], axis=1,inplace=True)
				#print(y_data)
				# if ouput values are not in {0,1} (e.g. categorical), convert it			
				if self.pos_class!=None:
					#print(self.pos_class)
					y_data=y_data.replace(self.pos_class,1)
					y_data=y_data.where(y_data==1,0)
					#y_data[self.class_label]=self.pos_class]=le.transform(y_data)
				#print(y_data)
				return (data,y_data)

	def get_unsafe_points(self):
		data,y_data=self.load_data(self.filename, self.class_label)
		#unsafe_pts=[]
		#for i in range(self.Nf):
		#	unsafe_pts.append(list(data[self.flabels[i]].where(data[self.class_label]==1).dropna(axis=0)))
		#f1_data=list(data[self.flabels[0]].where(data[self.class_label]==1).dropna(axis=0))
		#f2_data=list(data[self.flabels[1]].where(data[self.class_label]==1).dropna(axis=0))
		f1_data=list(pd.unique(data[self.flabels[0]].where(data[self.class_label]==1).dropna(axis=0)))
		f2_data=list(pd.unique(data[self.flabels[1]].where(data[self.class_label]==1).dropna(axis=0)))
		# possibile variazione, per trovare regioni di soli veri positivi
		#f1_data=list(pd.unique(data[self.flabels[0]].where(data[self.class_label]==0).dropna(axis=0)))
		#f2_data=list(pd.unique(data[self.flabels[1]].where(data[self.class_label]==0).dropna(axis=0)))
		return f1_data, f2_data

	def get_predictions(self):
		data,y_data=self.load_data(self.filename, self.class_label)
		f1_data,f2_data=self.get_unsafe_points()
		f1=self.flabels[0]
		f2=self.flabels[1]
		if os.path.isfile(self.results_file):
			os.remove(self.results_file)
		with open(self.results_file,'a') as output:
			output.write("th1_new"+","+"th2_new"+","+"FNR"+","+"TNR"+","+"TP, FP, TN, FN"+"\n")
		for th1 in f1_data:
			for th2 in f2_data:
				predicted=0
				TP=0
				FP=0
				TN=0
				FN=0
				if self.method=='outside':
					if self.case==1:
						for i in range(0,len(data)):
							if (data[f1][i]>=th1  or data[f2][i]<=th2):
								predicted=1
							else:
								predicted=0
							if (predicted==1 and data[self.class_label][i]==1):
							    TP+=1
							else: 
							    if (predicted==1 and data[self.class_label][i]==0):
							        FP+=1
							    else: 
							        if (predicted==0 and data[self.class_label][i]==0):
							            TN+=1
							        else:
							            if (predicted==0 and data[self.class_label][i]==1):
							                FN+=1
					else:
						if self.case==2:
							for i in range(0,len(data)):
								if (data[f1][i]<=th1  or data[f2][i]>=th2):
									predicted=1
								else:
									predicted=0
								if (predicted==1 and data[self.class_label][i]==1):
								    TP+=1
								else: 
								    if (predicted==1 and data[self.class_label][i]==0):
								        FP+=1
								    else: 
								        if (predicted==0 and data[self.class_label][i]==0):
								            TN+=1
								        else:
								            if (predicted==0 and data[self.class_label][i]==1):
								                FN+=1
							
						else:
							if self.case==3:
								for i in range(0,len(data)):
									if (data[f1][i]>=th1  or data[f2][i]>=th2):
										predicted=1
									else:
										predicted=0
									if (predicted==1 and data[self.class_label][i]==1):
									    TP+=1
									else: 
									    if (predicted==1 and data[self.class_label][i]==0):
									        FP+=1
									    else: 
									        if (predicted==0 and data[self.class_label][i]==0):
									            TN+=1
									        else:
									            if (predicted==0 and data[self.class_label][i]==1):
									                FN+=1
							else:
								if self.case==4:
									for i in range(0,len(data)):
										if (data[f1][i]<=th1  or data[f2][i]<=th2):
											predicted=1
										else:
											predicted=0
										if (predicted==1 and data[self.class_label][i]==1):
										    TP+=1
										else: 
										    if (predicted==1 and data[self.class_label][i]==0):
										        FP+=1
										    else: 
										        if (predicted==0 and data[self.class_label][i]==0):
										            TN+=1
										        else:
										            if (predicted==0 and data[self.class_label][i]==1):
										                FN+=1
									
				else:
						if self.method=='inside':
							if self.case==1:
								for i in range(0,len(data)):
									if (data[f1][i]>th1  or data[f2][i]<th2):
										predicted=0
									else:
										predicted=1
									
									if (predicted==1 and data[self.class_label][i]==1):
									    TP+=1
									else: 
									    if (predicted==1 and data[self.class_label][i]==0):
									        FP+=1
									    else: 
									        if (predicted==0 and data[self.class_label][i]==0):
									            TN+=1
									        else:
									            if (predicted==0 and data[self.class_label][i]==1):
									                FN+=1
							else:
								if self.case==2:
									for i in range(0,len(data)):
										if (data[f1][i]<th1  or data[f2][i]>th2):
											predicted=0
										else:
											predicted=1
										if (predicted==1 and data[self.class_label][i]==1):
										    TP+=1
										else: 
										    if (predicted==1 and data[self.class_label][i]==0):
										        FP+=1
										    else: 
										        if (predicted==0 and data[self.class_label][i]==0):
										            TN+=1
										        else:
										            if (predicted==0 and data[self.class_label][i]==1):
										                FN+=1
									
								else:
									if self.case==3:
										for i in range(0,len(data)):
											if (data[f1][i]>th1  or data[f2][i]>th2):
												predicted=0
											else:
												predicted=1
											if (predicted==1 and data[self.class_label][i]==1):
											    TP+=1
											else: 
											    if (predicted==1 and data[self.class_label][i]==0):
											        FP+=1
											    else: 
											        if (predicted==0 and data[self.class_label][i]==0):
											            TN+=1
											        else:
											            if (predicted==0 and data[self.class_label][i]==1):
											                FN+=1

									else:
										if self.case==4:
											for i in range(0,len(data)):
												if (data[f1][i]<th1  or data[f2][i]<th2):
													predicted=0
												else:
													predicted=1
												if (predicted==1 and data[self.class_label][i]==1):
												    TP+=1
												else: 
												    if (predicted==1 and data[self.class_label][i]==0):
												        FP+=1
												    else: 
												        if (predicted==0 and data[self.class_label][i]==0):
												            TN+=1
												        else:
												            if (predicted==0 and data[self.class_label][i]==1):
												                FN+=1

											
				error=FN/(FN+TP) # false negative rate
				coverage=TN/(TN+FP)#true negative rate
				with open(self.results_file,'a') as output:
					output.write(str(th1)+","+str(th2)+","+str(error)+","+str(coverage)+","+str(TP)+','+str(FP)+','+str(TN)+','+str(FN)+'\n')

	# get the optimal perturbations (maximum TNR for minimum Error (hopefully 0))
	def get_safety_regions(self):
		self.get_predictions()
		output=pd.read_csv(self.results_file)
		minErr=min(output['FNR'])
		outErrmin=output.loc[output['FNR']==minErr]
		maxCov=max(outErrmin['TNR'])
		outMaxCov=outErrmin.loc[outErrmin['TNR']==maxCov]
		if self.method=='outside':
			print("Getting optimal results for {} -- outside method".format(self.filename))
			optth1_new=min(outMaxCov['th1_new'])
			optth2_new=min(outMaxCov['th2_new'])
			optimalResults=outMaxCov.loc[(outMaxCov['th1_new']==optth1_new) & (outMaxCov['th2_new']==optth2_new)]
		else:
			if self.method=='inside':
				print("Getting optimal results for {} -- inside method".format(self.filename))
				optth1_new=max(outMaxCov['th1_new'])
				optth2_new=max(outMaxCov['th2_new'])
				optimalResults=outMaxCov.loc[(outMaxCov['th1_new']==optth1_new) & (outMaxCov['th2_new']==optth2_new)]
		return optimalResults

	def evaluate_safety_regions(self, test_file, th1,th2):
		data,y_data=self.load_data(test_file, self.class_label)
		predicted=0
		TP=0
		FP=0
		TN=0
		FN=0
		f1=self.flabels[0]
		f2=self.flabels[1]
		if self.method=='outside':
			if self.case==1:
				for i in range(0,len(data)):
					if (data[f1][i]>=th1  or data[f2][i]<=th2):
						predicted=1
					else:
						predicted=0
					if (predicted==1 and data[self.class_label][i]==1):
					    TP+=1
					else: 
					    if (predicted==1 and data[self.class_label][i]==0):
					        FP+=1
					    else: 
					        if (predicted==0 and data[self.class_label][i]==0):
					            TN+=1
					        else:
					            if (predicted==0 and data[self.class_label][i]==1):
					                FN+=1
			else:
				if self.case==2:
					for i in range(0,len(data)):
						if (data[f1][i]<=th1  or data[f2][i]>=th2):
							predicted=1
						else:
							predicted=0
						if (predicted==1 and data[self.class_label][i]==1):
						    TP+=1
						else: 
						    if (predicted==1 and data[self.class_label][i]==0):
						        FP+=1
						    else: 
						        if (predicted==0 and data[self.class_label][i]==0):
						            TN+=1
						        else:
						            if (predicted==0 and data[self.class_label][i]==1):
						                FN+=1
					
				else:
					if self.case==3:
						for i in range(0,len(data)):
							if (data[f1][i]>=th1  or data[f2][i]>=th2):
								predicted=1
							else:
								predicted=0
							if (predicted==1 and data[self.class_label][i]==1):
							    TP+=1
							else: 
							    if (predicted==1 and data[self.class_label][i]==0):
							        FP+=1
							    else: 
							        if (predicted==0 and data[self.class_label][i]==0):
							            TN+=1
							        else:
							            if (predicted==0 and data[self.class_label][i]==1):
							                FN+=1
					else:
						if self.case==4:
							for i in range(0,len(data)):
								if (data[f1][i]<=th1  or data[f2][i]<=th2):
									predicted=1
								else:
									predicted=0
								if (predicted==1 and data[self.class_label][i]==1):
								    TP+=1
								else: 
								    if (predicted==1 and data[self.class_label][i]==0):
								        FP+=1
								    else: 
								        if (predicted==0 and data[self.class_label][i]==0):
								            TN+=1
								        else:
								            if (predicted==0 and data[self.class_label][i]==1):
								                FN+=1
							
		else:
				if self.method=='inside':
					if self.case==1:
						for i in range(0,len(data)):
							if (data[f1][i]>th1  or data[f2][i]<th2):
								predicted=0
							else:
								predicted=1
							
							if (predicted==1 and data[self.class_label][i]==1):
							    TP+=1
							else: 
							    if (predicted==1 and data[self.class_label][i]==0):
							        FP+=1
							    else: 
							        if (predicted==0 and data[self.class_label][i]==0):
							            TN+=1
							        else:
							            if (predicted==0 and data[self.class_label][i]==1):
							                FN+=1
					else:
						if self.case==2:
							for i in range(0,len(data)):
								if (data[f1][i]<th1  or data[f2][i]>th2):
									predicted=0
								else:
									predicted=1
								if (predicted==1 and data[self.class_label][i]==1):
								    TP+=1
								else: 
								    if (predicted==1 and data[self.class_label][i]==0):
								        FP+=1
								    else: 
								        if (predicted==0 and data[self.class_label][i]==0):
								            TN+=1
								        else:
								            if (predicted==0 and data[self.class_label][i]==1):
								                FN+=1
							
						else:
							if self.case==3:
								for i in range(0,len(data)):
									if (data[f1][i]>th1  or data[f2][i]>th2):
										predicted=0
									else:
										predicted=1
									if (predicted==1 and data[self.class_label][i]==1):
									    TP+=1
									else: 
									    if (predicted==1 and data[self.class_label][i]==0):
									        FP+=1
									    else: 
									        if (predicted==0 and data[self.class_label][i]==0):
									            TN+=1
									        else:
									            if (predicted==0 and data[self.class_label][i]==1):
									                FN+=1

							else:
								if self.case==4:
									for i in range(0,len(data)):
										if (data[f1][i]<th1  or data[f2][i]<th2):
											predicted=0
										else:
											predicted=1
										if (predicted==1 and data[self.class_label][i]==1):
										    TP+=1
										else: 
										    if (predicted==1 and data[self.class_label][i]==0):
										        FP+=1
										    else: 
										        if (predicted==0 and data[self.class_label][i]==0):
										            TN+=1
										        else:
										            if (predicted==0 and data[self.class_label][i]==1):
										                FN+=1

									
		error=FN/(FN+TP) # false negative rate
		coverage=TN/(TN+FP)
		print("Evaluating the safety region obtained from {} on {}, with method {}".format(self.filename, test_file, self.method))
		eval_results=pd.DataFrame(data=[[th1,th2, error, coverage,TP, FP, TN, FN]], columns=['th1_new','th2_new','FNR','TNR','TP','FP','TN','FN'])
		return eval_results		

