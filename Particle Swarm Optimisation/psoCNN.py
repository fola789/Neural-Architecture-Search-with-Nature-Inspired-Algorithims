import keras
from keras.datasets import mnist
from keras.datasets import fashion_mnist
from keras.datasets import cifar10
import keras.backend

from population import Population

import numpy as np

from copy import deepcopy

class psoCNN:
    def __init__(self, dataset, n_iter, pop_size, batch_size, epochs, min_layer, max_layer, \
        conv_prob, pool_prob, fc_prob, max_conv_kernel, max_out_ch, max_fc_neurons, dropout_rate):
        
        self.pop_size = pop_size
        self.n_iter = n_iter
        self.epochs = epochs

        self.batch_size = batch_size
        self.gBest_acc = np.zeros(n_iter)
        self.gBest_test_acc = np.zeros(n_iter)

        if dataset == "mnist":
            input_width = 28
            input_height = 28
            input_channels = 1
            output_dim = 10

            (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()
        
        if dataset == "fashion-mnist":
            input_width = 28
            input_height = 28
            input_channels = 1
            output_dim = 10

            (self.x_train, self.y_train), (self.x_test, self.y_test) = fashion_mnist.load_data()

            self.x_train = self.x_train.astype('float32')
            self.x_test = self.x_test.astype('float32')
            self.x_train /= 255
            self.x_test /= 255

        if dataset == "cifar10":
            input_width = 32
            input_height = 32
            input_channels = 3
            output_dim = 10

            (self.x_train, self.y_train), (self.x_test, self.y_test) = cifar10.load_data()

        self.x_train = self.x_train.reshape(self.x_train.shape[0], self.x_train.shape[1], self.x_train.shape[2], input_channels)
        self.x_test = self.x_test.reshape(self.x_test.shape[0], self.x_test.shape[1], self.x_test.shape[2], input_channels)

        self.y_train = keras.utils.to_categorical(self.y_train, output_dim)
        self.y_test = keras.utils.to_categorical(self.y_test, output_dim)

        print("Initializing population...")
        self.population = Population(pop_size, min_layer, max_layer, input_width, input_height, input_channels, conv_prob, pool_prob, fc_prob, max_conv_kernel, max_out_ch, max_fc_neurons, output_dim)
        
        print("Verifying accuracy of the current gBest...")
        print(self.population.particle[0])
        self.gBest = deepcopy(self.population.particle[0])
        self.gBest.model_compile(dropout_rate)
        hist = self.gBest.model_fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs)
        test_metrics = self.gBest.model.evaluate(x=self.x_test, y=self.y_test, batch_size=batch_size)
        self.gBest.model_delete()
        
        self.gBest_acc[0] = hist.history['accuracy'][-1]
        self.gBest_test_acc[0] = test_metrics[1]
        
        self.population.particle[0].acc = hist.history['accuracy'][-1]
        self.population.particle[0].pBest.acc = hist.history['accuracy'][-1]

        print("Current gBest acc: " + str(self.gBest_acc[0]) + "\n")
        print("Current gBest test acc: " + str(self.gBest_test_acc[0]) + "\n")

        print("Looking for a new gBest in the population...")
        for i in range(1, self.pop_size):
            print('Initialization - Particle: ' + str(i+1))
            print(self.population.particle[i])

            self.population.particle[i].model_compile(dropout_rate)
            hist = self.population.particle[i].model_fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs)
            self.population.particle[i].model_delete()
           
            self.population.particle[i].acc = hist.history['accuracy'][-1]
            self.population.particle[i].pBest.acc = hist.history['accuracy'][-1]

            if self.population.particle[i].pBest.acc >= self.gBest_acc[0]:
                print("Found a new gBest.")
                self.gBest = deepcopy(self.population.particle[i])
                self.gBest_acc[0] = self.population.particle[i].pBest.acc
                print("New gBest acc: " + str(self.gBest_acc[0]))
                
                self.gBest.model_compile(dropout_rate)
                test_metrics = self.gBest.model.evaluate(x=self.x_test, y=self.y_test, batch_size=batch_size)
                self.gBest_test_acc[0] = test_metrics[1]
                print("New gBest test acc: " + str(self.gBest_acc[0]))
            
            self.gBest.model_delete()


    def fit(self, Cg, dropout_rate):
        for i in range(1, self.n_iter):            
            gBest_acc = self.gBest_acc[i-1]
            gBest_test_acc = self.gBest_test_acc[i-1]

            for j in range(self.pop_size):
                print('Iteration: ' + str(i) + ' - Particle: ' + str(j+1))

                # Update particle velocity
                self.population.particle[j].velocity(self.gBest.layers, Cg)

                # Update particle architecture
                self.population.particle[j].update()

                print('Particle NEW architecture: ')
                print(self.population.particle[j])

                # Compute the acc in the updated particle
                self.population.particle[j].model_compile(dropout_rate)
                hist = self.population.particle[j].model_fit(self.x_train, self.y_train, batch_size=self.batch_size, epochs=self.epochs)
                self.population.particle[j].model_delete()

                self.population.particle[j].acc = hist.history['accuracy'][-1]
                
                f_test = self.population.particle[j].acc
                pBest_acc = self.population.particle[j].pBest.acc

                if f_test >= pBest_acc:
                    print("Found a new pBest.")
                    print("Current acc: " + str(f_test))
                    print("Past pBest acc: " + str(pBest_acc))
                    pBest_acc = f_test
                    self.population.particle[j].pBest = deepcopy(self.population.particle[j])

                    if pBest_acc >= gBest_acc:
                        print("Found a new gBest.")
                        gBest_acc = pBest_acc
                        self.gBest = deepcopy(self.population.particle[j])
                        
                        self.gBest.model_compile(dropout_rate)
                        hist = self.gBest.model_fit(self.x_train, self.y_train, batch_size=self.batch_size, epochs=self.epochs)
                        test_metrics = self.gBest.model.evaluate(x=self.x_test, y=self.y_test, batch_size=self.batch_size)
                        self.gBest.model_delete()
                        gBest_test_acc = test_metrics[1]

                
            self.gBest_acc[i] = gBest_acc
            self.gBest_test_acc[i] = gBest_test_acc

            print("Current gBest acc: " + str(self.gBest_acc[i]))
            print("Current gBest test acc: " + str(self.gBest_test_acc[i]))

    def fit_gBest(self, batch_size, epochs, dropout_rate):
        print("\nFurther training gBest model...")
        self.gBest.model_compile(dropout_rate)

        trainable_count = 0
        for i in range(len(self.gBest.model.trainable_weights)):
            trainable_count += keras.backend.count_params(self.gBest.model.trainable_weights[i])
            
        print("gBest's number of trainable parameters: " + str(trainable_count))
        self.gBest.model_fit_complete(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs)

        return trainable_count
    
    def evaluate_gBest(self, batch_size):
        print("\nEvaluating gBest model on the test set...")
        
        metrics = self.gBest.model.evaluate(x=self.x_test, y=self.y_test, batch_size=batch_size)

        print("\ngBest model loss in the test set: " + str(metrics[0]) + " - Test set accuracy: " + str(metrics[1]))
        return metrics
