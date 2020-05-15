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

> Co je OMR

Optical music recognition (OMR) is an interesting subfield of computer vision. It shares a lot of similarities to optical character recognition (OCR) and handwritten text recognition (HTR). It is, however, more challenging as is pointed out in the paper *Understanding Optical Music Recognition* (https://arxiv.org/pdf/1908.03608.pdf). For example in OCR, characters are read in one direction, typically from left to right. Musical symbols seem to be similar in that a staff is also read from left to right, but many symbols can be placed above each other. Piano scores can even have symbols that span multiple staves.

Although a musical score can be very complex, many scores are not. We can limit ourselves to scores that are monophonic, have a single voice and have symbols spanning only one staff. Monophonic scores lack chords, meaning there's only one note plaing at a time. This holds, for example, for windblown instruments, since they cannot play multiple notes simulatenously. Sometimes multiple voices (instruments) are engraved in a single staff to save space. We will not attempt to read these scores either. It would be like reading two lines of text simultaneously and the proposed model can output only a single sequence. Also deciding what voice a given note belongs to is in itself a complicated problem.

> v HTR se používá RCNN, protože je fajn (https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742) nebo (http://www.jpuigcerver.net/pubs/jpuigcerver_icdar2017.pdf)
> Jednak, druhak jsem ji vybral, protože s ním mám zkušennosti, třeťak Calvo 2018 ji taky použil

Deep neural networks have transformed the field of computer vision recently. Especially convolutional networks (CNN), whose architecture is particularly well suited for image processing. Recurrent neural networks (RNN) have been used for sequence processing, like natural language modelling or natural language translation. We can combine these two architectures to create a so called RCNN network. When trained using connectionist temporal classification (CTC), we get a powerful architecture that is ideal for processing visual sequential data (http://www.jpuigcerver.net/pubs/jpuigcerver_icdar2017.pdf). This architecture has been used in handwritten text recognition to yield state-of-the-art results (https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742).

> tuhle architekturu zkusil Calvo 2018 na primusu

If we limit the complexity of musical scores to the point that a single staff can be represented as a sequence of tokens, we can use this architecture to tackle to problem of OMR. This approach has been tried in 2018 by Calvo-Zaragoza and Rizo in 2018 (https://www.mdpi.com/2076-3417/8/4/606). They created the PrIMuS dataset, which contains 87678 real-music incipits. An incipit is the part of a melody or a musical work that is most recognizable for that work. Each incipit is a few measures long, typically shorter than a single staff of printed sheet music would be.

> primus je nice and all, ale je sázenej, jenže hodně not je ručně psanejch (to je ta díra co plním)

The resulting model has been compared against Audiveris, an open-source OMR tool (https://github.com/Audiveris), and has proven to be superior on the PrIMuS dataset. However the dataset contains printed images only. Since this RCNN architecture is an end-to-end approach, there's a great chance that it would be ideal for reading handwritten scores as well (drawing analogy from HTR).

> my tohle chceme zkusit na ručně psaných *The goal of this thesis is: ...*

Therefore the goal of this thesis is to explore the end-to-end approach for optical music recognition of handwritten music scores. More specifically we want to train a RCNN network to yield the best possible results on the CVC-MUSCIMA dataset.

> narazili jsme na nedostatek dat

We needed to obtain training data. We explored the *Collection of datasets for OMR* by Alexander Pacha (https://apacha.github.io/OMR-Datasets/) and quickly found out that the only dataset containing entire staves of handwritten sheet music is the CVC-MUSCIMA dataset (http://www.cvc.uab.es/cvcmuscima/index_database.html). Every other handwritten dataset contains only muscial symbols or is derived from CVC-MUSCIMA. Since CVC-MUSCIMA is intended for writer classification and staff removal, it contains only 20 parts, each written by 50 writers. That's far too small variability, given the task we are trying to solve.

> takže součástí práce je taky Mashcima

Facing this issue we resorted to data augmentation. The idea is to take handwritten musical symbols and place them onto an empty staff to create a new staff image. We called this music engraving system *Mashcima* and the system is explained in the chapter [M](#M). The muscial symbols used by Mashcima come from the MUSCIMA++ dataset (https://ufal.mff.cuni.cz/muscima). This dataset is built on top of CVC-MUSCIMA and provides pixel-perfect symbol segmentation and relationships between symbols. The reason we chose MUSCIMA++, instead of other musical symbol datasets, is that it is built on top of CVC-MUSCIMA. This means the image resolution and overall style is consistent with CVC-MUSCIMA. Also MUSCIMA++ has been developed at Charles University and so it was easy to contact its creator when needed. We however do make sure, that the final evaluation is performed on data the neural network has not seen during training. Specifically it trains on staves by completely different writers than the ones used for evaluation.

Mashcima engraving system is the main feature that sets this thesis apart from other works. Other people, when faced with the lack of training data, use simple data augentation (dilation, blurring, distortion) or transfer learning (https://openreview.net/pdf?id=SygqKLQrXQ). We belive that custom angraving system for hadwritten music is the best way to produce overabundance of high quality training data. Our confidence stems from the fact, that non-trained human has difficulties distinguishing a real-world sample from a well-engraved one.

    figure comparing one staff from CVC-MUSCIMA and one from PrIMuS, engraved using Mashcima

> jak práce dopadla - úspěch nebo ne?

It is difficult to evaluate an OMR system in general. This is because there is no standard dataset that can be used and no standard set of metrics. Moreover we proposed a new Mashcima representation for the music engraved in a staff. This representation is based on the agnostic encoding proposed by Calvo-Zaragoza and Rizo (https://grfia.dlsi.ua.es/primus/). Using custom representation makes it yet more difficult to compare our results to other works. That being said, we can still make some comparisons. It seems that having specialized engraving system is a step in the right direction. The results we obained when evaluating are comparable to simmilar works performing simmilar evaluation (https://openreview.net/pdf?id=SygqKLQrXQ).

> MusicXML nebylo implementováno
> Image preprocessing nebyl implementován, máme už binarizovaný vstup

The thesis assignment states that output of our model will be a MusicXML file. We quickly realized that the problem is far larger then anticipated and so we focused on the core features only. Similarly the model input is not a plain photo or scan. It is already preprocessed and binarized. This problem has already been solved during the creation of the CVC-MUSCIMA dataset (http://www.cvc.uab.es/cvcmuscima/index_database.html).


## Thesis outline

Thesis outline:
- chapter 1, 2, 3, 4


# Content

*Vymysli, kam strčit následující - jestli je to úvod nebo ne.*

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
- Experimenty
    - účel 1: jak dobrý je model co jsem udělal (evaluace)
    - účel 2: na jakých posloupnostech je nejlépe trénovat (primus / generated)
        + diskuze o language modelu vs. regularizaci
    - porovnej díla a porovnej writery - jak se liší mezi sebou v úspěšnosti
    - otestovat hypotézu dropout vrstvy (SimpleHTR ji nemá?, Calvo ji má)