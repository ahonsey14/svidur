from fann2 import libfann as pyfann

connection_rate = .5
learning_rate = 0.5

desired_error = 0.00000001
max_iterations = 3500
iterations_between_reports = 50


training = pyfann.training_data()
training.read_train_from_file("/home/ubuntu/svidur/data_train.data")

num_input = len(training.get_input()[0])
num_neurons_hidden_1 = 24
num_neurons_hidden_2 = 7
num_output = len(training.get_output()[0])

ann = pyfann.neural_net()
#ann.create_sparse_array(connection_rate, (num_input,num_neurons_hidden_1,num_neurons_hidden_2, num_output))

ann.create_standard_array((num_input,num_neurons_hidden_1,num_neurons_hidden_2,num_output))
ann.set_activation_function_hidden(pyfann.ELLIOT_SYMMETRIC)
ann.set_activation_function_output(pyfann.ELLIOT_SYMMETRIC)
ann.set_training_algorithm(pyfann.TRAIN_BATCH)
ann.set_train_error_function(pyfann.ERRORFUNC_LINEAR)

ann.train_on_data(training, max_iterations, iterations_between_reports, desired_error)

print "Testing network"
test_data = pyfann.training_data()
test_data.read_train_from_file("/home/ubuntu/svidur/data_test.data")

ann.reset_MSE()
ann.test_data(test_data)
print "MSE error on test data: %f" % ann.get_MSE()

print "Testing network again"
ann.reset_MSE()
input=test_data.get_input()
output=test_data.get_output()
for i in range(len(input)):
    ann.test(input[i], output[i])
print "MSE error on test data: %f" % ann.get_MSE()

ann.save("/home/ubuntu/svidur/netattempt.net")
