# Neural Architecture Search with Nature Inspired Algorithims
This work explores the efficacy of automating neural architecture search by implementing four nature-inspired algorithms 3 of which are bio-inspired 
and the other physics-inspired and analysing the computational speed, accuracy, scalability, and other restricting issues around them


## Dataset
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/MNIST-Fashion-MNIST-and-CIFAR-10-training-samples.png)

### Mnist

* MNIST set is a large collection of handwritten digits.
* MNIST is short for Modified National Institute of Standards and Technology database
* MNIST contains a collection of 70,000, 28 x 28 greyscale images of handwritten digits from 0 to 9.
* The dataset is already divided into training and testing sets.
  * Training set of 60,000 examples 
  * Test set of 10,000 examples

### Fashion-Mnist

* Fashion-MNIST is a dataset of Zalando's article images.
* Fashion-MNIST contains a collection of 70,000, 28 x 28 greyscale images,  associated with a label from 10 classes.
* Each pixel has a single pixel-value associated with it, indicating the lightness or darkness of that pixel, with higher numbers meaning darker. 
* Each pixel-value is an integer between 0 and 255.
* The 10 categories include the following, 0 T-shirt/top, 1 Trouser, 2 Pullover, 3 Dress, 4 Coat, 5 Sandal, 6 Shirt, 7 Sneaker, 8 Bag, 9 Ankle boot


### CIFAR10

*  It is a subset of the 80 million tiny images dataset
*  CIFAR is short for Canadian Institute For Advanced Research 
*  Consisting of 60,000 32x32 color images in 10  different classes, with 6000 images per class.
*  The 10 different classes represent airplanes, cars, birds, cats, deer, dogs, frogs, horses, ships, and trucks.

## Project Architecture
The project features 4 key components, in which 4 different algorithims are implemented as search strategies to operate within their givben search space to to find the best neural network architecture.  

Where prior research has deemed that strategies for NAS could be classified and divided accordingly into three dimensions: search space, search strategy, and performance estimation/prediction strategy
### Genetic Algorithims
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/geneticAlgorithimModel.png)
<br/>
Each model is represented as fixed-width genome encoding information about the network's structure. a model contains a number of convolutional layers, a number of dense layers, and an optimizer. The convolutional layers can be evolved to include varying numbers of feature maps, different activation functions, varying proportions of dropout, and whether to perform batch normalization and/or max pooling. The same options are available for the dense layers with the exception of max pooling. <br/>

![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/geneticAlgorithim2.png)

### DeepSwarm
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/deepswarmModel.png)
(1) The ant is placed on the input node. (2) The ant checks what transitions are available. (3) The ant uses the ACS selection rule to choose the next node. (4) After choosing the next node the ant selects node’s attributes. (5) After all ants finished their tour the pheromone is updated. (6) The maximum allowed depth is increased and the new ant population is generated.<br/>

![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/deepswarm2.png)<br/>

**Note**: Arrow thickness indicates the pheromone amount, meaning that thicker arrows have more pheromone.


### Particle Swarm

The global best particle is based on the best blocks found in the swarm by following the PSO algorithm
The algorithm takes as input the training data and parameters related to the CNN architectures, such as the maximum number of layers. It consists of six procedures: CNN representation, swarm initialization, fitness evaluation of particles, velocity computation, particle update, and measuring the difference between two particles.<br/>
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/pso1.png)

Algorithm 2 describes

![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/pso2.png)
nitialization of the swarm. This function creates N particles with random CNN architectures, where each particle has a random number of layers between three and lmax, with the first and last layer always being a convolution and a fully-connected layer, respectively. Fully-connected layers can only be placed at the end of the architecture, and the algorithm ensures that once a fully-connected layer is added, every subsequent layer is also a fully-connected layer. The addConv(), addPool(), and addFC() functions add convolutional, pooling, and fully-connected layers to the particle architecture with randomly chosen hyperparameters. The activation function of all layers is always ReLU, and the number of pooling layers is constrained by the size of the input data. <br/>

![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/pso3.png)

### Simulated Annealing
The idea behind the  algorithm is that local minima can be solved by accepting worse solutions with some probability, in addition to subsampling the local region for better solutions.

A candidate move is randomly selected; this move is accepted if it leads to a solution with a better objective function value than the current solution, otherwise the move is accepted with a probability that depends on the deterioration ∆ of the objective function value. The probability of acceptance is computed as e−∆/T , using  a temperature T as control parameter.  <br/>

![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/simulatedAnnealing2.png)

## Results
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/geneticaAlgorithmResult.png)
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/deepswarmResults.png)
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/psoResults.png)
![](https://github.com/fola789/Neural-Architecture-Search-with-Nature-Inspired-Algorithims/blob/main/ReadMeImages/simulatedAnnealingResults.png)
