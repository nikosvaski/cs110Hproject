# this is code for a neural network that reads in 28x28 handwritten drawings from pytorch and
# feeds it through 2 sets of convolutional layers for reading features and then through classification 
# layers to organize feature into a prediction for the digit that is written.

import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import v2




BATCH_SIZE = 64
EPOCHS = 1

LOSS_FN = nn.CrossEntropyLoss()
DEVICE = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
# constants that tell the model how many times to run through the dataset, how big each "pull" of the 
# dataset should be for each backprop, and what algorithms and hardware to use for training the model



class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1,32, kernel_size = 3, padding = 1), # [1,1,28,28] -> [32,1,28,28]
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2), # [32,1,28,28] -> [32,1,14,14]
            nn.Conv2d(32,64, kernel_size = 3, padding = 1), #[32,1,14,14] -> [64,1,14,14]
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2), # [64,1,14,14] -> [64, 1, 7, 7]
        )

        # the above class atribute is a method to extract features from the original image
        # data and produces 64 differnt 7x7 feature maps, Ive provided comments for tracking
        # tensor shapes below

        self.classify = nn.Sequential(
            nn.Flatten(),
            nn.Linear(3136,128),
            nn.ReLU(),
            nn.Linear(128,10)
        )

        # this is the next stage of the model, it turns the 4-dimensional tensor and flattens 
        # it into a 1-D tensor. that tensor is then fed through as traditional fully connectwd 
        # layer and then presented into a 10 logits, each represented a probability of a number.
        # a softmax function is not necessary because the error function for training optimizes 
        # final probabilities to be a probability distrubtion


    def forward(self, x):
        x = self.features(x)
        logits = self.classify(x)
        return logits
    # this is essentially the "run" of the model, it is a function that takes input and passes
    # it sequentially through the model's arcitechture

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    global batch_n
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(DEVICE), y.to(DEVICE)

        pred = model(X)
        loss = loss_fn(pred,y)
        # captures the final output of the model for a data and the difference from the correct prediction

        batch_loss.append(loss.item()) 
        batch_n += 1
        # data capture for graphs of model progress

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch+1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(DEVICE), y.to(DEVICE)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
            # run through the dataset exclusively used for testing, compute the accuracy from loss
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

def data_harness():
    training_data = datasets.MNIST(
    root="data",
    train=True,
    download=True,
    transform=v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)]),
    )

    test_data = datasets.MNIST(
    root="data",
    train=False,
    download=True,
    transform=v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)]),
    ) 

    # download the MNIST dataset from the torch library

    return training_data,test_data


def loader_harness(training_data, test_data):
    train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE)
    test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE)

    # package MNIST dataset into a torch dataloader object to be fed into the model

    return train_dataloader,test_dataloader

def data_plot(training_data, batch_n, batch_loss):
    labels_map = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    }

    # dict for matching data to catagories

    display = 12
    plt.figure("data sample")
    for plot in range(display):
        plt.subplot(4,3,plot+1)
        sample_idx = torch.randint(len(training_data), size=(1,)).item()
        img, label = training_data[sample_idx]
        plt.title(labels_map[label])
        plt.axis("off")
        plt.imshow(img.squeeze(), cmap="gray")
        # this plot displays drawings in accordance with their catagories to visualize the data 
        # from the MNIST dataset that is being used in training the model
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.4)

    plt.figure("training loss")
    plt.subplot(1,1,1)
    plt.plot(list(range(batch_n)),batch_loss)
    plt.xlabel("batch")
    plt.ylabel("loss")
    plt.title("loss over training")
    # this plot tracks and displays the loss with every epoch

    plt.show()

def train_loop(train_dataloader,test_dataloader,model,optimizer,epochs):
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        epoch_loss = train(train_dataloader, model, LOSS_FN, optimizer)
        test(test_dataloader, model, LOSS_FN)
    # run through the specified amount of epochs and train the model on all of the train data
    print("Done!")

def show_model(model):
    print(model)
    # prints out the model arcitechture and structure


if __name__ == "__main__": # MAIN RUNTIME SEQUENCE FOR FILE
    print(f"Using {DEVICE} device")
    model = NeuralNetwork().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    # specify the model object and optimizer algorithm to be used in training

    batch_n = 0
    batch_loss = []
    show_model(model)
    training_data, test_data = data_harness()
    train_dataloader, test_dataloader = loader_harness(training_data, test_data)
    # get and seperate data

    train_loop(train_dataloader, test_dataloader, model, optimizer,EPOCHS)
    print("done!")
    # train the model

    test(train_dataloader, model, LOSS_FN)
    # run a final test of the model using the training data

    torch.save(model.state_dict(), 'model_state_dict.pth')
    print("State dict saved.")
    # save the trained model weights into a different file that can be used to run inference without 
    # running the whole training algorithm again
    
    data_plot(training_data, batch_n, batch_loss)
    # display visualizations for data and training progress
    
