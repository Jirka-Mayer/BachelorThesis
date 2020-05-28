<!--
# Some Links

Medvěd: https://mj.ucw.cz/vyuka/bc/

Hajič Jr. thesis proposal: http://ufal.mff.cuni.cz/~zabokrtsky/pgs/thesis_proposal/jan-hajic-jr-proposal.pdf
A Starting Point for Handwritten Music Recognition: https://openreview.net/pdf?id=SygqKLQrXQ
From Optical Music Recognition to Handwritten Music Recognition: A baseline: https://www.sciencedirect.com/science/article/abs/pii/S0167865518303386
Handwritten Music Recognition for Mensural notation with convolutional recurrent neural networks: https://www.sciencedirect.com/science/article/abs/pii/S0167865519302338

HTR (TU Wien): https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742
-->

# Abstract

Optical music recognition is a challenging field similar in many ways to optical text recognition. It brings, however, many challenges that traditional pipeline-based recognition systems struggle with. The end-to-end approach has proven to be superior in the domain of handwritten text recognition. We tried to apply this approach to the field of OMR. Specifically, we focused on handwritten music recognition. To resolve the lack of training data, we developed an engraving system for handwritten music called Mashcima. This engraving system is successful at mimicking the style of the CVC-MUSCIMA dataset. We evaluated our model on a portion of the CVC-MUSCIMA dataset and the approach seems to be promising.


# Introduction

<!-- Co je OMR -->

