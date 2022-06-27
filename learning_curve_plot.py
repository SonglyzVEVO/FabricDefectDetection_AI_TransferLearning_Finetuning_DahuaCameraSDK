import matplotlib.pyplot as plt 
import tensorflow as tf 
import numpy as np 


def learning_curve_fullplot(history):
    fig = plt.figure(figsize=(24,16))

    #plot accuracy
    plt.subplot(221)
    plt.plot(history.history["accuracy"],"bo--", label = "acc")
    plt.plot(history.history["val_accuracy"],"ro--", label = "val_acc")
    plt.title("acc vs val_acc")
    plt.ylabel("accuracy")
    plt.xlabel("epochs")
    plt.legend()

    #plot loss function
    plt.subplot(222)
    plt.plot(history.history["loss"],"bo--", label = "loss")
    plt.plot(history.history["val_loss"],"ro--", label = "val_loss")
    plt.title("loss vs val_loss")
    plt.ylabel("loss")
    plt.xlabel("epochs")
    plt.legend()
    plt.show()

def plot_acc(history):
    plt.plot(history.history["accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epochs")
    plt.show()

def plot_loss(history):
    plt.plot(history.history["loss"])
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epochs")
    plt.show()

def plot_val_acc(history):
    plt.plot(history.history["val_accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epochs")
    plt.show()

def plot_val_loss(history):
    plt.plot(history.history["val_loss"])
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epochs")
    plt.show()

