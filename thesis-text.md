https://mj.ucw.cz/vyuka/bc/

# Abstract

Optical music recognition is a challenging field similar in many ways to optical text recognition. It brings, however, many challenges that traditional pipeline-based recognition systems struggle with. The end-to-end approach has proven to be superior in the domain of handwritten text recognition. We tried to apply this approach to the field of OMR. Specifically, we focused on handwritten music recognition. We evaluated our system on a portion of the CVC-MUSCIMA dataset and the approach seems to be promising.

*Note:* Přidat do abstraktu informace, že handwritten datasetů je fakt málo a že máme sázecí systém, kterej umí generovat fakt podobný syntetický data?

HTR:
https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742


# Introduction

- RCNN sítě jsou úspěšné na OCR a HTR
- OMR je podobné OCR, ale přináší další komplikace
- RCNN ještě nebyly použité na OMR pro ručně psané texty
    - pouze sázené, viz. CalvoRizo


**Cílem práce je:**
**Abstraktně:** Prozkoumat end-to-end přístup k řešení OMR
**Konkrétně:** Mít end-to-end model, který dává co nejlepší výsledky na prvních pěti přepisovatelích datasetu CVC-MUSCIMA. (Evaluate how this specific RCNN model performs on CVC-MUSCIMA)

---

Optical music recognition (OMR) is an interesting subfield of computer vision. It shares a lot of similarities to optical character recognition (OCR) and handwritten text recognition (HTR). It is, however, more challenging as is pointed out in the paper *Understanding Optical Music Recognition* (https://arxiv.org/pdf/1908.03608.pdf). For example in OCR, characters are read in one direction, typically from left to right. Musical symbols seem to be similar in that a staff is also read from left to right, but many symbols can be placed above each other. Piano scores can even have symbols that span multiple staves.

Although a musical score can be very complex, many scores are not. We can limit ourselves to scores that are monophonic, have a single voice and have symbols spanning only one staff. Monophonic scores lack chords, meaning there's only one note plaing at a time. This holds, for example, for windblown instruments, since they cannot play multiple notes simulatenously. Sometimes multiple voices (instruments) are engraved in a single staff to save space. We will not attempt to read these scores either. It would be like reading two lines of text simultaneously and the proposed model can output only a single sequence. Also deciding what voice a given note belongs to is in itself a complicated problem.

> v HTR se používá RCNN, protože je fajn (https://repositum.tuwien.ac.at/obvutwhs/download/pdf/2874742)
> Jednak, druhak jsem ji vybral, protože s ním mám zkušennosti, třeťak Calvo 2018 ji taky použil

> tuhle architekturu zkusil Calvo 2018 na primusu

> primus je nice and all, ale je sázenej, jenže hodně not je ručně psanejch (to je ta díra co plním)

> my tohle chceme zkusit na ručně psaných *The goal of this thesis is: ...*

> narazili jsme na nedostatek dat, takže součástí práce je taky Mashcima


---

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