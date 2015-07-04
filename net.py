from fann2 import libfann as pyfann

connection_rate = .3
learning_rate = 0.7
num_input = 34
num_neurons_hidden_1 = 24
num_neurons_hidden_2 = 15
num_output = 1

desired_error = 0.00000001
max_iterations = 1
iterations_between_reports = 10


training = pyfann.training_data()
training.read_train_from_file("/home/ubuntu/svidur/data_train.data")


ann = pyfann.neural_net()
#ann.create_sparse_array(connection_rate, (num_input,num_neurons_hidden_1,num_neurons_hidden_2, num_output))

ann.create_standard_array((num_input,num_neurons_hidden_1,num_neurons_hidden_2,num_output))
ann.set_activation_function_hidden(pyfann.SIGMOID_SYMMETRIC_STEPWISE)
ann.set_activation_function_output(pyfann.SIGMOID_SYMMETRIC_STEPWISE)
ann.set_training_algorithm(pyfann.TRAIN_BATCH)

ann.train_on_data(training, max_iterations, iterations_between_reports, desired_error)

ann.get_MSE()

ann.save("/home/ubuntu/testnet.config")
