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

> Tradiční systémy používají pipeline

> deep NN spojují celou pipeline do jednoho celku, learned features

> CTC umožňuje neřešit alignment, snazší anotace

> konkrétní architektura mojí sítě (tabulka) + hypotéza o dropout vrstvě

> multi channel CTC attempts


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

We can provide a simple overview of the terms used in this chapter:

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

The first symbol we need to encode is a note. A note has some duration and some pitch. These two pieces of information can vary independently, so it can seem logical to represent them using two vectors. The problem is that the connection temporal classification can output only one vector at a time. To solve this, we take every possible combination of note duration and pitch and create a token for that case.

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

The set of pitches we can choose from greatly impacts the vocabulary size. This is not a major issue, because the vocabulary size will still remain relatively small. Currently the vocabulary has about 550 tokens. The pitch range we choose spans from `-12` to `12` - that is from the fourth ledger line below the staff to the fourth ledger line above the staff.

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

There are few notes regarding the ordering:

- Slurs are always the first/last attachment.
- Some tokens are mutually exclusive, so are placed on the same level.
- There are many ornaments and this list is not exhaustive. It is meant to be extended in the future.
- Not all symbols here can be engraved by Mashcima.
- There can be many more tuplet numbers, only triplets are currently present.


### Slurs

Slurs and ties are one of the first symbols that make OMR complicated. Slur is a curved line going from one notehead to another. Notes that are under a slur should be played blended together without explicit note beginnings. Tie looks exactly like a slur, just the two notes it joins have the same pitch. This means the notes should be played as one long note. So the difference is only semantic, we will consider ties to be slurs.

> CONTINUE HERE


### Beams

<!-- beams -->


### Key and time signatures

<!-- key & time signatures -->


## Differences to PrIMuS

<!-- kratší názvy tokenů - víc se jich vejde na řádek + vizuelní podobnost -->
<!-- pitch encoding, já jsem centered -->
<!-- agnostic mi zajistí jednodušší kód, protože si nemusím pamatovat stavovou informaci, jako je key signature -->


## Extensibility


# Engraving System


# Experiments and Results

<!--
- describe metrics used for evaluation (SER)
- describe the data we are evaluating on (writer selection, ...)
- describe the experiments and what their goal is (01 - 03)
- talk about differences in generated symbols vs. all the symbols, propose new levenshtein normalization and show the results
- compare the results to the baseline paper and discuss
- result of the dropout hypothesis

drobnosti:
- language model má vliv, ale ne tak zásadní. Například se naučil nevyrábět nedokončené beamy (když splete první notu, tak z "e= =e= =e" vyrobí "q e= =e", ačkoliv prostřední nota má trámec na obě strany)
- stejně tak se naučí že jeden křížek po klíči má správnou hodnotu i když je nakreslený špatně
     (tzn. proto je dobré trénovat jak na generovaných, tak na primusu)
-->

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
| 1          | 0.31              |
| 2          | 0.27              |
| 3          | 0.24              |

It seems that training on synthetic data is better than training on real-world data. But looking at the experiment 3, we see that the best approach is to combine both approaches. Synthetic data is probably better than real-world data simply because all the tokens are represented equally. The discussion on language model is more complicated and is explored [in a separate section](#123).

In [section xyz](#xyz) we proposed a set of metrics, intended to give us insight into the mistakes the model makes:

| Experiment | ITER_RAW | ITER_TRAINED | ITER_SLURLESS | ITER_ORNAMENTLESS | ITER_PITCHLESS |
| ---------- | -------- | ------------ | ------------- | ----------------- | -------------- |
| 1          | 0.41     | 0.39         | 0.28          | 0.25              | 0.20           |
| 2          | 0.35     | 0.33         | 0.25          | 0.23              | 0.17           |
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