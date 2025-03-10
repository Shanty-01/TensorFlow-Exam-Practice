# ===================================================================================================
# PROBLEM B4
#
# Build and train a classifier for the BBC-text dataset.
# This is a multiclass classification problem.
# Do not use lambda layers in your model.
#
# The dataset used in this problem is originally published in: http://mlg.ucd.ie/datasets/bbc.html.
#
# Desired accuracy and validation_accuracy > 91%
# ===================================================================================================

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import pandas as pd
import numpy as np

def solution_B4():
    bbc = pd.read_csv('https://github.com/dicodingacademy/assets/raw/main/Simulation/machine_learning/bbc-text.csv')

    # DO NOT CHANGE THIS CODE
    # Make sure you used all of these parameters or you can not pass this test
    vocab_size = 1000
    embedding_dim = 16
    max_length = 120
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = "<OOV>"
    training_portion = .8

    # YOUR CODE HERE
    # Using "shuffle=False"
    X = bbc['text']
    y = bbc['category']

    training_sentences, validation_sentences, training_labels, validation_labels = train_test_split(X, y,
                                                                            train_size=training_portion, shuffle=False)

    # Fit your tokenizer with training data
    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.fit_on_texts(training_sentences)
    sequences = tokenizer.texts_to_sequences(training_sentences)
    padded = pad_sequences(sequences, maxlen=max_length, truncating=trunc_type, padding=padding_type)

    validation_sequences = tokenizer.texts_to_sequences(validation_sentences)
    validation_padded = pad_sequences(validation_sequences, maxlen=max_length, truncating=trunc_type,
                                      padding=padding_type)
    
    # You can also use Tokenizer to encode your label.
    tokenizer_label = Tokenizer()
    tokenizer_label.fit_on_texts(bbc['category'])
    sequences_labels = tokenizer_label.texts_to_sequences(training_labels)
    validation_labels_sequences = tokenizer_label.texts_to_sequences(validation_labels)

    sequences_labels = np.array(sequences_labels)
    sequences_labels = np.reshape(sequences_labels, (-1,))

    validation_labels_sequences = np.array(validation_labels_sequences)
    validation_labels_sequences = np.reshape(validation_labels_sequences, (-1,))

    class Callback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if logs.get('val_accuracy') > 0.91 and logs.get('accuracy') > 0.91:
                print("\nAccuracy is higher than 0.91 so cancelling training!")
                self.model.stop_training = True
    callbacks = Callback()

    model = tf.keras.Sequential([
        # YOUR CODE HERE.
        # YOUR CODE HERE. DO not change the last layer or test may fail
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.9),
        tf.keras.layers.Dense(6, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.005), metrics=['accuracy'])
    model.fit(padded, sequences_labels, epochs=20, validation_data=(validation_padded, validation_labels_sequences), callbacks=[callbacks])
    # Make sure you are using "sparse_categorical_crossentropy" as a loss fuction

    return model

    # The code below is to save your model as a .h5 file.
    # It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    model = solution_B4()
    model.save("model_B4.h5")
