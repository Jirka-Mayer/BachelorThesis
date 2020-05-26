# Some Links

Medvěd: https://mj.ucw.cz/vyuka/bc/

Hajič Jr. thesis proposal: http://ufal.mff.cuni.cz/~zabokrtsky/pgs/thesis_proposal/jan-hajic-jr-proposal.pdf
A Starting Point for Handwritten Music Recognition: https://openreview.net/pdf?id=SygqKLQrXQ
From Optical Music Recognition to Handwritten Music Recognition: A baseline: https://www.sciencedirect.com/science/article/abs/pii/S0167865518303386
Handwritten Music Recognition for Mensural notation with convolutional recurrent neural networks: https://www.sciencedirect.com/science/article/abs/pii/S0167865519302338

HTR (TU Wien): https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742


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


## Thesis outline

**Chapter X:** Proč end-to-end, proč RCNN+CTC, výhody, nevýhody, viz log - proces vymýšlení, vícekanálová CTC, problémy

**Chapter X:** Reprezentace výstupu sítě (Mashcima representation)

**Chapter X:** Engraving system Mashcima, jak funguje, jakou má strukturu

**Chapter X:** Experiments and results (jak vypadají experimenty, jak dopadly)


# Related Work

> TODO ... vypiš hlavní práce o které se opíráš a co zajímavého z nich používáš.

- SimpleHTR
- Calvo-Zaragoza and Rizo, PrIMuS
- CVC-MUSCIMA
- MUSCIMA++
- HMR Baseline paper


# Deep Neural Network

<!--
> Tradiční systémy používají pipeline

> deep NN spojují celou pipeline do jednoho celku, learned features

> CTC umožňuje neřešit alignment, snazší anotace

> konkrétní architektura mojí sítě (tabulka) + hypotéza o dropout vrstvě
-->

This chapter describes the specific model we decide to use for our OMR task. It discusses traditional methods and how deep neural networks help us simplify the process. It describes models other people used for similar tasks and how we've been influenced by them.


## Traditional approaches

A musical score intended for OMR typically begins as a raster image. This image is a photo or a scan of a real-world sheet of paper. The image needs to be prepared first. We need to find the sheet of paper in the image and correct any rotation or perspective distortion. Scanned images are easier to prepare, because they don't contain any perspective deformation and lighting artifacts. Searching for the paper in the image can be performed using many approaches, e.g. by using maximally stable extremal regions (http://cmp.felk.cvut.cz/~matas/papers/matas-bmvc02.pdf). We can detect stafflines using probabilistic Hough transform (https://en.wikipedia.org/wiki/Hough_transform). We can then use this information to remove any affine distortion of the image.

