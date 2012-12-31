from liblinear import *
xi, idx = gen_feature_nodearray(features, feature_max=my_models[157].nr_feature)
biasterm = feature_node(-1, my_models[157].bias)
xi[-2] = biasterm
pred_labels = []
pred_values = [] 
dec_values = (c_double * 1)()
label = liblinear.predict_values(my_models[157], xi, dec_values)
values = dec_values[:1]			
pred_labels += [label]
pred_values += [values]
