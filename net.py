from fann2 import libfann as pyfann

connection_rate = .5
learning_rate = 0.7
num_input = 34
num_neurons_hidden_1 = 10
num_neurons_hidden_2 = 50
num_neurons_hidden_3 = 5
num_output = 1

desired_error = 0.0001
max_iterations = 100000
iterations_between_reports = 1000

training = pyfann.training_data()
training.read_train_from_file("/Users/jamesquadrino/git/svidur/data_train.data")


ann = pyfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input,num_neurons_hidden_1, num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_hidden(pyfann.SIGMOID_SYMMETRIC_STEPWISE)
ann.set_activation_function_output(pyfann.SIGMOID_SYMMETRIC_STEPWISE)
ann.set_training_algorithm(pyfann.TRAIN_INCREMENTAL)


ann.train_on_data(training, max_iterations, iterations_between_reports, desired_error)

ann.get_MSE()

ann.save("~/Users/jamesquadrino/testnet.config")
