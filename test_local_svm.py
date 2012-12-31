from liblinearutil import *
# Read data in LIBSVM format
y, x = svm_read_problem('../heart_scale')
m = train(y[:100], x[:100], '-s 0')
save_model('heart_scale.model_1', m)
m = train(y[100:200], x[100:200], '-s 0')
save_model('heart_scale.model_2', m)
m = train(y[200:], x[200:], '-s 0')
save_model('heart_scale.model_3', m)

#m = load_model('heart_scale.model')
#p_label, p_acc, p_val = predict(y[:10], x[:10], m, '-b 1')
#print p_val
