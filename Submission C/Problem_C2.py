# =============================================================================
# PROBLEM C2
#
# Create a classifier for the MNIST Handwritten digit dataset.
# The test will expect it to classify 10 classes.
#
# Don't use lambda layers in your model.
#
# Desired accuracy AND validation_accuracy > 91%
# =============================================================================

import tensorflow as tf


def solution_C2():
    mnist = tf.keras.datasets.mnist
    (training_images, training_labels), (test_images, test_labels) = mnist.load_data()
    # NORMALIZE YOUR IMAGE HERE
    training_images = training_images / 255.0
    test_images = test_images / 255.0
    # DEFINE YOUR MODEL HERE
    # End with 10 Neuron Dense, activated by softmax
    model = tf.keras.Sequential([tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
                                 tf.keras.layers.Dense(128, activation='relu'),
                                 tf.keras.layers.Dense(10, activation='softmax')])
    # COMPILE MODEL HERE
    model.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # TRAIN YOUR MODEL HERE
    model.fit(training_images, training_labels, epochs=5, validation_data=(test_images, test_labels))
    return model


# The code below is to save your model as a .h5 file.
# It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    model = solution_C2()
    model.save("model_C2.h5")
