def read_model_choice(fname):
	choices = {}
	fd = open(fname)
	for line in fd:
		line = line.strip().split('\t')
		id = int(line[0])
		choice = line[len(line)-1]
		choices[id] = choice
	fd.close()
	return choices

def read_pav_parameters(fname):	
	tmp_parameters = []
	fd = open(fname)	
	for line in fd:
		line = line.strip().split('\t')
		line = [float(l) for l in line]
		tmp_parameters.append((line[0], line[2]))		
	fd.close()
	#refinement
	parameters = []
	l = len(tmp_parameters)
	for i in range(1, l):
		parameters.append((tmp_parameters[i][0], tmp_parameters[i-1][1]))	
	return (parameters, tmp_parameters[l-1][1])

def read_pav_parameters_by_ids(ids, folder, postfix):
	all_paras = {}
	for id in ids:	
		all_paras[id] = read_pav_parameters(folder + '/' + str(id) + postfix)
	return all_paras			
	
def commpute_pav_probability(parameters, score):
	for p in parameters[0]:
		if score <= p[0]:
			return p[1]
	return parameters[1]
					
if __name__ == '__main__': 		
	choices = read_model_choice('/home/xiao/SEE_Probability_Estimation/best_parameter.txt')
	paras = read_pav_parameters('/home/xiao/SEE_Probability_Estimation/pav_model/1SEE_0.2_pav_model')
	print commpute_pav_probability(paras, 4.738)
	all_paras = read_pav_parameters_by_ids([0, 10, 100, 200, 661], '/home/xiao/SEE_Probability_Estimation/pav_model', 'SEE_0.2_pav_model')