Next step is performing some color normalization and binarization. There might be a light-intensity gradient over the image, so we do some automatic contrasting to bring the lightness to a constant level across the image. Median filtering can be applied to remove noise (https://www.uio.no/studier/emner/matnat/ifi/INF2310/v12/undervisningsmateriale/artikler/Huang-etal-median.pdf). Conversion to grayscale image is often used, since color is not useful for OMR. The image can then be binarized to further remove unnecessary information. There are many thresholding algorithms that can be used for this step, many of which are implemented in the OpenCV library (https://opencv.org/). Binarization is important for traditional approaches, since they often use methods based on connected components to detect individual symbols. Neural networks could benefit from non-binarized images, since binarization can create aliasing artifacts that distort the input image on pixel level.

The steps described above are shared by both traditional and neural network based approaches. Traditional approaches now usually perform staffline removal. This step lets methods based on connected components to become useful. Staff localization may be an important part of this step. Symbols then need to be segmented and classified separately. Meaning is then reconstructed by looking at the relationships between all the classified symols. With the musical score understood at the symbol level, the extracted information can be converted to some final representation (MusicXML, MEI, MIDI).


## Deep learning approaches

Deep learning is a class of machine learning that focuses on deep neural networks. Deep learning has risen over the past two decades and became a very powerful tool for solving many problems, especially classification problems regarding computer vision. Neural networks can be used in many places throughout the pipeline of a traditional OMR system. They can be used for staffline removal (https://link.springer.com/article/10.1007/s00138-017-0844-4), symbol classification (http://mipal.snu.ac.kr/images/3/3b/ICISS_MuSymb.pdf) or even symbol detection (https://hal.archives-ouvertes.fr/hal-01972424/document).

Recently, neural networks have been used to tackle the problem of OMR in an end-to-end fashion (*link primus, link HTR baseline*). This approach allows us to replace many stages of the pipeline with a single model. The input sheet of music is usually processed staff by staff, so an intial segmentation of staves is required. This step is, however, very robust and can be performed reliably.

Main steps unified by an end-to-end system are segmentation, symbol classification and part of the relationship extraction. This means we don't need to explicitly specify structure of this part of the pipeline, which saves a lot of time and thinking. Also any intermediate features that would be extracted (like noteheads) need not be specified. The deep neural network has the ability to learn, what those features are. Moreover it can adapt these features to the problem better than a human could.

Deep learning, especially in an end-to-end approach also has some drawbacks. The first is bound to the ability of the model to learn the solution from data. While it's very helpful, that we don't have to desing part of our OMR system manually, it's often very difficult to acquire enough high-quality data for the training. Also the more complex our model is and the more learned paramateres it has, the more training data it requires. The data also needs to be high quality. Ambiguity and mistakes in annotations lead to poor performance of the resulting model. The trained model can only ever be as good as it's training data.

The second drawback is the very difficult nature of debugging the model. Neural network is by design a black box and we cannot easily assign specific meaning to any of its internal parts. The process of fixing a mistake the model makes is tedious and requires a lot of experimentation and re-training.


# Music Representation

<!--
    - Inspirováno Primusem, ale drobné změny
    - proč agnostic a ne semantic
        - menší abeceda, jednodušší generátor mashcima
    - míň ukecaný než u primusu, aby se dalo lépe anotovat ručně - vizuelní podobnost
    - symetrické - pozice 0 je uprostřed
    - Co se generuje vs. co lze anotovat
    - Pitch information
    - Attachments
    - Jak lze rozšířit do budoucna (dynamika, akordy) ... tohle ale spíš do závěru tady jen odkaz
-->

This chaptes explores how the music is represented within this thesis. It looks at the encodings devised for the PrIMuS dataset and how they have been modified to produce our Mashcima music encoding. Then we explore how this encoding can be used for annotating datasets and how it can be extended in the future.

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

The pitch encoding is built such that it would be easy to understand for a non-musician. In western contemporary music notation (**TODO link**) pitch of a note is represented by the vertical position of that note on the staff. An empty staff is composed of 5 stafflines. Mashcima encoding sets the middle staffline position to be zero. Going up, the first space is pitch `1` and the first line is pitch `2`. Going down, the first space is pitch `-1` and the first line is pitch `-2`.

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

<!--gracenotes-->
Special place have gracenotes. They look like little notes, they do not affect the rythm and are considered an ornament attached to another note. PrIMuS agnostic encoding can represent them, but at the expense of adding a lot of additional tokens. We decided not to bloat our vocabulary with symbols that aren't very abundant in the CVC-MUSCIMA dataset. They are present in a few places in the evaluation dataset and are represented by the `?` token.

<!--chords-->
A chord is two or more notes played simultaneously. Currently there is no way of encoding simultaneous notes. Since chords usually share a stem, they could maybe be represented via after attachments. Maybe if we encoded the top-most note of a chord as a regular note and then added one "notehead" token for every remaining note, we could represent a chord. But there are problems with having multiple accidentals. Either way it would be interesting to explore in some future work.

<!--text-->
Text (like lyrics and tempo) is also ignored. It is not encoded by even the `?` token.


# Engraving System

This chapter talks about the Mashcima engraving system. Why we developed this system and what problem it solves. How it works, what are its limitations and how it can be extended.


## Why custom engraving system

In the [thesis introduction](#123) we stated that there is only a single dataset containing handwritten staves of music. There are other handwritten music datasets, but they either contain only symbols, or they are derived from CVC-MUSCIMA. Using this dataset as-is for training is not plausible, because it contains far too few symbol combinations.

We are not the first to realise this issue. The HTR baseline paper (*link*) talks about using data augmentation and transfer learning to solve the lack of training data. They propose a model to be trained on printed music, of which there's abundance. After that the model is fine-tuned by training on the CVC-MUSCIMA dataset. The results they obtained are impressive, considering the method they used. To help with the process, they used simple data augmentation, like dilation, erosion and blurring.

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

This chapter describes experiments we performed. These experiments aim to measure performance of our approach and test hypotheses postulated in previous chapters.


## Training data

Before we can talk about experiments, we have to explain what the training data looks like. In the [chapter 1](#1) we talked about the network architecture. The model takes an image as the input and produces a sequence of annotation tokens. [Chapter 2](#2) describes how these annotation tokens encode the music in an image. Now we just need to obtain enough pairs of image and annotation to train on.

The [thesis introduction](#intro) stated that the only available dataset is CVC-MUSCIMA (*link*). This dataset contains 1000 images of handwritten sheets of music, consisting of 20 pages, each written by 50 writers. Because of this lack of variability the dataset cannot be used as-is. In [chapter 3](#3) we described our Mashcima engraving system. This system can produce an image of one staff, that corresponds to a given Mashcima annotation. It does that by rendering musical symbols present in CVC-MUSCIMA, which in turn were extracted as part of the MUSCIMA++ dataset (*link*).

We have a system, that can create images for given annotations. All we need to provide are those annotations.


### PrIMuS incipits

The 20 pages of CVC-MUSCIMA contain this information. The problem is that there is only 20 of them. We ideally need thousands of annotations to account for all the variability in note types and pitches our encoding can capture. Luckily, PrIMuS dataset (*link*) contains exactly what we need. PrIMuS contains over 87 000 incipits of monophonic music. An incipit is the recognizable part of a melody or a song. The incipits have ideal length of a few measures. It's not an entire staff, but not a few symbols either. Also all the incipits are encoded in many formats, but most importantly they are encoded in the agnostic format, that is very simmilar to the Mashcima encoding.

We can take the PrIMuS dataset, engrave all the incipits using Mashcima and train on the result. The only obstacle is converting PrIMuS agnostic encoding to Mashcima encoding.

Converting PrIMuS agnostic encoding to Mashcima encoding is mostly a one-to-one mapping of tokens. Pitches have to be encoded differently, tokens have different names. In PrIMuS, all tokens have pitch information, so for some tokens, it gets stripped away.

Some incipits, however, need to be filtered out. PrIMuS contains symbols, that aren't present in CVC-MUSCIMA, therefore cannot be engraved. These symbols are very long or very short notes (longa, breve, thirty-second). PrIMuS also contains many gracenotes and simmilar symbols that the Mashcima engraving system cannot render, so they get removed. There are a couple of other rules and checks that make the conversion slightly more complicated. The exact code for the conversion can be found in the file `mashcima/primus_adapter.py`.

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
| 02   | Yes        | trills, gracenotes                                   |
| 11   | Yes        | `?` token                                            |
| 09   | Yes        | `?` token, fermata                                   |
| 05   | Yes        | trills                                               |
| 01   | Yes        | triplets, fermata, rests in beamed groups            |
| 13   | Yes        | `?` token                                            |
| 14   | Yes        | chord, triplets                                      |
| 17   | Yes        | two staves with chords                               |
| 15   | Yes        | rests in beamed groups                               |
| 16   | Yes        | beamed notes with empty noteheads, accents           |
| 06   | Not ideal  | trills, many gracenotes                              |
| 04   | Not ideal  | tenuto, triplets, nested slurs, bar repeat, fermata  |
| 18   | Not ideal  | two staves with chords                               |
| 07   | No         | trills, many concurrent notes                        |
| 08   | No         | gracenotes, unsupported symbols, two voices in bass  |
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

**Writer 17, Page 1:** The last three measures contain nested slurs. These cannot be represented, so I chose to represent slur beginnings and slur endings as they can be seen in the page. One note cannot have two slur beginings, so only one is annotated. The very last slur is maybe not a slur, but some pitch articulation symbol. I annotated it as a slur continuing onto the next staff.

    image

**Page 2:** The last two staves contain three occurences of gracenotes. They look like regular notes, but are smaller. Gracenotes cannot be represented yet, so I replaced them with a `?` token. I replaced the entire grace note group (two sixteenths with a slur) with a single `?` token.

    image

**Page 9:** There are two measures with notes playing at the same time. The first three half notes are slightly offset, so they are annotated from left to right. The last two quarter notes are right above each other, so I replaced them with the `?` token. I wanted to place at least one `?` token inside the measure and then tried to annotate the rest as best as I could. This way the measure is marked and can be repaired in the future.

    image

**Page 11:** One measure has the same problem as page 9.

**Page 16:** Third staff contains a bracket symbol in the key signature. The bracket symbol is completely ignored, but the clef and key signature is annotated as usual. The fifth staff contains double-beamed notes with empty noteheads. These are not sixteenth notes, but since they look so simmilar, I annotated them as such. These symbols are not very common and the trained model treated them as sixteenth notes as well, so I kept it that way.

    image

Special thick barlines, double barlines or barlines with braces at the begining of a staff are all annotated as simple `|` token. The only exception are repeat signs that do have their corresponding tokens.

There are many trills or accents throughout the pages. Those are not in the training data, but can be represented, so they are annotated just as defined in the chapter on Mashcima encoding.


## Evaluation metrics

<!--
- we evaluate the output = token sequence against a token sequence
- describe SER = normalized levenshtein
- sketch out the problem of comparison when removing tokens ... "important tokens"
-->

Now that we have a model producing some token sequences and we have our gold sequences, we need a way to measure the model performance. There are basically three goals for these measurements:

- Compare the model against itself to track improvements.
- Get an overall idea of the model performance and compare it to other works.
- Analyze model output to identify common mistakes it makes.

Looking at the work by Calvo-Zaragoza and Rizo (*link*) or the HMR baseline paper (*link*) we can see, that the metric they use is Symbol Error Rate (SER). This metric is also known as normliazed Levenhstein distance or edit distance. The name Symbol Error Rate is used in contrast to Word Error Rate (WER) in the text recognition community. Since we don't work with text, we are left with the Symbol Error Rate only.

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

Evaluation will be performed with the trained model, by feeding in the evaluation images and reading the resulting token sequence. There are, however, two additional steps performed. Firstly the prodced token sequence is repaired. This means the rules regarding beamed notes are checked and corrected and attachment tokens are sorted properly. This repairing process is relatively simple and completely rule-based. For the details see the `repair_annotation` function inside `app/vocabulary.py`. After the repairing process, leading and trailing barlines are stripped from both gold data and the prediction. This is because barlines at the beginning and at the end of staff convey no additional meaning. It is analogous to trimming whitespace characters around a sentence. Barlines with repeat signs are not stripped away, since they are important.


## Experiments

In the section on [training data](#td) we hypothesized some differences between training on PrIMuS incipits and synthetic data. The main idea is that training on PrIMuS incipits should allow the model to learn the language model. More generally training on real-wold music samples should help the model, since it will be evaluated on real-world music in the CVC-MUSCIMA dataset. Training on synthetic data should allow the model to learn complicated combinations of symbols, that are not as common in the real-world music.

To test this hypothesis we propose a set of three experiments:

| Experiment | Training data                                     | Validation data          |
| ---------- | ------------------------------------------------- | ------------------------ |
| 1          | 63 000 PrIMuS incipits                            | 1 000 PrIMuS incipits    |
| 2          | 63 000 synthetic incipits                         | 1 000 synthetic incipits |
| 3          | 31 500 PrIMuS incipits, 31 500 synthetic incipits | 1 000 PrIMuS incipits    |

First experiment trains a model on real-world incipits, second uses synthetic incipits and the third one combines both approaches in a 1:1 ratio. The last experiment validates on real-world incipits, since the evaluation will also be performed on real-world music. The second experiment validaates on synthetic incipits, because we wanted to simulate a scenario where we don't have access to real-world incipits.

We trained each experiment for 20 epochs and took the model with lowest edit distance, averaged over the validation dataset.

    graphs of the validation & training edit distances from the tensorboard


## Results

<!--
- tabulka výsledků (pro každý experiment, pro každého přepisovatele, pro každé dílo)
- jak se SER chová když neřeším legato, attachmenty, pitche, ...
- diskuze nad language modelem a porovnání experimentů (+regularizace šumem)
-->

Here are the resulting symbol error rates, averaged over the entire validation dataset:

| Experiment | Symbol error rate |
| ---------- | ----------------- |
| 1          | 0.34              |
| 2          | 0.28              |
| 3          | 0.24              |

It seems that training on synthetic data is better than training on real-world data. But looking at the experiment 3, we see that the best approach is to combine both approaches. Synthetic data is probably better than real-world data simply because all the tokens are represented equally. The discussion on language model is more complicated and is explored [in a separate section](#123).

In [section xyz](#xyz) we proposed a set of metrics, intended to give us insight into the mistakes the model makes:

| Experiment | ITER_RAW | ITER_TRAINED | ITER_SLURLESS | ITER_ORNAMENTLESS | ITER_PITCHLESS |
| ---------- | -------- | ------------ | ------------- | ----------------- | -------------- |
| 1          | 0.44     | 0.42         | 0.30          | 0.26              | 0.21           |
| 2          | 0.37     | 0.34         | 0.28          | 0.25              | 0.17           |
| 3          | 0.31     | 0.29         | 0.21          | 0.19              | 0.14           |

When we compare the *ITER_RAW*, *ITER_TRAINED* and *ITER_SLURLESS*, we can see that reducing our focus to only trained tokens helps slightly, although it's not as big of an impact as I expected. Considerably larger difference is when we remove slur tokens. This confirms, what can be seen by looking manually at the predictions the model makes. There are a lot of mistakes related to slur classification. This might be caused by the fact that the engraving system does not capture all the variability that exists in the real world with regards to slur engraving.

Now that we know the experiment 3 performed the best, we will take a closer look at it. Here is a table of metrics for each evaluation page (averaged over all staves in that page):

| Page | Writer | SER  | ITER_RAW | ITER_TRAINED | ITER_SLURLESS | ITER_ORNAMENTLESS | ITER_PITCHLESS |
| ---- | ------ | ---- | -------- | ------------ | ------------- | ----------------- | -------------- |
| 2    | 13     | 0.19 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 3    | 13     | 0.11 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 16   | 13     | 0.29 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 1    | 17     | 0.28 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 2    | 20     | 0.26 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 3    | 20     | 0.09 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 16   | 20     | 0.31 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 2    | 34     | 0.24 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 3    | 34     | 0.05 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 16   | 34     | 0.32 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 2    | 41     | 0.21 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 3    | 41     | 0.15 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 16   | 41     | 0.27 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 3    | 49     | 0.27 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 5    | 49     | 0.18 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 9    | 49     | 0.41 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |
| 11   | 49     | 0.41 | 0.??     | 0.??         | 0.??          | 0.??              | 0.??           |

We can do an average for each writer and compare the results to the style of their handwriting:

| Writer | SER  | Handwriting style                               |
| ------ | ---- | ----------------------------------------------- |
| 13     | 0.20 | regular, round noteheads                        |
| 34     | 0.21 | regular, round noteheads, slanted               |
| 41     | 0.21 | beautiful, round noteheads                      |
| 20     | 0.22 | regular, dash noteheads                         |
| 17     | 0.28 | regular, round noteheads                        |
| 49     | 0.32 | worse, dash noteheads                           |

The first four writers are very much comparable, but the writer 49 has the worst handwriting of all the writers an he eded up last, as expected.

Similarly we can average over each music page:

| Page | SER  | Notes                                                |
| ---- | ---- | ---------------------------------------------------- |
| 3    | 0.13 | perfect                                              |
| 5    | 0.18 | trills                                               |
| 2    | 0.26 | trills, gracenotes                                   |
| 1    | 0.28 | triplets, fermata, rests in beamed groups            |
| 16   | 0.30 | beamed notes with empty noteheads, accents           |
| 9    | 0.41 | `?` token, fermata                                   |
| 11   | 0.41 | `?` token                                            |


Pages 9 and 11 ended up last, because they are only present for writer 49, who ended up as the worst writer. Page 3 is very interesting. It is the only page, that can be fully encoded using Mashcima encoding and all the smybols it contains can be engraved using the Mashcima engraving system. It is, however, also the simplest page in that it does not contain any complicated expressions and contains only few slurs. This is supported by the fact that page 5 ended up also very well and the page 5 is very comparable in its layout and complexity to the page 3.


### Language model

<!--
- language model má vliv, ale ne tak zásadní. Například se naučil nevyrábět nedokončené beamy (když splete první notu, tak z "e= =e= =e" vyrobí "q e= =e", ačkoliv prostřední nota má trámec na obě strany)
- stejně tak se naučí že jeden křížek po klíči má správnou hodnotu i když je nakreslený špatně
     (tzn. proto je dobré trénovat jak na generovaných, tak na primusu)
-->

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


## Comparison to other work

<!--
- the baseline paper - how we compare
- is the comparison fair? (different vocabulary, different token density)
    - e.g. dynamics? Text around the staff? ... popsat co všechno může být nefér a pak se podívat, jak moc je to reálně nefér
    - ALE můžu vzít ten jeden staff co tam mají s obrázkem a přidat můj vysledek
- what are the numbers for commercial software from that paper?
- qualitative comparison on the staff from page 003

??? CO VŠECHNO Z TOHO ČLÁNKU SI MŮŽU DOVOLIT SEM DÁT ???
-->


## Evaluating on Printed PrIMuS incipits

We also wanted to try, how would our model perform on printed music. Models by other people are often pre-trained on printed music and then fine-tuned on handwritten images via transfer learning. Ours is different in that it has never seen an image of printed music. We already have code for parsing PrIMuS dataset and since the dataset contains images as well, we will use those. We just slightly preprocessed the images - inverted them, normalized and slightly scaled down to have dimensions comparable to what the model trained on. We used the model from experiment 3 since it performed the best. The evaluation was performed on 100 incipits that the model hasn't seen during training and these are the results:

| SER  | ITER_RAW | ITER_TRAINED | ITER_SLURLESS | ITER_ORNAMENTLESS | ITER_PITCHLESS |
| ---- | -------- | ------------ | ------------- | ----------------- | -------------- |
| 0.76 | 0.79     | 0.79         | 0.75          | 0.74              | 0.71           |

You can see, that the performance is not very impressive. I did expect the error rate to be high, but not that high. Although it is understandable, because the printed music is very different to the handwritten. It would be interesting to also train on printed images in the future. This error rate would go down, but maybe the CVC-MUSCIMA error rate would go down as well.

    image of a printed staff and the prediction and the gold
    + maybe the same staff, engraved using Mashcima

Also note that *ITER_RAW* and *ITER_TRAINED* have the same value. This is expected, because we filter out incipits that can be engraved by Mashcima.


## Dropout layer importance

<!--
- popiš problém s dropoutem, jak to blblo, jak jsi to řešil, jak jsi zjistil,
    že by mohl pomoct dropout a jak pak pomohl
-->


# Conclusion and Future Works

> - anotace a generátor:
>   - rozšíření barlines (:|: |: :|, ||) a spoustu dalších symbolů (trill, fermata)
>   - rozšíření na dynamiku (mf, ff, pp, hairpins, ...)
>   - rozšíření na akordy
>   - rozšíření na text kolem not (kvůli regularizaci), e.g. "andante", "T=180", ...
> - použít úplně jinačí model - zkombinovat baseline paper a můj generátor
> - nebo vypiplat generátor a postavit na jeho základě novej dataset


# XXX `Content layout and notes`

V čem je end-to-end výhodné? (tzn. proč to vůbec prozkoumávám?)
- ručně vybraný fičury nebejvaj nejlepší, lepší je se interní fičury naučit
    (ideálně nějakej odkaz do Deep Leraning book na deep sítě)
- chyby v prvních fázích pipeline způsobují lavinový efekt chyb

Proč jsem zvolil RCNN+CTC? (jako konkrétní realizaci end-to-end modelu)
1) používá to SimpleHTR a od něho jsem se odpíchnul
2) díky CTC nemusím řešit alignment (segmentaci)
- z čeho jiného bych mohl vybírat?

Proč jsem zvolil CVC-MUSCIMA na evaluaci?
1) snadno lze anotovat, protože se díla opakují
2) z datasetů co jsou na výběr vyšel nejlíp https://apacha.github.io/OMR-Datasets/
    - je handwritten, obsahuje celé sheety, mám k němu MUSCIMA++ na symboly
    - je to jediný single-staff handwritten na výběr, ostatní na něm staví
        nebo to jsou pouze datasety symbolů

Na čem trénovat model?
- CVC-MUSCIMA nestačí, moc malý, malá variabilita
- žádný jiný na výber není
- použiju augmentaci dat -> vygeneruju nová data přeházením symoblů z CVC-MUSCIMY
    - jak dostanu symboly? Ty už mám v MUSCIMA++, použiju tu
    - dostanu anotace zadarmo
    - jak dostanu posloupnosti co generovat? Protože nechci totální náhodu.
        Použiju incipity z Primusu. (hypotéza: naučíme se language model)
            - odkaz: hypotézu otestujeme v experimentech

---

- Co je to RCNN síť
    - v čem je výhodná CTC loss (není třeba alignment)
    - Konkrétní architektura mojí sítě
- Reprezentace výstupu sítě **TODO: tohle rozepiš do detailu**
    - Inspirováno Primusem, ale drobné změny
    - proč agnostic a ne semantic
        - menší abeceda, jednodušší generátor mashcima
    - míň ukecaný než u primusu, aby se dalo lépe anotovat ručně - vizuelní podobnost
    - symetrické - pozice 0 je uprostřed
    - Co se generuje vs. co lze anotovat
    - Pitch information
    - Attachments
    - Jak lze rozšířit do budoucna (dynamika, akordy) ... tohle ale spíš do závěru tady jen odkaz
- Mashcima **TODO: tohle rozepiš do detailu**
    - sázení ručně psaných not pomocí symbolů z datasetu MUSCIMA++
    - proč? Mám málo dat vzhledem k tomu jak mohou být variabilní
    - cíl - co nejvíce napodobit vzhled dat v CVC-MUSCIMA
        - tzn. neřeším preprocessing a binarizaci
        - proč? Protože na něm budu testovat
    - popsat architekturu generátoru (třídy v pythonu), prostě dokumentace
        + nejen třídy, ale i jak funguje
    - problémy s rozlišením a max. délkou výstpu
- Experimenty
    - účel 1: jak dobrý je model co jsem udělal (evaluace)
    - účel 2: na jakých posloupnostech je nejlépe trénovat (primus / generated)
        + diskuze o language modelu vs. regularizaci
    - porovnej díla a porovnej writery - jak se liší mezi sebou v úspěšnosti
    - otestovat hypotézu dropout vrstvy (SimpleHTR ji nemá?, Calvo ji má)