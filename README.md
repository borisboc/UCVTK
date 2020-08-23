# UCVTK
UCVTK : a python Useful Computer Vision Tool Kit for us, the vision engineers, who need to be efficient and productive.

## Introduction
We all know that there are now a lot of great and powerful computer vision, machine learning, deep learning, point clouds (and so many more) open source libraries available for anyone. But still, why are we (the vision engineer) still often using some private/commercial products? Because they are "more convenient". It is not just a matter of laziness: we need to be efficient, productive, easy to understand and be understood. During the development phase, but also the debugging, maintenance, bug fixes ... That is my conclusion after working more than 7 years in machine vision and robotics, using very different technologies. I search for a long time, and I am now convinced that we need to make the development, debugging and maintenance of computer vision codes easier, thanks to very useful, non-intrusive, extensible tool kits. That is the aim of this repository. Please, do not hesitate to give you feedback via the issues / via email.
Sincerely, Boris Bocquet.

## UCVTK, what it does, its features

**UCVTK** helps you with tools, tool kits, functions, interactive GUIs in order to develop, debug, maintain your computer vision python codes in a more efficient, productive and professionnal way.
Currently, the features are : 
* Easy way to print images in your python console.
* Easy interactive drawing of Region Of Interests on your images.
* Easy  interactive blob (connected components) informations and selections on your images.

* Todo : grayval line profiles, interactive histograms, interactive grayval threshold, interactive blob threshold, integration with IDEs (e.g. Spyder) ... And so much more. Please provide some proposals!

## Requirements

* **numpy** (1.18.1, 1.19.1)
* **matplotlib** (3.1.3, 3.3.1)
* **pyqt5** (5.15.0)
* **opencv** (3.4.1, 4.4.0.42)
* **napari** (0.2.12, 0.3.6)

The written package version are the versions I used while implementing the project. So I considere this version as tested / validated. It should very probably work with other versions.

## Installation

An installation procedure should come later. Basically, install all dependencies using ```pip```.

Then you can clone the codes of this repository : 
```shell
git clone https://github.com/AKEOPLUS-boris-bocquet/UCVTK.git
```
If needed, install the requirements : 
```shell
cd UCVTK
python3 pip install -r requirements.txt
```

You can run the samples (see Testing paragraph).
You can call these modules in your own codes.
There are currently no better packaging. This will come later.

## Testing

If you sucessfully installed, you can run the samples in the root folder : 
* **example_print.py** : a very simple and comprehensive example about how to print an image in your python console.
* **example_roi.py** : a very simple and comprehensive example about how to interactively draw Regions Of Interest on an image. 
* **example_blobs.py** : a more specific (still simple and comprehensive) example about how to interactively get some informations and select blobs (connected components) on an image. 

## Code quality

I try to do my best to provide code with a certain level of quality even though python is not my main language. The code is commented and documented. With my IDE, I use some tools to check the syntax an . But of course all your proposals and pull requests are welcome !

## Contributing

Please fork, improve and propose your pull request !

## Donations

This work is definitly NOT to make money on it. My motivations are to provide easy and usefull codes that could help all people like me. Of course you may show your enthusiasm by giving a small donation => [![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/borisBocquet?locale.x=fr_FR) 
