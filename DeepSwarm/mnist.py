import os
import sys
import tensorflow as tf

from deepswarm.backends import Dataset, TFKerasBackend
from deepswarm.deepswarm import DeepSwarm

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Load MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# Normalize and reshape data
x_train, x_test = x_train / 255.0, x_test / 255.0
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
# Create dataset object, which controls all the data
normalized_dataset = Dataset(
    training_examples=x_train,
    training_labels=y_train,
    testing_examples=x_test,
    testing_labels=y_test,
    validation_split=0.1,
)
# Create backend responsible for training & validating
backend = TFKerasBackend(dataset=normalized_dataset)
# Create DeepSwarm object responsible for optimization
deepswarm = DeepSwarm(backend=backend)
# Find the topology for a given dataset
topology = deepswarm.find_topology()
# Evaluate discovered topology
deepswarm.evaluate_topology(topology)
# Train topology for additional 30 epochs
trained_topology = deepswarm.train_topology(topology, 30)
# Evaluate the final topology
deepswarm.evaluate_topology(trained_topology)