Optical music recognition (OMR) is an interesting subfield of computer vision. It shares a lot of similarities to optical character recognition (OCR) and handwritten text recognition (HTR). It is, however, more challenging as is pointed out in the paper *Understanding Optical Music Recognition* (https://arxiv.org/pdf/1908.03608.pdf). For example in OCR, characters are read in one direction, typically from left to right. Musical symbols seem to be similar in that a staff is also read from left to right, but many symbols can be placed above each other. Piano scores can even have symbols that span multiple staves.

Although a musical score can be very complex, many scores are not. We can limit ourselves to scores that are monophonic, have a single voice and have symbols spanning only one staff. Monophonic scores lack chords, meaning there's only one note plaing at a time. This holds, for example, for windblown instruments, since they cannot play multiple notes simulatenously. Sometimes multiple voices (instruments) are engraved in a single staff to save space. We will not attempt to read these scores either. It would be like reading two lines of text simultaneously and the proposed model can output only a single sequence. Also deciding what voice a given note belongs to is in itself a complicated problem.

<!-- v HTR se používá RCNN, protože je fajn (https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742) nebo (http://www.jpuigcerver.net/pubs/jpuigcerver_icdar2017.pdf)
Jednak, druhak jsem ji vybral, protože s ním mám zkušennosti, třeťak Calvo 2018 ji taky použil -->

Deep neural networks have transformed the field of computer vision recently. Especially convolutional networks (CNN), whose architecture is particularly well suited for image processing. Recurrent neural networks (RNN) have been used for sequence processing, like natural language modelling or natural language translation. We can combine these two architectures to create a so called RCNN network. When trained using connectionist temporal classification (CTC), we get a powerful architecture that is ideal for processing visual sequential data (http://www.jpuigcerver.net/pubs/jpuigcerver_icdar2017.pdf). This architecture has been used in handwritten text recognition to yield state-of-the-art results (https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742).

<!-- tuhle architekturu zkusil Calvo 2018 na primusu -->

If we limit the complexity of musical scores to the point that a single staff can be represented as a sequence of tokens, we can use this architecture to tackle the problem of OMR. This approach has been tried in 2018 by Calvo-Zaragoza and Rizo in 2018 (https://www.mdpi.com/2076-3417/8/4/606). They created the PrIMuS dataset, which contains 87678 real-music incipits. An incipit is the part of a melody or a musical work that is most recognizable for that work. Each incipit is a few measures long, typically shorter than a single staff of printed sheet music would be.

<!-- primus je nice and all, ale je sázenej, jenže hodně not je ručně psanejch (to je ta díra co plním) -->

The resulting model has been compared against Audiveris, an open-source OMR tool (https://github.com/Audiveris), and has proven to be superior on the PrIMuS dataset. However the dataset contains printed images only. Since this RCNN architecture is an end-to-end approach, there's a great chance that it would be ideal for reading handwritten scores as well (drawing analogy from HTR).

<!-- my tohle chceme zkusit na ručně psaných *The goal of this thesis is: ...* -->

Therefore the goal of this thesis is to explore the end-to-end approach for optical music recognition of handwritten music scores. More specifically we want to train a RCNN network to yield the best possible results on the CVC-MUSCIMA dataset.

<!-- narazili jsme na nedostatek dat -->

We needed to obtain training data. We explored the *Collection of datasets for OMR* by Alexander Pacha (https://apacha.github.io/OMR-Datasets/) and quickly found out that the only dataset containing entire staves of handwritten sheet music is the CVC-MUSCIMA dataset (http://www.cvc.uab.es/cvcmuscima/index_database.html). Every other handwritten dataset contains only muscial symbols or is derived from CVC-MUSCIMA. Since CVC-MUSCIMA is intended for writer classification and staff removal, it contains only 20 parts, each written by 50 writers. That's far too small variability, given the task we are trying to solve.

<!-- takže součástí práce je taky Mashcima -->

Facing this issue we resorted to data augmentation. The idea is to take handwritten musical symbols and place them onto an empty staff to create a new staff image. We called this music engraving system *Mashcima* and the system is explained in the chapter [M](#M). The muscial symbols used by Mashcima come from the MUSCIMA++ dataset (https://ufal.mff.cuni.cz/muscima). This dataset is built on top of CVC-MUSCIMA and provides pixel-perfect symbol segmentation and relationships between symbols. The reason we choose MUSCIMA++, instead of other musical symbol datasets, is that it is built on top of CVC-MUSCIMA. This means the image resolution and overall style is consistent with CVC-MUSCIMA. Also MUSCIMA++ has been developed at Charles University and so it was easy to contact its creator when needed. We however do make sure, that the final evaluation is performed on data the neural network has not seen during training. Specifically it trains on staves by completely different writers than the ones used for evaluation.

Mashcima engraving system is the main feature that sets this thesis apart from other works. Other people, when faced with the lack of training data, used simple data augentation (dilation, blurring, distortion) or transfer learning (https://openreview.net/pdf?id=SygqKLQrXQ). We belive that custom engraving system for hadwritten music is the best way to produce overabundance of high quality training data. Our confidence stems from the fact, that non-trained human has difficulties distinguishing a real-world sample from a well-engraved one.

    figure comparing one staff from CVC-MUSCIMA and one from PrIMuS, engraved using Mashcima

<!-- jak práce dopadla - úspěch nebo ne? -->

It is difficult to evaluate an OMR system in general. This is because there is no standard dataset that can be used and no standard set of metrics. Moreover we proposed a new Mashcima representation for the music engraved in a staff. This representation is based on the agnostic encoding proposed by Calvo-Zaragoza and Rizo (https://grfia.dlsi.ua.es/primus/). Using custom representation makes it yet more difficult to compare our results to other works. That being said, we can still make some comparisons. It seems that having specialized engraving system is a step in the right direction. The results we obained when evaluating are comparable to simmilar works performing simmilar evaluation (https://openreview.net/pdf?id=SygqKLQrXQ).

<!-- MusicXML nebylo implementováno
Image preprocessing nebyl implementován, máme už binarizovaný vstup -->

The thesis assignment states that output of our model will be a MusicXML file. We quickly realized that the problem is far larger then anticipated and so we focused on the core features only. Similarly the model input is not a plain photo or scan. It is already preprocessed and binarized. This problem has already been solved during the creation of the CVC-MUSCIMA dataset (http://www.cvc.uab.es/cvcmuscima/index_database.html), therefore we didn't tackle it either.

<!-- odkaz na github -->
Also there's a Github repository containing all the source code and text of this thesis at https://github.com/Jirka-Mayer/BachelorThesis. There's also a release tag corresponding to the time this thesis was submitted and it contains all the trained models for download.


## Thesis outline

**Chapter 1:** This chapter describes the specific model we decide to use for our OMR task. It discusses traditional methods and how deep neural networks help us simplify the process. It describes models other people used for similar tasks and how we've been influenced by them.

**Chapter 2:** This chapter mainly describes the Mashcima music encoding - the encoding we used for our model. It describes how it relates to the PrIMuS agnostic encoding, and why we made certain decisions regarding its design.

**Chapter 3:** This chapter talks about the Mashcima engraving system. Why we developed this system and what problem it solves. How it works, what are its limitations and how it can be extended.

**Chapter 4:** This chapter describes experiments we performed. These experiments aim to measure performance of our approach and test hypotheses postulated in previous chapters. We will also attempt to compare our results to other similar works.


# Related Work


## CVC-MUSCIMA dataset

CVC-MUSCIMA is a dataset presented in the article: *[CVC-MUSCIMA: A ground truth of handwritten music score images for writer identification and staff removal](https://www.researchgate.net/publication/225445011_CVC-MUSCIMA_A_ground_truth_of_handwritten_music_score_images_for_writer_identification_and_staff_removal)*. This dataset contains 1000 sheets of music, consisting of 20 pages, each written by 50 different musicians. It's the only publicly available dataset containing entire staves of handwritten music. The dataset has been designed for writer identification and staff (staffline) removal tasks. It contains two sets of images. One set for writer identification (containing gray, binary and staff-less binary images) and one set for staff removal (contains raw, staff-less and staff-only images, all binary).

We will use part of the staff removal set for evaluation. We will also use another part of the staff removal set for engraving, but indirectly via the MUSCIMA++ dataset.


## MUSCIMA++ dataset

MUSCIMA++ is a dataset developed by Jan Hajič jr. and Pavel Pecina and has been presented in the article: *[In Search of a Dataset for Handwritten Optical Music Recognition: Introducing MUSCIMA++](https://arxiv.org/abs/1703.04824)*. This dataset provides additional information for a subset of the CVC-MUSCIMA dataset. MUSCIMA++ contains 140 sheets of music. Each sheet is annotated at the level of individual symbols (noteheads, stems, flags, beams, slurs, stafflines). Each one of these symbols is classified, contains a bounding box and a pixel mask. These symbols are then interlinked in a graph that can be traversed to extract higher-level objects (notes, key signatures, beamed note groups).

We will use the dataset as a collection of musical symbols. We will then place those symbols onto an empty staff to create sythetic training data. The additional data (relationship graph) will help us position certain symbols properly.


## End-to-End OMR and the PrIMuS dataset

This section refers to the article: *[End-to-End Neural Optical Music Recognition of Monophonic Scores](https://www.mdpi.com/2076-3417/8/4/606)*. This article first discribes the PrIMuS dataset (https://grfia.dlsi.ua.es/primus/). This dataset contains 87678 real-music incipits. An incipit is the part of a melody or a musical work that is most recognizable for that work. Each incipit is a few measures long, typically shorter than a single staff of printed sheet music. Each incipit is encoded in a few widely known encodings (MEI, MIDI) and has a corresponding printed image. This image has been engraved using the music notation engraving library Verovio (https://www.verovio.org/). Each incipit is also encoded using two on-purpose devised encodings - the PrIMuS semantic and agnostic encoding. These encodings are interesting, because they are the output of a model proposed in the article, but also the Mashcima encoding described in [chapter 2](#2) of this thesis is very simmilar to the agnostic encoding.

The article also proposes a neural network architecture for an end-to-end solution of OMR. The architecture is very similar to ours, almost identical. It also uses the connectionist temporal classification as the loss function, which shapes the PrIMuS dataset encoding formats. This thesis  differs from this article mainly in the focus on handwritten music and the introduction of a custom engraving system for handwritten music. This article focuses on printed music only.

We will use the PrIMuS dataset as a source of melodies that can be used as input to our engraving system. The will also take this article as a basis for our Mashcima encoding and our model architecture.


## HMR baseline article

This section refers to the article: *[From Optical Music Recognition to Handwritten Music Recognition: A baseline](https://www.sciencedirect.com/science/article/abs/pii/S0167865518303386)*. This paper proposes a model that should serve as a baseline for handwritten music recognition. The model is again a convolutional recurrent neural network that recognises entire staves. The model is trained on printed music and then, using transfer learning, fine-tuned on handwritten music. The handwritten music comes from the MUSCIMA++ dataset and it has been varied using data augmentation (blurring, erosion, dilation, measure shuffling). This model, however, does not use CTC loss function, instead it produces two vectors for each pixel of the input image width. One vector contains symbols that are present in the image at that position and the other vector contains pitches of these symbols. This means annotations have to be aligned with the symbols (unlike with CTC), but it allows the model to recognise dense music sheets and even chords.

We will attempt to compare our model to the one from this article. The comparison will be difficult, because the output formats are so different, but we will mention all the differences and add a qualitative comparison of the final predictions. We want to utilize the fact that our evaluation dataset intersects with theirs and so we can perform direct comparison.


# Deep Neural Network

This chapter talks mainly about the model we decided to use. First we describe the full pipeline of a traditional OMR system. Many of these steps are shared between traditional and deep learning approaches. Then we will talk about the deep learning approaches that can be taken. Neural networks can replace parts of a traditional pipeline, or they can be used in an end-to-end setting, where the neural network replaces the most difficult core of the pipeline. We will describe our architecture consisting of a convolutional block, recurrent block and the connectionist temporal classification (CTC) loss function. Following sections describe in more detail what a neural network is and how the individual blocks of our model work internally. The last section explains how CTC works and what are its pros and cons, compared to the approach described in the HMR baseline article (*link*).


## Traditional approaches

A musical score intended for OMR typically begins as a raster image. This image is a photo or a scan of a real-world sheet of paper. The image needs to be prepared first. We need to find the sheet of paper in the image and correct any rotation or perspective distortion. Scanned images are easier to prepare, because they don't contain any perspective deformation and lighting artifacts. Searching for the paper in the image can be performed using many approaches, e.g. by using maximally stable extremal regions (http://cmp.felk.cvut.cz/~matas/papers/matas-bmvc02.pdf). We can detect stafflines using probabilistic Hough transform (https://en.wikipedia.org/wiki/Hough_transform). We can then use this information to remove any affine distortion of the image.

Next step is performing some color normalization and binarization. There might be a light-intensity gradient over the image, so we do some automatic contrasting to bring the lightness to a constant level across the image. Median filtering can be applied to remove noise (https://www.uio.no/studier/emner/matnat/ifi/INF2310/v12/undervisningsmateriale/artikler/Huang-etal-median.pdf). Conversion to grayscale image is often used, since color is not useful for OMR. The image can then be binarized to further remove unnecessary information. There are many thresholding algorithms that can be used for this step, many of which are implemented in the OpenCV library (https://opencv.org/). Binarization is important for traditional approaches, since they often use methods based on connected components to detect individual symbols. Neural networks could benefit from non-binarized images, since binarization can create aliasing artifacts that distort the input image on pixel level.

The steps described above are shared by both traditional and neural network based approaches. Traditional approaches now usually perform staffline removal. This step lets methods based on connected components to become useful. Staff localization may be an important part of this step. Symbols then need to be segmented and classified separately. Meaning is then reconstructed by looking at the relationships between all the classified symols. With the musical score understood at the symbol level, the extracted information can be converted to some final representation (MusicXML, MEI, MIDI).


## Deep learning approaches

Deep learning is a class of machine learning that focuses on deep neural networks. Deep learning has risen over the past two decades and became a very powerful tool for solving many problems, especially classification problems regarding computer vision. Neural networks can be used in many places throughout the pipeline of a traditional OMR system. They can be used for staffline removal (https://link.springer.com/article/10.1007/s00138-017-0844-4), symbol classification (http://mipal.snu.ac.kr/images/3/3b/ICISS_MuSymb.pdf) or even symbol detection (https://hal.archives-ouvertes.fr/hal-01972424/document).

Recently, neural networks have been used to tackle the problem of OMR in an end-to-end fashion (*link primus, link HMR baseline*). This approach allows us to replace many stages of the pipeline with a single model. The input sheet of music is usually processed staff by staff, so an intial segmentation of staves is required. This step is, however, very robust and can be performed reliably.

Main steps unified by an end-to-end system are segmentation, symbol classification and part of the relationship extraction. This means we don't need to explicitly specify structure of this part of the pipeline, which saves a lot of time and thinking. Also any intermediate features that would be extracted (like noteheads) need not be specified. The deep neural network has the ability to learn, what those features are. Moreover it can adapt these features to the problem better than a human could.

Deep learning, especially in an end-to-end approach also has some drawbacks. The first is bound to the ability of the model to learn the solution from data. While it's very helpful, that we don't have to desing part of our OMR system manually, it's often very difficult to acquire enough high-quality data for the training. Also the more complex our model is and the more learned paramateres it has, the more training data it requires. The data also needs to be high quality. Ambiguity and mistakes in annotations lead to poor performance of the resulting model. The trained model can only ever be as good as it's training data.

The second drawback is the very difficult nature of debugging the model. Neural network is by design a black box and we cannot easily assign specific meaning to any of its internal parts. The process of fixing a mistake the model makes is tedious and requires a lot of experimentation and re-training.


## Our architecture

As stated in the title of this thesis, we decided to explore the end-to-end approach to OMR using deep neural networks. We were primarily inspired by these three models:

- End-to-End Neural Optical Music Recognition of Monophonic Scores by Calvo-Zaragoza and Rizo (*link*)
- SimpleHTR by Harald Scheidl (https://github.com/githubharald/SimpleHTR)
- From Optical Music Recognition to Handwritten Music Recognition: A baseline (*link*)

All of these models share the same high-level structure. They combine a convolutional neural network (CNN) with a recurrent neural network (RNN). This combination is sometimes called the RCNN architecture. Convolutional neural networks are used in image processing. Their architecture is inspired by the way filters work in computer graphics (convolving a kernel over the source image). They learn to extract edges, corners and then even more abstract features like noteheads and stems. Recurrent neural networks are used for sequence processing (text and speech). They have been designed to carry state information throughout the input sequence. In our case they learn to propagate information horizontally - like infering pitch of an accidental from the pitch of a neighbouring note. The CNN block learns to extract features that th RNN block then learns to combine into more abstract features.

    image of the blocks (image -> cnn -> rnn -> ctc -> resulting vectors)

The CNN block can be followed by fully connected layers that further refine the result, although these layers are not necessary and our achitecture doesn't contain them. This may be due to the fact that our encoding is very close to the symbolic visual representation and so most of the heavy lifting is probably performed in the CNN block.

The final layer outputs a sequence of vectors, where each vector represents one time-step (horizontal slice of the input image). Values in such vector correspond to probabilities of individual output classes (tokens) at that given time-step. One additional class *blank* is added, that represents "no symbol present". The most likely class for each time-step is selected and then repetitions of the same class are collapsed into one token. Lastly all the blank symbols are removed. The remaining sequence of classes is mapped directly onto annotation tokens of the Mashcima encoding explained in the [chapter 2](#2). This approach is called greedy CTC decoding (https://www.cs.toronto.edu/~graves/icml_2006.pdf) and is used during training. For evaluation a more advanced method is used, called beam search decoding (https://arxiv.org/pdf/1601.06581.pdf).

When training, loss is computed using connectionist temporal classification (CTC) (https://arxiv.org/pdf/1601.06581.pdf). The loss function provides a gradient for improving the network. This gradient is then calculated for the entire network using the backpropagation algorithm (https://www.deeplearningbook.org/contents/mlp.html#pf25). Parameters are then updated using the adaptive learning rate optimizer (Adam) (*link*).

Values of all hyperparameters, including sizes and types of all layers are specified in the section [1.2.3](#123).


### Neural network

Neural network is a model inspired by the human brain. Its core building block is a perceptron (analogous to a neuron in the brain). Perceptron is a node that has a number of inputs (real numbers), combines them, and produces a single output value. The mathematical description is following:

$$
    y = \varphi(w \cdot x + b)
$$

Vector $x$ contains all the input values. It is multiplied by a vector of weights $w$ and a constant scalar bias $b$ is added. The result is passed through an activation function $\varphi$ that produces the output value $y$. The core idea behind this model is that a perceptron activates (fires), when enough inputs activate. Weights and the bias are parameters that allow the perceptron to learn - to detect a specific pattern in the input values. The activation function attempts to model the activation threshold and introduces non-linearity into the system.

One of the first activation functions to be used was the sigmoid function $\frac{1}{1 + e^{-x}}$, but it suffered from the problem of vanishing and exploding gradients (https://en.wikipedia.org/wiki/Vanishing_gradient_problem#cite_note-1). Hyperbolic tangent function was then used to remedy this problem. Nowadays, rectifier function is often used ($\max(0, x)$), because it is easy to compute. Perceptrons with this function are called rectified linear units (ReLU). It also has some problems, so leaky ReLU can be used to address them (https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf).

Perceptrons can be interconnected to form neural networks. Typical architecture is a feedforward neural network (FNN). It organizes perceptrons into layers, through which information flows in one direction. The resulting graph is directed and acyclic, which allows us to understand the whole network as a complex mathematical function and lets us train it using the backpropagation (https://en.wikipedia.org/wiki/Backpropagation#cite_note-1) and gradient descent (https://www.deeplearningbook.org/contents/optimization.html) algorithms.

The simplest feedforward network is a network with dense (fully connected) layers. Each perceptron in a given layer receives input as output of all perceptrons in the previous layer.

    image of a dense network with some layers (individual perceptrons should be visible)


### Convolutional neural network

Convolutional neural network (CNN) is a kind of feedforward network. It is ideal for processing visual data. A CNN is build from two kinds of layers:

**Convolutional layer** A convolutional layer is similar to a fully connected layer, but the connections are only local. The input and output is a two-dimensinoal array of numbers (like one channel of an image). Each perceptron takes input from only a small window of neighbouring perceptrons in the input layer (3x3, 5x5, 7x7). Weights are represented by a kernel of the same size as this neighbourhood window. This kernel is shared by all the perceptrons, reducing the number or learned argments substantially and allowing the layer to process images of variable sizes. There may be many input and output arrays (channels), then the layer has one kernel for each pair of channels. This architecture is inspired by the convolution filters from computer graphics - hence the name.

**Pooling layer** A pooling layer typically follows a convolutional layer. It's job is to downsample the image, reducing its spatial resolution, while preserving the number of channels. The downsampling is performed by splitting the input into a set of ractangular regions (that may overlap) and then reducing each region using max, sum or average function. Widely used function is the maximum and the resulting layer is called a *max pooling layer*. The pool size is typically 2x2.

**Fully-connected layer** One or more fully connected layers can be added at the end of a CNN, to further refine features extracted by the previous layers. This layer is often present in models performing classification, because we want to reduce the number of outputs to the number of classes we are predicting.

A CNN has typically many convolutional layers, combined with pooling layers. Each time the spatial dimensions shrink in a pooling layer, more channels are added to be able to represent more features. This forces the network to create abstractions and convert the visual data into some abstract representation vector.

    some image of a convolution


### Recurrent neural network

A recurrent neural network (RNN) is a network intended for sequence processing. Input for the network is a sequence of vectors and the output is a sequence of the same length. The recurrent network can be understood as composed of recurrent units, each with two inputs and two outputs. A unit accepts one vector from the input sequence and an old state vector. It outputs corresponding vector of the output sequence and the new state vector. These recurrent units can be unrolled along the input sequence and each one passes the state vector to the next one, using it to send information along the length of the sequence. All instances of the recurrent unit share the same learned parameters and so can be unrolled to any length necessary. The sequence dimension, where unrolling happens, is called the time dimension.

    image of an unrolled recurrent network (e.g. for NLP)

The internal architecture of a recurrent unit may vary, but it's often a feedforward network, where the input and output vectors are both split into a sequence part and a state part. The most common reccurent unit architectures are the long short-term memory (LSTM) (https://en.wikipedia.org/wiki/Long_short-term_memory#cite_note-lstm1997-1) and the gated recurrent unit (GRU) (https://en.wikipedia.org/wiki/Long_short-term_memory#cite_note-11). You can join two reccurrent layers, passing information in opposite directions, to create a bidirectional recurrent layer.


### Connectionist temporal classification

A recurrent neural network outputs a sequence of vectors. If these vectors are the final output of the model, they typically represent class probabilities for a given time-step (we solve sequence classification). If we did OCR, we would have a set of characters (an alphabet) and the vector would have the same size as the alphabet. Each value in that vector would correspond to the probability of that given character being present at that given time-step. We could use the softmax function (https://en.wikipedia.org/wiki/Softmax_function#cite_note-FOOTNOTEGoodfellowBengioCourville2016184-1) to convert the perceptron activations to probabilities.

This creates a problem when training. In OCR, we want to produce a sequence of letters as the output. But one letter might span multiple time-steps in the input. This means we not only need the gold sequence of letters, we also need to know at which specific time-steps the letters are present. This mapping of output classes to specific time-steps is called *alignment* and it complicates the creation of a training dataset.

Connectionist temporal classification (CTC) (https://arxiv.org/pdf/1601.06581.pdf) is an approach that solves the alignment issue. CTC loss function is able to calculate the loss value over all possible alignments of our gold sequence over the output sequence. This allows us to train the model, without having explicit alignment.

When the model is trained, the greedy decoding algorithm (https://www.cs.toronto.edu/~graves/icml_2006.pdf) can be used to convert the output vector sequence to the proper prediction. This algorithm takes each vector of the output sequence and selects the most probable output class (letter). It then collapses all repetitions of that class into one occurrence, producing the final sequence. One special output class called *blank* is introduced, to prevent two actual successive occurences of a given class from being collapsed into one. This symbol is, however, after collapsing removed and will never be present in the final prediction.

There's also the option to use the beam search decoding algorithm (https://arxiv.org/pdf/1601.06581.pdf). This algorithm keeps a list of best decodings so far, as the entire decoding is being computed. Greedy decoding is a special case of the beam search decoding, where the list contains only one item. All partial decodings cannot be considered, because there is exponentially many of them.

Connectionist temporal classification has many benefits regarding the alignment problem, but it has some flaws as well. The loss computaion and the decoding rely on the fact, that there will be only one class predicted for each time-step. This means we cannot capture the fact of two symbols appearing in the input at the same time. This happens often with music. We can solve this problem partially by utilizing the recurrent layers. They will allow us to output simultaneous symbols sequentially, by remembering those symbols for a while. This however increases the length of the final sequence, but this sequence can never be longer than the total number of time-steps. We might run out of temporal resolution.

The HMR baseline article (*link*) opted not to use CTC and performed manual alignment instead. This let them to have a model that can predict multiple symbols simultaneously. This also reduces complexity of the output sequence and the model thus need not perform much additional work as in our case (see the section on [attachment ordering](#123)).


# Music Representation

This chaptes explores how music is represented within this thesis. It looks at the encodings devised for the PrIMuS dataset and how they've been modified to produce our Mashcima music encoding. Then we explore how this encoding can be used for annotating datasets and how it can be extended in the future.

All the encodings explored in this chapter are made for a model that produces a sequence of tokens. An encoding then defines a specific set of tokens and describes how they map onto the musical symbols. In the context of a neural network with a CTC loss function, we take all the tokens of an encoding and represent them as the individual classifier classes. How the tokens get indexed and how the blank symbol is represented is considered an implementation detail of the neural network and is not covered in the encoding specification.

We can provide a short overview of the terms used in this chapter:

- **Token** is a single item of the output sequence produced by a model.
- **Vocabulary** is the set of all tokens in an encoding.
- **Encoding** is a scheme for mapping musical staves onto a sequence of tokens.
- **Annotation** is a specific sequence of tokens.


## PrIMuS agnostic encoding

The PrIMuS dataset contains over 87 000 items, each with an image of the printed staff and then multiple files describing the music in that staff. There are two standard formats, namely Music Encoding Initiative format (MEI) and the Plaine and Easie code source. Then there are two on-purpouse encodings devised specifically for this dataset. These two encodings are what interests us.

    figure containing a sample incipit

The first of these two encodings is the *semantic encoding*. It represents what the musical symbols mean. Each symbol has a specific pitch that relies on the cleft at the begining of the staff. This makes the vocabulary much larger and any model using this encoding has take the clef into account when reading the symbols. It is however much easier to transform this encoding to some well known format like MusicXML, since these formats tend to represent the meaning of a score, not the score appearence.

    semantic encoding of the incipit above

The second encoding is the *agnostic encoding*. This encoding treats the staff visually as a specific positioning of specific symbols. It tries to capture what is in the staff visually, not what the symbols mean musically. This is comparable to a sentence being thought of as a sequence of letters, whereas the semantic encoding could be thought of as the specific sounds a written sentence represents. This makes the encoding harder to convert to a well known format acceptable by other music software. On the other hand this encoding is formal-enough to be easily converted to the semantic encoding, if read correctly. So this encoding lets the model do less work, therefore the model should do fewer mistakes.

    agnostic encoding of the incipit above

The agnostic encoding has also the advantage, that annotating an image is not as difficult for a human. Annotating an image using the semantic encoding requires the annotator to know pitches for a given key. The situation is even more complicated by key signatures. This means an untrained non-musician has to do a lot of thinking when annotating, which leads to many errors and slow annotation speed.

We've taken this agnostic encoding and modified it slightly to produce our Mashcima music representation.


## Mashcima music encoding


### Notes and pitches

Mashcima music encoding is an encoding that attempts to improve upon the PrIMuS agnostic encoding. In the source code, most of the logic regarding this encoding is placed inside the `app/vocabulary.py` file. Each token of this encoding represents some musical symbol.

    figure containing primus incipit engraved using Mashcima
    with the corresponding Mashcima encoding

The first symbol we need to encode is a note. A note has some duration and some pitch. These two pieces of information can vary independently, so it can seem logical to represent them using two vectors. The problem is that the connectionist temporal classification can output only one vector at a time. To solve this, we take every possible combination of note duration and pitch and create a token for that case.

| Mashcima token | Duration           | Pitch |
| -------------- | ------------------ | ----- |
| `w5`           | Whole note         | 5     |
| `h0`           | Half note          | 0     |
| `q-8`          | Quarter note       | -8    |
| `e-4`          | Eighth note        | -4    |
| `s9`           | Sixteenth note     | 9     |
| `t12`          | Thirty-second note | 12    |

> The table shows all possible note durations, each with some pitch.

Combining duration information and pitch information into a single token actually ends up being a reasonable solution. That is because the concept of note duration can be extended to a concept of symbol type in general. This is because not only notes have pitches.

The set of pitches we can choose from greatly impacts the vocabulary size. This is not a major issue, because the vocabulary size will still remain relatively small. Currently the vocabulary has around 550 tokens. The pitch range we choose spans from `-12` to `12` - that is from the fourth ledger line below the staff to the fourth ledger line above the staff.

The pitch encoding is built such that it would be easy to understand for a non-musician. In western music notation, pitch of a note is represented by the vertical position of that note on the staff. An empty staff is composed of 5 stafflines. Mashcima encoding sets the middle staffline position to be zero. Going up, the first space is pitch `1` and the first line is pitch `2`. Going down, the first space is pitch `-1` and the first line is pitch `-2`.

    image of rising half notes engraved using Mashcima
    with the corresponding tokens

This pitch encoding has the advantage of being vertically symmetric, which speeds up the manual annotation process. First ledger line above the staff is pitch `6`, and the first ledger line below is pitch `-6`. Second property this system has is that pitches placed on lines are even and pitches placed in spaces are odd.


### Rests and barlines

The second most common symbol is probably a rest. A rest has duration, just like a note, but it has no pitch information. Its vertical position may vary, but that doesn't encode any pitch information.

| Mashcima token | Duration                |
| -------------- | ----------------------- |
| `lr`           | Longa rest (4 measures) |
| `br`           | Breve rest (2 measures) |
| `wr`           | Whole rest              |
| `hr`           | Half rest               |
| `qr`           | Quarter rest            |
| `er`           | Eighth rest             |
| `sr`           | Sixteenth rest          |
| `tr`           | Thirty-second rest      |

> Table shows tokens for all rests that can be represented in the Mashcima encoding.

You may have noticed, that that there are two extra durations - longa and breve. Also there is missing the sixty-fourth rest. It all has to do with the fact that not all durations are used equally frequently. I based Mashcima on the CVC-MUSCIMA and MUSCIMA++ datasets. There is no occurence of longa or breve note in those datasets. There are, however, occurences of longa and breva rests. Similarly, sixty-fourth notes and rests are also not present. The vocabulary can luckily be extended to accomodate these symbols. See the section [X.Y.Z](#X.Y.Z) for more details.

Now that we have notes and rests, we can start groupping them into measures (bars). A barline is represented by the "pipe" character (`|`). Barlines separate notes and rests into groups of same total duration. There are many types of barlines (double barline, repeat signs) and although they are used quite often, they have not yet been implemented into the Mashcima engraving system. This is simply because we wanted to see, whether our approach even works. These special barline types can be easily added in the future.

    staff with some rests and barlines
    with tokens below


### Generic tokens

There are some tokens that contain pitch information and some that do not. Since the pitch information is often not required when inspecting a token sequence, it is useful to strip it away. This is why we define a *generic token* as a version of a token without pitch information. So for example a generic quarter note is represented by the `q` token.

Generic tokens are not present in the vocabulary and cannot be produced by the model. They should also never appear in the gold data. They are, however, often used when analyzing a given token sequence.

The only exception are tokens that don't contain pitch information (e.g. rests). They are considered to be their own generic token (i.e. the generic token for a quarter rest `qr` is still just `qr`).

The vocabulary file (`app/vocabulary.py`) has helper methods for working with pitches:

- `to_generic(token: str) -> str` Obtains generic version of a token, unless the given token is already generic.
- `get_pitch(token: str) -> Optional[int]` Obtains pitch of a token, or `None` if that token has no pitch.


### Attachments

It's often the case, that notes are decorated with symbols that slightly modify their meaning. Since these decorating symbols are bound to the note itself, we call them *attachments*. An attachment token is simply a token that belongs to some other non-attachment token.

There are many kinds of musical symbols that behave as attachments:

- **Accidentals** are symbols placed before a note and they modify their pitch by a semi-tone.
- **Duration dots** are placed after a note and they extend the duration of a note.
- **Articulation symbols** are usually placed below or above a note and they specify how the note should be played (e.g. staccato, tenuto, accent).
- **Other symbols**, like a tuplet number, fermata, trill, etc.
- **Artificial tokens**, that we've added to encode specific time-spanning symbols. See the section on [slurs](#slurs) to learn more.

You can see, that the term *attachment* is not a musical term and it describes more how a symbol is represented, not what a symbol means.

<!-- accidentals -->

All of these attachments lack pitch information, since the pitch is stored in the note token. The only exception here are accidentals. Accidentals are special, because they need not be attached to a note. They can be standalone in a key signature. This means that they need pitch information. This creates some redundancy in the encoding; when a note has an accidental, they both should have the same pitch. This condition is not ideal, because it may cause the model to make unnecessary errors. It is however better, than having different tokens for standalone accidentals and attached accidentals.

| Mashcima token | Accidental              | Pitch   |
| -------------- | ----------------------- | ------- |
| `#5`           | Sharp                   | 5       |
| `b4`           | Flat                    | 4       |
| `N-4`          | Natural                 | -4      |
| `x8`           | Double sharp            | 8       |
| `bb0`          | Double flat             | 0       |

> Table of accidentals with various pitches.

<!-- before & after accidentals -->

Attachments come in two kinds:

- **Before attachments** are placed before the target token
- **After attachments** are placed after the target token

By placement we mean placement in the token sequence. It may not correspond to the visual order of the symbols. The rule of thumb here is that tokens are ordered from left to right and from top to bottom. The problem is that some symbols may be both above and below a note, depending on the note pitch. Therefore we didn't make this into a strict rule and instead devised a specific ordering of the attachments:

<!-- ordering -->

| Before attachments | Meaning                 |
| ------------------ | ----------------------- |
| `)`                | Slur end                |
| `fermata`          | Fermata                 |
| `trill +`          | Trill                   |
| `tuplet.3`         | Tuplet number           |
| `# b N x bb`       | Accidentals             |

> Before attachments, properly ordered.


| After attachments  | Meaning                 |
| ------------------ | ----------------------- |
| `.`                | Staccato                |
| `_`                | Tenuto                  |
| `>`                | Accent                  |
| `^`                | Marcato                 |
| `* **`             | Duration dots           |
| `(`                | Slur start              |

> After attachments, properly ordered.

Here are few notes regarding the ordering:

- Slurs are always the first/last attachment.
- Some tokens are mutually exclusive, so are placed on the same level.
- There are many ornaments and this list is not exhaustive. It is meant to be extended in the future.
- Not all symbols here can be engraved by Mashcima.
- There can be many more tuplet numbers, only triplets are currently present.


### Slurs

Slurs and ties are one of the first symbols that make OMR complicated. Slur is a curved line going from one notehead to another. Notes that are under a slur should be played blended together without explicit note beginnings. Tie looks exactly like a slur, just the two notes it joins have the same pitch. This means the notes should be played as one long note. So the difference is only semantic, we will consider ties to be slurs.

Mashcima encoding does not represents slurs explicitly, but it represents their beginings and ends. This is acomplished by two attachment tokens, `(` and `)`. The problem it creates is that sometimes it's impossible to pair beginings and ends properly. Therefore we can only annotate staves that don't contain nested slurs.

Slurs can also span from one staff to the next. When this happens, the slur ends at a barline. Therefore a barline can also act as a token, on which a slur can start or end.

    image showing different slur variants


### Beams

Beamed notes pose simmilar problems as slurs, but they obey some additional constraints that make them easier to deal with. Beams are encoded from the perspective of a single note within the beamed group. Duration of this note depends only on the number of beams passing through its stem. We just need to distinguish the note from it's flag variant, therefore we add some information regarding the beam presence. The last problem is, that having a couple of beamed notes in a row does not tell us about the way the beams are groupped. Therefore we modify the beam presence information into two parts - beam ending and beam starting.

Therefore for a given note duration, we get three tokens, that represent all the possible beam situations:

    image of a sixteenth beamed group (s= =s= =s= =s e= =e)

This, however, allows for nonsensical annotations to exist. We can create un-finished and non-started beams. For this reason there is the `repair_annotation` function in the file `app/vocabulary.py` that can repair such situations or validate correctness of an annotation.


### Key and time signatures

Key signature is just a group of many accidentals, typically at the begining of a staff. These accidentals are not attached to any note, so they have special handling in the source code. They are not a problem from the annotaion point of view.

Time signature is either a symbol C, or a pair of two numbers on top of each other. The standalone C symbol can be represented easily using the `time.C` token. A pair of numbers is represented by two tokens, e.g. `time.3 time.4`. Numbers have to be paired. Non-paired time number is considered an invalid annotation.

    image of clef, time and key signatures

Time signature numbers are also treated specially, since they always come in pairs.


### Clefs and repeats

Clefs are encoded similar to rests, with the only difference of having a pitch assicoated. Not all pitches are allowed, though. There are three types of clefs (G, C, F). Each of these clefs has a set of pitches it can have.

    image of all clefs

There are special barlines that mark a part of music to be repeated. These barlines cannot be engraved yet, but they do have corresponding tokens in the encoding: `:|`, `|:`, `:|:`.


## Differences to PrIMuS

Mashcima encoding is very similar to the agnostic PrIMuS encoding, but there are some deliberate changes introduced. Mashcima encoding has on purpouse shorter token names. This aims to aid readability, when manually annotating. The goal is to fit one staff of tokens onto the screen. Common tokens, like quarter notes (`q5`), are also quick to get typed. We also decided to use characters that look like the musical symbols they encode (sharps `#5`, flats `b5`, barlines `|`).

The pitch is also encoded differently. In PrIMuS agnostic encoding, every token has a pitch - even a barline. The pitch might not be useful, but it's present, to smplify working with the encoding. We decided to leave some tokens without pitch information. That complicates the code, but makes the annotation more user-friendly.

Also the specific pitch values are different. PrIMuS indexes lines and spaces separately and the line zero is the first ledger line below the staff. We tried to improve on this by putting the line zero at the center of the staff. This makes the pitch values vertically symmetric. We also removed the separation of lines and spaces and we use just an integer value. That simplifies the code that deals with pitch information. This integer value is then odd in spaces and even on lines.


## Extensibility

Because the CVC-MUSCIMA dataset contains such a wide range of symbols, we didn't want to create an encoding that would capture every possible symbol in the dataset. Most of these unusual symbols are present in only a few places and adding them to the encoding would make everything much more complicated, for little to no return. Therefore the Mashcima encoding contains the `?` token. This token should be placed into gold data whenever we encounter a symbol (or a group of symbols) that cannot be represented by our encoding. This `?` token acts as a marker, that we cannot fully represent specific place in the staff. It can then be used to filter out such bars or just to find such places if the encoding was ever extended in the future.

<!--note durations-->
As mentioned in previous sections, there are missing some note and rest durations. These can be easily added when needed. These new tokens would follow the rules that are posed onto all the current notes and rests.

<!--dynamics-->
<!--tuplets and other attachments-->
Similarly there are many symbols that are not present in the encoding, but could be easily added. Dynamics cannot be encoded right now. They are ignored as if they wasn't present at all. They could be added as after attachments. Same applies to additional tuplets or simmilar ornaments.

<!--grace notes-->
Special place have grace notes. They look like little notes, they do not affect the rythm and are considered an ornament attached to another note. PrIMuS agnostic encoding can represent them, but at the expense of adding a lot of additional tokens. We decided not to bloat our vocabulary with symbols that aren't very abundant in the CVC-MUSCIMA dataset. They are present in a few places in the evaluation dataset and are represented by the `?` token.

<!--chords-->
A chord is two or more notes played simultaneously. Currently there is no way of encoding simultaneous notes. Since chords usually share a stem, they could maybe be represented via after attachments. Maybe if we encoded the top-most note of a chord as a regular note and then added one "notehead" token for every remaining note, we could represent a chord. But there are problems with having multiple accidentals. Either way it would be interesting to explore in some future work.

<!--text-->
Text (like lyrics and tempo) is also ignored. It is not encoded by even the `?` token.


# Engraving System

This chapter describes the Mashcima engraving system we developed. We created a custom engraving system for handwritten music to serve as an advanced data augmentation tool. We opted to write a new system from scratch, because of the flexibility we needed. We will talk about the specific requirements for the engraving system. We will briefly overview the inner workings of the system - how it understands the input (Mashcima encoding), what are the basic building blocks from which a staff image is engraved, what are the most important events that happen during engraving. We will talk about shortcommings of the system and how it could be extended in the future.


## Why custom engraving system

In the [thesis introduction](#123) we stated that there is only a single dataset containing handwritten staves of music. There are other handwritten music datasets, but they either contain only symbols, or they are derived from CVC-MUSCIMA. Using this dataset as-is for training is not plausible, because it contains far too few symbol combinations.

We are not the first to realise this issue. The HMR baseline article (*link*) talks about using data augmentation and transfer learning to solve the lack of training data. They propose a model to be trained on printed music, of which there's abundance. After that the model is fine-tuned by training on the CVC-MUSCIMA dataset. The results they obtained are impressive, considering the method they used. To help with the process, they used simple data augmentation, like dilation, erosion and blurring.

We propose to use more sophisticated data augmentation. Specifically we want to shuffle the data on the level of individual musical symbols. The reason we choose this approach is that we have access to the MUSCIMA++ dataset (*link*). This dataset contains a lot of additional information regarding the CVC-MUSCIMA dataset, which includes segmentation masks of individual symbols and their relationships. We want to use these masks to engrave entirely new staves of music.

We will also build our own engraving system, because engraving handwritten music is something that existing engraving systems don't focus on. Handwritten music is very different from printed music. Symbol positions vary, notehead shapes may differ from note to note within a single staff, slant angle may also change. We tried looking at Abjad (*link*) - a python package for engraving music that uses Lilypond (*link*) at its core. Lilypond is able to load custom fonts, but those have to be in vector form, not raster masks. Also there's no way to introduce a controlled variability and randomness into the engraving process. When we considered the options, we decided to create or own system, since it would be faster and we would have the ability to modify it in the future.


## Requirements

We are not trying to produce PDF files, like the other engraving systems do. Our goal is to produce a single staff of handwritten music, as a raster image. This image should look as simmilar as possible to a cropped image of a staff from the CVC-MUSCIMA dataset. This means the image is already binarized, it has comparable resolution and the image has about three times the height of the staff it contains (the height of the staff lines).

This similarity can be acomplished by using symbols from MUSCIMA++. In page 19 of writer 1, there's an empty staff. We take the mask of the staff lines and produce an empty image of proper dimensions containing the empty staff lines. The staff lines are almost perfectly horizontal (they wobble up and down by a few pixels, but don't drift), therefore we will use them to create a lookup table for converting pitch number to pixel offset in the $y$ axis. This will act as our blank canvas, from which we will start. *Canvas* is an actual term used in the codebase.

    image of an empty staff + show the spadding in the staff height on it

By trying to mimic the look of CVC-MUSCIMA, we will remove a lot of problems that we would otherwise face. We don't need to perform any distortion removal, alignment, cropping, preprocessing and binarization. All this is already performed on the source data we use. This lets us focus only on the engraving system, which is complicated enough by itself.


## Token groups and canvas items

The Mashcima encoding defines the concept of token groups. It is not discussed in the chapter on the encoding, because it is not so important for the encoding itself. A *token group* is a group of tokens, that has one main token and then all the attachments of that token. So for examplea quarter note with a sharp and a staccato dot is represented by three tokens, but it is a single token group. A token group is all the tokens that belong to some non-attachment token.

Token groups are used in Mashcima annotation validation. When proper attachment ordering is checked, the annotation is first groupped into token groups and then each group has its attachment order checked. It also helps us to hide away all the attachment tokens and focus only on the important tokens.

Two special kinds of token groups are key signatures and numeric time signatures. It again makes sense to treat a time signature as a single object and since it's actually a multitude of tokens, it's represented by a token group.

Token groups are important, because they map directly onto canvas items. A *canvas item* is something on the staff, that takes up horizontal space and can be rendered. Canvas item represents a barline, a note, a rest. Attachments, like accidentals and dots, are not canvas items, but are part of some given canvas item and they modify its appearance. Canvas items are placed on the staff righ after each other with some randomized amount of padding between them. A canvas item has all the vertical space it can have and it decides, where to draw itself vertically. You can see the bounding boxes of individual canvas items in the following figure:

    image of some music with bounding boxes around canvas items

Each canvas item type is represented by a class and the inheritance hierarchy can be seen in this diagram:

    inheritance diagram of canvas item classes


## Rendering flow

The process of converting an annotation to an image has couple of important steps:

**Canvas instance is created.** Instance of the `mashcima.Canvas` class is created, so that canvas items could be added into it.

**Canvas items are added.** The annotation is groupped into token groups and those groups are mapped onto canvas items. This step just feeds the semantic information from the encoding system to the engraving system. This step is performed by the `annotation_to_canvas` function inside `mashcima/annotation_to_image.py`.

The following steps happen inside the `Canvas.render(...)` method.

**Canvas construction is finished.** This goes over the added canvas items and extracts information about slurs and beams. This step also validates that beams and slurs are properly formed. This extracted information is used later during rendering of slurs and beams.

**Sprites are selected.** Each canvas item gets to choose specific symbol sprites (images) to use for rendering. These sprites are chosen from a symbol sprite repository, represented by the class `mashcima.Mashcima` inside the file `mashcima/__init__.py`.

**Sprites and canvas items are placed.** With specific sprites selected, dimensions are now known and so everything can be positioned properly. Canvas items are positioned from left to right one at a time. Each time a canvas item is placed, it also places its internal sprites (and attachments and other ornaments) and determines its total width.

**Beams are placed.** With note positions known, we can calculate proper position and angle for each beam. Once the beam position is calculated, length of stems of all corresponding notes is adjusted to match the beam.

**Everything is rendered.** Canvas items, beams and slurs are rendered. The order is not important, because the resulting image is binary.


## Slurs and beams

There are only a few symbols that are not taken from the MUSCIMA++ dataset as images, but are instead rendered manually. Those are slurs and beams. MUSCIMA++ does contain binary masks of these sybmols, but the problem is that they cannot be simply moved to a different position and rendered. They rely heavily on the position of other symbols and therefore they would need to be stretched, rotated and skewed in order to render properly.

Slurs have some pre-defined attachment points they can use and the specific attachment point is chosen by the way a note is flipped. Once the two points are chosen, the slur is rendered as a parabola. This approach far too naive and simplified, so it doesn't capture the whole variability of a handwritten slur. We think this is the reason the model makes so many mistakes regarding slur placement.

    some slur image

Beams face many similar problems as slurs. They are also rendered manually, as straight lines. This again does not capture the real world. Beams are often curved or they have a gap between itself and a note stem. This again seems to be the source of many mistakes, especially with the writer 49, who leaves a lot of gaps betweem beams and stems.

    some beam image


## Multi-staff images

Staves are usually so close together, that cropping a single staff with proper space around it will usually crop parts of symbols from the staves above and below. We want to capture this property of real-world data in our synthetic data.

We can take our rendering system and run it three times to render three staves into a single image. We crop out the middle staff we actually want. It can be used with some variations - having staff only above, or only below.

Multi-staff rendering can be performed by the `multi_staff_annotation_to_image` function inside `mashcima/annotation_to_image.py` file.

    multi-staff image here


## Additional deformation and normalization

Affine transformation is applied to the produced image to make the model resiliant to changes in image positioning, perspective, size and rotation. This transformation is subtle, but very important step of the systhetic data preparation.

Finally, before the image is fed into the model, it's normalized to a specified height, while preserving the aspect ratio. The resulting image can look like this:

    heavily skewed, normalized image of multi-staff


## Extensibility

There are many symbols that currently can be encoded, but not engraved (trills, accents, fermatas). These attachment symbols could be added relatively easily, in simmilar fashion to the way staccato dots and accidentals are rendered.

The slur and beam rendering system could be improved to better mimic the real world. The concept of attachment points for slurs is a little bit too digital. It could be made more fuzzy. Also there are certain slur placements, that the current system does not render (like slur above a beam). This kind of extension should not require too much redesign of the system.

It would be interesting to render tuplets. They are similar to beams and slurs in many ways. Also dynamics and hairpins are maybe even easier to add. But they cannot currently be encoded.

Adding chords is an interesting problem, I think the current system architecture would make it quite difficult. The note canvas item would need to be entirely redesigned.


# Experiments and Results

This chapter focuses on experiments we performed. We will first describe the training and evaluation data. How it was chosen, where it comes from and in the case of evaluation data, also the manual annotation process. Then we will talk about the symbol error rate (SER), a metric used for evaluation, as well as additional metrics we propose to understand mistakes our model makes. We will desribe the training and evaluation process in detail and provide values for all hyperparameters. We will describe setup for each experiment and the explore the results from many perspectives. Finally, we will compare our results to the results in the HMR baseline article (*link*).


## Training data

Before we can talk about experiments, we have to explain what the training data looks like. In the [chapter 1](#1) we talked about the network architecture. The model takes an image as the input and produces a sequence of annotation tokens. [Chapter 2](#2) describes how these annotation tokens encode the music in an image. Now we just need to obtain enough pairs of image and annotation to train on.

The [thesis introduction](#intro) stated that the only available dataset is CVC-MUSCIMA (*link*). This dataset contains 1000 images of handwritten sheets of music, consisting of 20 pages, each written by 50 writers. Because of this lack of variability the dataset cannot be used as-is. In [chapter 3](#3) we described our Mashcima engraving system. This system can produce an image of one staff, that corresponds to a given Mashcima annotation. It does that by rendering musical symbols present in CVC-MUSCIMA, which in turn were extracted as part of the MUSCIMA++ dataset (*link*).

We have a system, that can create images for given annotations. All we need to provide are those annotations.


### PrIMuS incipits

The 20 pages of CVC-MUSCIMA contain this information. The problem is that there is only 20 of them. We ideally need thousands of annotations to account for all the variability in note types and pitches our encoding can capture. Luckily, PrIMuS dataset (*link*) contains exactly what we need. PrIMuS contains over 87 000 incipits of monophonic music. An incipit is the recognizable part of a melody or a song. The incipits have ideal length of a few measures. It's not an entire staff, but not a few symbols either. Also all the incipits are encoded in many formats, but most importantly they are encoded in the agnostic format, that is very simmilar to the Mashcima encoding.

We can take the PrIMuS dataset, engrave all the incipits using Mashcima and train on the result. The only obstacle is converting PrIMuS agnostic encoding to Mashcima encoding.

Converting PrIMuS agnostic encoding to Mashcima encoding is mostly a one-to-one mapping of tokens. Pitches have to be encoded differently, tokens have different names. In PrIMuS, all tokens have pitch information, so for some tokens, it gets stripped away.

Some incipits, however, need to be filtered out. PrIMuS contains symbols, that aren't present in CVC-MUSCIMA, therefore cannot be engraved. These symbols are very long or very short notes (longa, breve, thirty-second). PrIMuS also contains many grace notes and simmilar symbols that the Mashcima engraving system cannot render, so they get removed. There are a couple of other rules and checks that make the conversion slightly more complicated. The exact code for the conversion can be found in the file `mashcima/primus_adapter.py`.

When the conversion finishes, we are left with 64 000 incipits we can use to train on.

    image of a primus incipit printed and mashcima engraved side-by-side
    with mashcima encoding tokens

The advantage of this training data is that the music in it comes from the real world. This allows the model to pick up common patterns and possibly learn the language model.


### Synthetic incipits

The other option we have is to just simply randomize the training annotations, to create some synthetic data. We throw away the possibility of learning a language model, but we get a different benefit. We can artificially boost frequencies of tokens that appear lass frequently in the real world. This will cause the model to make fewer mistakes on uncommon symbols.

Randomization seems simple at first, but it can be done in many ways. At one extreme, we can simply randomly choose tokens from the vocabulary. This, however, produces sequences that cannot be rendered and are nonsensical. Beamed notes have to have a beginning and an end. We cannot have an unfinished or non-started beam. At another extreme, we can try to mimic the language model by using a lot of rules.

We opted for something in the middle. We make sure, that the synthetic annotation can be engraved, but we don't ensure anything more. Duration per measure is not correct, pitch is almost random, time signatures can be in the middle of a measure. The resulting image looks nothing like what we are used to seeing in sheet music. The code for generating synthetic annotations can be found in file `app/generate_random_annotation.py`.

    image of a synthetic staff, with annotation

We will compare these two approaches later in the experiments. It may come as a surprise, but the best approach will be to combine both synthetic and real-world data, effectively training on both.


## Evaluation data

When we faced the lack of training data, we resorted to data augmentation. We cannot do that for evalution, because the evaluation data should be as close to the real-world as possible. Therefore using a well established dataset it the only option.

By looking at the *Collection of datasets for OMR* by Alexander Pacha (https://apacha.github.io/OMR-Datasets/) we can see that most existing datasets are for printed music. If we focus on the handwritten datasets, most of those contain only muscial symbols, not entire staves. When we filter those out, what remains is CVC-MUSCIMA (*link*), MUSCIMA++ (*link*) and Baró Single Stave Dataset (http://www.cvc.uab.es/people/abaro/datasets.html). We are already familiar with the first two datasets, since we used them for training. The last dataset is also derived from CVC-MUSCIMA and it is used in the paper for HMR baseline (https://www.sciencedirect.com/science/article/abs/pii/S0167865518303386?via%3Dihub). We will compare our results to the results in the paper in section [x.y.z](#x.y.z).

We decided to evaluate on a portion of the CVC-MUSCIMA dataset. Partly because it is the only dataset available for this purpouse, partly because other people use it for evaluation as well. To learn more about the CVC-MUSCIMA dataset, see the section [related-work x.y.z](#xyz).

The fact that we devised custom encoding means we have to annotate the evaluation data manually. This is not very difficult, because the evaluation set need not be large. It also means the resulting annotations are of high quality and follow the rules of the Mashcima encoding.

We cannot use the entire CVC-MUSCIMA dataset for evaluation, because we already use it for training. Therefore we need to decide what portion is going to be used for evaluation. We definitely need to evaluate on data from different writers than those we train on. This is because seeing the specific writer's handwriting style might help the model score higher during evaluation. Avoiding specific music pages is not necessary, since the data augmentation process completely destroys any rythmic or melodic information. The Mashcima engraving system samples individual symbols, ignoring their placement relative to other symbols in the staff. So the primary concern is to separate writers used for evaluation.

There are additional criteria for selecting the evaluation writers. We want the writer selection to be diverse in terms of handwriting style. Some writers have very clean handwriting, some not so much. Noteheads can be little circles, ellipses or even little dashes. Some writers have note stems slanted, some have straight, vertical stems. Also the width and spacing of symbols differ.

We also want to evaluate on pages that are present in MUSCIMA++. This is because pages in MUSCIMA++ have a lot of additional information available and there exist detailed MusicXML transcriptions for them. Both of these facts may become useful in the future. Each writer has 20 music pages in CVC-MUSCIMA, but only 2 or 3 in MUSCIMA++. Additionally, not all pages can be represented in the Mashcima encoding (some are polyphonic or have multiple voices).

First we sorted the 20 pages by how easily they can be encoded using Mashcima encoding. This sorting is not perfect, the main goal is to separate pages that we cannot encode at all. Some symbols can be encoded, but since the engraving system cannot render them, they are considered slightly problematic. See the section on extending mashcima encoding (*link*).

| Page | Acceptable | Notes                                                |
| ---- | ---------- | ---------------------------------------------------- |
| 03   | Yes        | perfect                                              |
| 12   | Yes        | perfect                                              |
| 02   | Yes        | trills, grace notes                                  |
| 11   | Yes        | `?` token                                            |
| 09   | Yes        | `?` token, fermata                                   |
| 05   | Yes        | trills                                               |
| 01   | Yes        | triplets, fermata, rests in beamed groups            |
| 13   | Yes        | `?` token                                            |
| 14   | Yes        | chord, triplets                                      |
| 17   | Yes        | two staves with chords                               |
| 15   | Yes        | rests in beamed groups                               |
| 16   | Yes        | beamed notes with empty noteheads, accents           |
| 06   | Not ideal  | trills, many grace notes                             |
| 04   | Not ideal  | tenuto, triplets, nested slurs, bar repeat, fermata  |
| 18   | Not ideal  | two staves with chords                               |
| 07   | No         | trills, many concurrent notes                        |
| 08   | No         | grace notes, unsupported symbols, two voices in bass |
| 20   | No         | chords in many places                                |
| 10   | No         | chords                                               |
| 19   | No         | multiple voices                                      |

> All pages of CVC-MUSCIMA sorted by how easily they can be represented using the Mashcima encoding.


Then we took all the acceptable pages and found all writers for those pages that are present in MUSCIMA++. We sorted those writers by the number of pages that satisfied our selection.

| Pages | Writer | Handwriting style                               | Selected |
| ----- | ------ | ----------------------------------------------- | -------- |
| 4     | 49     | worse, dash noteheads                           | Yes      |
| 3     | 06     | nice, round noteheads                           | No       |
| 3     | 13     | regular, round noteheads                        | Yes      |
| 3     | 20     | regular, dash noteheads                         | Yes      |
| 3     | 27     | nice, round noteheads                           | No       |
| 3     | 34     | regular, round noteheads, slanted               | Yes      |
| 3     | 41     | beautiful, round noteheads                      | Yes      |

> Table shows the final writers that were considered to be selected for evaulation.

All the remaining writers had only two or less pages from the selection. We took 5 writers out of those 7 writers manually, to keep the handwriting diversity high.

Lastly we wanted to compare our results with the results of *From Optical Music Recognition to Handwritten Music Recognition: A baseline* (*link*), so we added the writer 17. The final writer and page selection can be seen in the table:

| Writer | Pages          |
| ------ | -------------- |
| 13     | 02, 03, 16     |
| 17     | 01             |
| 20     | 02, 03, 16     |
| 34     | 02, 03, 16     |
| 41     | 02, 03, 16     |
| 49     | 03, 05, 09, 11 |

We end up with 6 writers, 17 pages (7 distinct), 115 staves and over 5840 tokens. Annotations for these pages can be found in the file `app/muscima_annotations.py`. These annotations have been performed by me - the author of this thesis. Experience regarding the annotation process is described in the [following section](#123).

Lastly we want to show a frequency table of the most common tokens in the evaluation dataset. The table contains generic variants of the tokens. Table containing common pitches is the very next table.

    table of generic tokens

    table of pitches


### Manual annotation experience

Although the Mashcima encoding attempts to not be ambiguous, there were some places where I had to make some decisions regarding undefined situations. This section goes over these situations.

**Page 1:** The last three measures contain nested slurs. These cannot be represented, so I chose to represent slur beginnings and slur endings as they can be seen in the page. One note cannot have two slur beginings, so only one is annotated. The very last slur is maybe not a slur, but some pitch articulation symbol. I annotated it as a slur continuing onto the next staff.

    image

**Page 2:** The last two staves contain three occurences of grace notes. They look like regular notes, but are smaller. Grace notes cannot be represented yet, so I replaced them with a `?` token. I replaced the entire grace note group (two sixteenths with a slur) with a single `?` token.

    image

**Page 9:** There are two measures with notes playing at the same time. The first three half notes are slightly offset, so they are annotated from left to right. The last two quarter notes are right above each other, so I replaced them with the `?` token. I wanted to place at least one `?` token inside the measure and then tried to annotate the rest as best as I could. This way the measure is marked and can be repaired in the future.

    image

**Page 11:** One measure has the same problem as page 9.

**Page 16:** Third staff contains a bracket symbol in the key signature. The bracket symbol is completely ignored, but the clef and key signature is annotated as usual. The fifth staff contains double-beamed notes with empty noteheads. These are not sixteenth notes, but since they look so simmilar, I annotated them as such. These symbols are not very common and the trained model treated them as sixteenth notes as well, so I kept it that way.

    image

Special thick barlines, double barlines or barlines with braces at the begining of a staff are all annotated as simple `|` token. The only exception are repeat signs that do have their corresponding tokens.

There are many trills or accents throughout the pages. Those are not in the training data, but can be represented, so they are annotated just as defined in the chapter on Mashcima encoding.


## Evaluation metrics

Now that we have a model producing some token sequences and we have our gold sequences, we need a way to measure the model performance. There are basically three goals for these measurements:

- Compare the model against itself to track improvements.
- Get an overall idea of the model performance and compare it to other works.
- Analyze model output to identify common mistakes it makes.

Looking at the work by Calvo-Zaragoza and Rizo (*link*) or the HMR baseline article (*link*) we can see, that the metric they use is Symbol Error Rate (SER). This metric is also known as normliazed Levenhstein distance or edit distance. The name Symbol Error Rate is used in contrast to Word Error Rate (WER) in the text recognition community. Since we don't work with text, we are left with the Symbol Error Rate only.

Regular Levenhstein distance (https://ui.adsabs.harvard.edu/abs/1966SPhD...10..707L/abstract) is defined as the minimum number of single-character edits that turn our prediction into the gold sequence. We don't work with strings, so we use tokens instead of characters. The basic edit operations are insertion, deletion and substitution. The lower this number, the better. Zero means perfect match.

This metric has to be normalized by the length of gold sequence in order to allow for averaging over multiple values. Normalized Levehnstein distance produces a number that is typically between 0 and 1, where 0 means the sequences was predicted perfectly and 1 means the sequence is entirely wrong. The normalized distance can be greater than 1, when the predicted sequence is much longer than the gold one, but that happens only when the model is completely useless.

    SER = lev_normalized = \frac{#insertions + #deletions + #substitutions}{gold_length}

Since this metric is also used by other works, we will use it for comparison against these works.

When training, we will use the edit distance function implemented in the Tensorflow library (http://tensorflow.org/). Although it is claimed to be the normalized Levenhstein distance, the implementation is different to the one used during evaluation. Therefore these two values should not be compared directly. The training edit distance is only meant for tracking the learning process a determinig the stopping condition.


### Understanding model mistakes

We would like to get an idea on the kind of mistakes our trained model makes. The [chapter 2](#2) talks about the Mashcima encoding and how it is able to represent symbols that it cannot yet represent (by the `?` token). Having this `?` token in the gold data creates an ever present mistake, that increases our error rate. We would like to get an estimate of how much of the overall error is contributed by such symbols. Also note that `?` is not the only token the model cannot produce. There are symbols that cannot be engraved yet, like trills, accents or fermatas. Being able to measure the error these tokens contribute would give us an idea on how much the model could improve, if we implemented these symbols in the engraving system.

During evaluation, we will take the prediction and remove certain tokens from it. These same tokens will be removed from the gold sequence as well. We will compute the error of these simplified sequences. Comparing this error to the baseline error should tell us how much the removed tokens contribute to the baseline error.

The metric used for computing this error will be the Levenhstein distance, but normalized by the number of *imporatnt tokens* in the gold sequence. An *important token* is a token that will never be removed. It can be altered, but not removed. This will make sure the normalization term stays constant over all the possible transofrmations and thus all the error values should be comparable.

*Important tokens* are notes, rests, barlines, clefs, accidentals and other simmilar tokens. What remains as non-important are slurs, ornaments and the `?` token. The specific list of important tokens can be found in the file `app/vocabulary.py`. We will call this metric Important Token Error Rate (ITER). Remember that this metric should not be used for comparison against other models using different encodings. It is purely to get an idea of what mistakes contribute to the Symbol Error Rate.

With this metric we propose a set of transformation functions that progressively simplify the sequences:

- *ITER_RAW* - No transformation is applied, corresponds to SER, but normalized by the number of important tokens.
- *ITER_TRAINED* - Tokens that the model hasn't seen during training are removed (`?` token, trills, fermatas, etc.).
- *ITER_SLURLESS* - Like the above, but slurs are removed as well (`(`, `)`).
- *ITER_ORNAMENTLESS* - Like the above, but most of the non-important attachments are removed (trill, accent, staccato, fermata, ...). What has to remain are accidentals and duration dots. Those are important for correct pitch and rythm.
- *ITER_PITCHLESS* - Like the above, but all pitch information is removed by converting all tokens to their generic variant.

Each metric builds on the previous one, further simplifying the sequences. This means the error rate should decrease as we go down. The amount by which it decreases can tell us how much the given transformation affected the error, therefore how much the removed tokens contributed to the error rate.

Also please understand, that all these errors are computed on a single trained model. The gold sequence is modified during evaluation. Not during training. We are trying to understand a specific model we have.


## Architecture, training and evaluation

In [chapter 1](#1) we provided a short introduction to deep neural networks and described the RCNN architecture. We will use this architecture in the following experiments. Here is the list of layers, used in the neural network:

    tabulka s vrstvama sítě a jejich parametrama

The Mashcima engraving system works with images at the resolution of the CVC-MUSCIMA dataset. Image of an engraved staff is about 400px in height and the width varies from 500px to over 2000px. The neural network however requires the input image to be exactly 64px in height. The image will be scaled down because of this, while preserving its aspect ratio.

There will be two datasets used for training. One for the actual training - a *training dataset* and one for validation - a *validation dataset* (or "dev dataset"). The training dataset is fed into the model in batches and each batch is used to perform update of the learned parameters of the model. This process is called stochastic gradient descent (*link*). Using the entire training dataset once is called *one epoch*. The validation dataset will be used after each epoch to estimate the true performance of the model (to estimate the generalization error). Edit distance will be measured during training and validation and it will be used to track the learning progress.

Learned parameters will be updated by the adaptive learning rate optimizer (Adam) (*link*), that comes with Tensorflow (*link*), with the default parameters:

| Parameter     | Value     |
| ------------- | --------- |
| Learning rate | 0.001     |
| $\beta_1$     | 0.9       |
| $\beta_2$     | 0.999     |
| $\varepsilon$ | $10^{-8}$ |

We have not tried to fine tune these parameters or any other hyperparameters. Our goal was to try training on engraved handwritten images and see whether this approach is even feasible. Tuning hyperparameters is one of the places where our approach can be improved in the future.

The training will run for a given number of epochs. In each epoch an average symbol error rate on validation dataset is recorded. The final trained model is the model, that had the lowest validation symbol error rate, during the whole training. If the number of epochs trained is sufficiently high, this method should return the model at the point, where the generalization error began to rise. Also note that the symbol error rate here is the edit distance function from Tensorflow. It is a diffenrent implementation of SER, than the one used for evaluation.

During evaluation, the beam search decoding algorithm is used with the beam width of 100 (https://arxiv.org/pdf/1601.06581.pdf). There are two additional steps performed after that. Firstly the produced token sequence is repaired. This means the rules regarding beamed notes are checked and corrected and attachment tokens are sorted properly. This repairing process is relatively simple and completely rule-based. For the details see the `repair_annotation` function inside `app/vocabulary.py`. After the repairing process, leading and trailing barlines are stripped from both gold data and the prediction. This is because barlines at the beginning and at the end of staff convey no additional meaning. It is analogous to trimming whitespace characters around a sentence. Barlines with repeat signs are not stripped away, since they are important.


## Experiments

In the section on [training data](#td) we hypothesized some differences between training on PrIMuS incipits and synthetic data. The main idea is that training on PrIMuS incipits should allow the model to learn the language model. More generally training on real-wold music samples should help the model, since it will be evaluated on real-world music in the CVC-MUSCIMA dataset. Training on synthetic data should allow the model to learn complicated combinations of symbols, that are not as common in the real-world music.

To test this hypothesis we propose a set of four experiments:

| Experiment | Training data                                     | Validation data          |
| ---------- | ------------------------------------------------- | ------------------------ |
| 1          | 63 000 PrIMuS incipits                            | 1 000 PrIMuS incipits    |
| 2          | 63 000 synthetic incipits                         | 1 000 synthetic incipits |
| 3          | 31 500 PrIMuS incipits, 31 500 synthetic incipits | 1 000 PrIMuS incipits    |
| 4          | 63 000 PrIMuS incipits, 63 000 synthetic incipits | 1 000 PrIMuS incipits    |

First experiment trains a model on real-world incipits, second uses synthetic incipits and the third one combines both approaches in a 1:1 ratio. The last experiment validates on real-world incipits, since the evaluation will also be performed on real-world music. The second experiment validaates on synthetic incipits, because we wanted to simulate a scenario where we don't have access to real-world incipits. The fourth experiment is the same as the third one, only utilizing the whole PrIMuS dataset as is available to us.

We trained each experiment for 20 epochs (except for the fourth that has been trained for only 10 epochs) and took the model with the lowest edit distance, averaged over the validation dataset.

    graphs of the validation & training edit distances from the tensorboard


## Results

Here are the resulting symbol error rates, averaged over the entire validation dataset:

| Experiment | Symbol error rate |
| ---------- | ----------------- |
| 1          | 0.34              |
| 2          | 0.28              |
| 3          | 0.26              |
| 4          | 0.25              |

It seems that training on synthetic data is better than training on real-world data. But looking at the experiment 3, we see that the best approach is to combine both approaches. Synthetic data is probably better than real-world data simply because all the tokens are represented equally. The discussion on language model is more complicated and is explored [in a separate section](#123). The experiment 4 is slightly better then the experiment 3, because it has twice as much data to train on.

In [section xyz](#xyz) we proposed a set of metrics, intended to give us insight into the mistakes the model makes:

| Experiment | ITER_RAW | ITER_TRAINED | ITER_SLURLESS | ITER_ORNAMENTLESS | ITER_PITCHLESS |
| ---------- | -------- | ------------ | ------------- | ----------------- | -------------- |
| 1          | 0.44     | 0.42         | 0.30          | 0.26              | 0.21           |
| 2          | 0.37     | 0.34         | 0.28          | 0.25              | 0.17           |
| 3          | 0.34     | 0.32         | 0.24          | 0.21              | 0.16           |
| 3          | 0.33     | 0.31         | 0.23          | 0.21              | 0.16           |

When we compare the *ITER_RAW*, *ITER_TRAINED* and *ITER_SLURLESS*, we can see that reducing our focus to only trained tokens helps slightly, although it's not as big of an impact as we expected. Considerably larger difference happens when we remove slur tokens. This confirms, what can be seen by looking manually at the predictions the model makes. There are a lot of mistakes related to slur classification. This might be caused by the fact that the engraving system does not capture all the variability that exists in the real world with regards to slur engraving.

In a previous [section on evaluation](#xyz) we mentioned, that the prediction, before being evaluated, is repaired by a few rules (attachment sorting, barline trimming). The following table shows how much impact does the repair have on the error rate:

| Experiment | Raw SER | Repaired prediction SER |
| ---------- | ------- | ----------------------- |
| 1          | 0.34    | 0.34                    |
| 2          | 0.28    | 0.28                    |
| 3          | 0.26    | 0.26                    |
| 4          | 0.25    | 0.25                    |

You can see, that there's almost no difference. The repairs were indeed disabled, its just that the performance difference was so minor, that the resulting average is the same.

Now that we know the experiment 4 performed the best, we will take a closer look at it. Here is a table of metrics for each evaluation page (averaged over all staves in that page):

| Page | Writer | SER  | ITER_RAW | ITER_TRAINED | ITER_SLURLESS | ITER_ORNAMENTLESS | ITER_PITCHLESS |
| ---- | ------ | ---- | -------- | ------------ | ------------- | ----------------- | -------------- |
| 2    | 13     | 0.16 | 0.18     | 0.17         | 0.17          | 0.14              | 0.12           |
| 3    | 13     | 0.12 | 0.13     | 0.13         | 0.07          | 0.06              | 0.04           |
| 16   | 13     | 0.30 | 0.42     | 0.40         | 0.33          | 0.27              | 0.21           |
| 1    | 17     | 0.28 | 0.37     | 0.31         | 0.26          | 0.23              | 0.16           |
| 2    | 20     | 0.26 | 0.32     | 0.30         | 0.27          | 0.24              | 0.14           |
| 3    | 20     | 0.11 | 0.12     | 0.12         | 0.07          | 0.06              | 0.05           |
| 16   | 20     | 0.32 | 0.48     | 0.44         | 0.27          | 0.22              | 0.15           |
| 2    | 34     | 0.28 | 0.34     | 0.32         | 0.29          | 0.24              | 0.15           |
| 3    | 34     | 0.06 | 0.07     | 0.07         | 0.03          | 0.03              | 0.02           |
| 16   | 34     | 0.34 | 0.49     | 0.47         | 0.35          | 0.29              | 0.19           |
| 2    | 41     | 0.23 | 0.27     | 0.25         | 0.24          | 0.22              | 0.14           |
| 3    | 41     | 0.14 | 0.16     | 0.16         | 0.07          | 0.07              | 0.06           |
| 16   | 41     | 0.28 | 0.41     | 0.37         | 0.29          | 0.23              | 0.14           |
| 3    | 49     | 0.29 | 0.33     | 0.33         | 0.24          | 0.24              | 0.21           |
| 5    | 49     | 0.24 | 0.26     | 0.25         | 0.21          | 0.21              | 0.18           |
| 9    | 49     | 0.42 | 0.61     | 0.59         | 0.36          | 0.35              | 0.33           |
| 11   | 49     | 0.50 | 0.67     | 0.67         | 0.50          | 0.48              | 0.44           |

We can do an average for each writer and compare the results to the style of their handwriting:

| Writer | SER  | Handwriting style                               |
| ------ | ---- | ----------------------------------------------- |
| 13     | 0.19 | regular, round noteheads                        |
| 41     | 0.22 | beautiful, round noteheads                      |
| 34     | 0.23 | regular, round noteheads, slanted               |
| 20     | 0.23 | regular, dash noteheads                         |
| 17     | 0.28 | regular, round noteheads                        |
| 49     | 0.36 | worse, dash noteheads                           |

The first four writers are very much comparable, but the writer 49 has the worst handwriting of all the writers an he ended up last, as expected.

Similarly, we can average over each page:

| Page | SER  | Notes                                                |
| ---- | ---- | ---------------------------------------------------- |
| 3    | 0.14 | perfect                                              |
| 2    | 0.23 | trills, grace notes                                  |
| 5    | 0.24 | trills                                               |
| 1    | 0.28 | triplets, fermata, rests in beamed groups            |
| 16   | 0.31 | beamed notes with empty noteheads, accents           |
| 9    | 0.42 | `?` token, fermata                                   |
| 11   | 0.50 | `?` token                                            |

Pages 9 and 11 ended up last, because they are only present for writer 49, who ended up as the worst writer. Page 3 is very interesting. It is the only page, that can be fully encoded using Mashcima encoding and all the smybols it contains can be engraved using the Mashcima engraving system. It is, however, also the simplest page in that it does not contain any complicated expressions and contains only a few slurs. This is supported by the fact that page 5 ended up with also very low error and the page 5 is very much comparable in its layout and complexity to the page 3.


### Language model

When comparing results of training on real-world data vs. synthetic data, it is strange that pure synthetic data outperforms purely real-world data. But it probably has to do with the fact, that the synthetic dataset is balanced with respect to the individual output class abundance. The learned language model of real-world data helps the first experiment, but it's not nearly enough to beat the benefits of a balanced dataset for the second experiment.

This idea is supported by the fact that the third experiment beats both of the first two. It can benefit from both a balanced dataset and from learning a language model.

The experiment 3 does indeed learn a basic language model. When I was annotating the evaluation dataset I used a trained model from experiment 3 and I noticed, that if often made mistakes in beamed note groups. Especially for the writer 49. It classified the first note of a beamed group as a quarter note. But then it (incorrectly) classified the second note as a beam start note, even though it can be easily seen the beam runs to both sides of the note. It prefered a well-formed beam, rather then the correct token. This property can be learned even from synthetic data, since they contain well-formed beams only.

    image of a misclassified first eight as quarter note
    predicted: ...
    gold: ...
    expected without language model: ...

Then there are couple of places where it correctly predicts key signature, even though an accidental is misplaced by the writer. In a key signature, the number and type of accidentals
uniquely identifies, what pitches those accidentals have. For example, when there's only a single sharp, it always corresponds to an `F#` note. Combining this with a specific clef gives us a correct position for the sharp.

    find image of that place with comparison of individual experiment predictions
    (01 correct (hopefully), 02 wrong (hopefully), 03 correct)


## Comparison to other works

We wanted to make a comparison against the HMR baseline article (*link*), because our evaluation datasets overlap. Specifically, we share the page 3 for writer 13 and the page 1 for writer 17. We both use the symbol error rate metric, although there are many differences that need to be addressed. Their model classifies rythm and pitch separately, so both error rates are provided. There is also a combined error rate that treats the output symbols similar to our Mashcima encoding - having pitch and rythm in one token (this number should be analogous to ours). The last column shows our error rate, given by the experiment 4.

| Page  | Writer | Rythm SER | Pitch SER | Rythm + Pitch SER | Our SER |
| ----- | ------ | --------- | --------- | ----------------- | ------- |
| 1     | 17     | 0.528     | 0.349     | 0.592             | 0.28    |
| 3     | 13     | 0.226     | 0.175     | 0.270             | 0.12    |

You can see, that our model has much smaller error rate, but we have to consider this result carefully. Their model does not use the CTC loss and the output encoding is very different. While our model might output a sequence of length 50, their model produces sequence of the same length as the width of the input image, that is in the order of hundreds to a thousand sequence items. Also their encoding requires perfect alignment. If the model transitions between output classes at slightly different time-steps then the gold data, it produces a lot of error, even though when collapsed, the resulting sequence is the same. And given the temporal resolution, this might contribute a lot.

More fair comparison would be a qualitative one. Luckily the paper provides qualitative comparison of one staff from the page 3 of their model against a commercial software called PhotoScore (https://www.neuratron.com/photoscore.htm). We can add a prediction by our model and compare all three. Note that the image has been produced by manually engraving the predicted Mashcima annotation.

    image containing the qualitative comparison p03 w13

You can see, that the difference is not as pronounced, although this staff is one of the simpler ones. There is, however, also a qualitative comparison on a staff from the page 1:

    image containing the qualitative comparison p01 w17

TODO: comment the second qualitative comparison

It should also be noted, that each model uses different input resolution. The model from HMR article normalizes to height of 100 pixels, whereas ours normalizes to only 64 pixels. This might be a disadvantage to us. Also our model cannot read chords by design, but theirs can. This might very well be required for some task and it would make our model unusable. Their model can also detect presence of dynamics and text.


## Evaluating on Printed PrIMuS incipits

We also wanted to try, how would our model perform on printed music. Models by other people are often pre-trained on printed music and then fine-tuned on handwritten images via transfer learning. Ours is different in that it has never seen an image of printed music. We already have code for parsing PrIMuS dataset and since the dataset contains images as well, we will use those. We just slightly preprocessed the images - inverted them, normalized and slightly scaled down to have dimensions comparable to what our model trained on. We used the model from experiment 4 since it performed the best. The evaluation was performed on 100 incipits that the model hasn't seen during training and these are the results:

| SER  | ITER_RAW | ITER_TRAINED | ITER_SLURLESS | ITER_ORNAMENTLESS | ITER_PITCHLESS |
| ---- | -------- | ------------ | ------------- | ----------------- | -------------- |
| 0.61 | 0.64     | 0.64         | 0.60          | 0.59              | 0.56           |

You can see, that the performance is not very impressive. We did expect the error rate to be high, but not that high. Although, it is understandable, because the printed music is very different to the handwritten. It would be interesting to also train on printed images in the future. This error rate would go down, but maybe the CVC-MUSCIMA error rate would go down as well.

    image of a printed staff and the prediction and the gold
    + maybe the same staff, engraved using Mashcima

Also note that *ITER_RAW* and *ITER_TRAINED* have the same value. This is expected, because we filter out incipits that cannot be engraved by Mashcima.


# Conclusion and Future Works

> - anotace a generátor:
>   - rozšíření barlines (:|: |: :|, ||) a spoustu dalších symbolů (trill, fermata)
>   - rozšíření na dynamiku (mf, ff, pp, hairpins, ...)
>   - rozšíření na akordy
>   - rozšíření na text kolem not (kvůli regularizaci), e.g. "andante", "T=180", ...
> - použít úplně jinačí model - zkombinovat baseline paper a můj generátor
> - nebo vypiplat generátor a postavit na jeho základě novej dataset


# Appendix

## Conversion table between PrIMuS agnostic and Mashcima encoding

> - describe the issues faced
> - generic conversion table
> - link code that does the conversion

<!--
    TODO: describe all the parameters of Mashcima engraving system
        (where randomness occurs)
-->
