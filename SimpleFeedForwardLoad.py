import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("../MNIST_data/", one_hot=True)

learning_rate = 0.5
training_epochs = 1000
batch_size = 64

number_of_input = 784
number_of_output = 10

layer_1_size = 128
layer_2_size = 64

is_train = False

with tf.variable_scope("input"):
    X = tf.placeholder(tf.float32, shape=[None, number_of_input])

with tf.variable_scope("layer1"):
    weights = tf.get_variable(name="weights1", shape=[number_of_input, layer_1_size],
                              initializer=tf.contrib.layers.xavier_initializer())

    biases = tf.get_variable(name="biases1", shape=[layer_1_size], initializer=tf.zeros_initializer())
    layer_1_output = tf.nn.relu(tf.matmul(X, weights) + biases)

with tf.variable_scope("layer2"):
    weights = tf.get_variable(name="weights2", shape=[layer_1_size, layer_2_size],
                              initializer=tf.contrib.layers.xavier_initializer())

    biases = tf.get_variable(name="biases2", shape=[layer_2_size], initializer=tf.zeros_initializer())
    layer_2_output = tf.nn.relu(tf.matmul(layer_1_output, weights) + biases)

with tf.variable_scope("output"):
    weights = tf.get_variable(name="weightsOut", shape=[layer_2_size, number_of_output],
                              initializer=tf.contrib.layers.xavier_initializer())

    biases = tf.get_variable(name="biasesOut", shape=[number_of_output], initializer=tf.zeros_initializer())
    output = tf.nn.softmax(tf.matmul(layer_2_output, weights) + biases)

with tf.variable_scope("cost"):
    Y = tf.placeholder(tf.float32, shape=[None, number_of_output])
    cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(output), reduction_indices=[1]))

with tf.variable_scope("accuracy"):
    correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


saver = tf.train.Saver()
with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    saver.restore(session, "../saveFeedForward/trained_model.ckpt")
    final_accuracy = session.run(accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels})
    print("Fianl Accuracy: ", final_accuracy)

