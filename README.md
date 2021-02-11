# Two_generator
This neural network works on my [nero_net](https://github.com/Respman/nero_net) project.

This net tries to determine whether the numbers given to it belong to first or second linearly congruent pseudo-random sequence generator with different settings.

How to use this project:

* generate test and working examples for training, run ./generator.py

* train the network using the program ./nero_net_v3_teaching.py

* use resulting network using the program ./nero_net_v3_using.py. It will display the number of guessed examples from the control group of samples.

All programs are configured via their own json configuration files.
