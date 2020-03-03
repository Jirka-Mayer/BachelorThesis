## 2020-02-17

- seznámení se s datasetem MUSCIMA++
- vymýšlení automatického generování dat

> MUSCIMA++ je dost malá a navíc co mám zkušennosti s architekturou sítě
z rozpoznávání textu, tak se vyplatí nejprve trénovat na generovaných, lehkých
datech. Jinak nastanou problémy s konvergencí. Jakmile se síť "chytne", tak pak
už se naučí i složitější data (zřejmě jde o něco jako transfer learning).
Každopádně generovaná data ještě navíc pomáhají dataset vyvážit (zvýšit četnost
klasifikačních tříd, které se vyskytují zřídka).


## 2020-02-24

- programování logiky kolem generování a ukládání datasetu


## 2020-02-25

Řeším problémy s konvergencí. Myšlenka byla, vzít model Texia, vyměnit dataset
za noty a zkusit jak se učí. Jenže ono to nekonvergovalo. Ve skutečnosti jsem
model texia nezkopíroval beze změn, takže tu byla možnost že jsem vyrobil chybu.
Tak jsem tedy vzal texio beze změn a zkusil jak rychle konverguje. Na číslech
generovaných automticky konvergovalo rychle (30s trénování - asi 300 batchů).
Když jsem tam dal noty, kdy jsem jednotlivé notové symboly namapoval na
číslice, tak nekonvergovalo ani po 10 minutách.

Všiml jsem si, že text číslic je dost velký (číslíce je od okraje k
okraji obrázku), tak jsem zkusil následující změny:

- zmenšil jsem okraj nad a pod notovou osnovou tak, že se houslový klíč přesně
  dotýká okrajů obrázku
- odřízl jsem houslový klíč a taktové předznamenání
- zredukoval jsem řetězce na konstantní délku 1

Najednou síť konvergovala stejně rychle jako na číslicích. Vrátil jsem zpět
délku sekvencí na rozmezí 1 - 5 a opět konvergence zůstala. Ale zbylé dvě věci
(ani každou zvlášť) jsem vrátit nemohl, ke konvergenci pak nedošlo.

> Ještě jsem řešil délku trénovacích sekvencí a ono stačí mít sekvence krátké
  (jednotky symbolů), rychleji se trénují a počet batchů ke konvergenci
  se prakticky nezmění.

```txt
Čili cílem je konvergovat během ~300 batchů, déle by konvergence trvat neměla.
```

Ok, tak ještě to vypadá, že je tu prvek náhody. Někdy prostě nezkonverguje
i když má klasifikovat jen jeden symbol. Takže je s tím třeba počítat.

Ok, tak nakonec ani rozlišení nemá tak zásadní vliv jak jsem myslel.
Když má trénovací dataset jen jednu notu, tak také zkonverguje.
Čili je to asi kombinace více faktorů. Ve finále jde o to, nějak
tu síť nakopnout, aby věděla, co je vůbec symbol a potom teprve může začít
klasifikovat více symbolů a potom nějaké složitější kombinace symbolů.

> **Pozor:** možná se mi ABBC slepí na ABC při parsování výstupu sítě
  Ale možná taky jen chybí dostatek příkladů v trénovacím setu, aby
  se síť naučila vkládat blank mezi opakování symbolu. (boost repeat?)


## 2020-03-02

Vymýšlím, jak na vícerozměrnou CTC.
Tady ji vícerozměrnou nedělají: https://github.com/OMR-Research/tf-end-to-end

Dobrý CTC přehled:
https://towardsdatascience.com/intuitively-understanding-connectionist
-temporal-classification-3797e43a86c

Co takhle mít pro každou linku jednu CTC, která řekne TRUE když tam je nota
a případně i její variantu a EMPTY když tam nota není. Navíc bude vždy
hlásit pomlky, klíče a další symboly přes celou osnovu.

To by mohlo vyřešit problém s vícenásobnými notami (akordy).
Každý výstupní CTC kanál zaregistruje "je tu akord", ale každý řekne, zda
je v tom akordu přítomen.


## 2020-03-03

Peru se s vícekanálovým výstupem sítě. (13 kanálů, od dolní pomocné linky po
horní pomocnou linku) Moc to nejde, síť nekonverguje, má problémy se cokoliv
naučit i když je vstup triviální. Když se štěpila na poslední vrstvě, tak
to moc nedělalo a když jsem to teď rozštěpil mezi CNN a RNN, tak je teď
síť podstatně větší a tedy se i o dost pomaleji trénuje.

Tak nakonec dříve rozštěpená síť zkonvergovala, ale trvalo jí to déle, protože
má teď asi větší kapacitu (a trénuje se pomaleji). Jo a taky zatím zkonvergovala
jen na trénovacích datech, ne validačních, takže se je možná jen
naučila nazpaměť. Jo, to bude ono. Overfituje.

> Co takhle udělat model, co na monofonní hudbě funguje stejně nějako předchozí
jednokanálová architektura? (o které víme, že zkonvergovala)

Zkusím se omezit jen na 4 kanály místo 13 a ty budou reprezentovat jednotlivé
hlasy směrem odshora dolů. Pokud n-tý hlas nebude přítomen, tak bude predikovat
třídu, že tu není nota. Monofonní vstupy bude potom klasifikovat čistě
první kanál.

Ok, naprogramoval jsem "voice channels". Když dám jeden voice, tak na
13 možných výstupních tříd (pozic not) konverguje v pořádku.
Když dám jeden voice, generuju občas i dvojnoty, tak zkonverguje, ale musí
být četnost vícenásobných not dostatečně nízká (1/8). Konvergence se mi takhle
povedla i se dvěma výstupními kanály na (1/8) četnosti dvojnot. Po prvotní
konvergenci se ale četnost bude muset navýšit, protože jiank drhuý hlas všude
predikuje "voice-not-present" třídu.

Stejně je jeden hlas mnohem lepší než více hlasů. Teď jsem zkoušel trénovat
na jednom hlasu síť pro dva hlasy a prostě ne a ne zkonvergovat a když
jsem ji omezil na jeden hlas, tak konverguje okamžitě.

Ještě mě napadá vrátit se k principu kanálů podle pozic not, jen místo
štěpení jedné sítě trénovat oddělené modely. A taky jim generovat data
s rozumným zastoupením cílové třídy. (síť detekující střední linku bude
mít stejně not na střední lince, jako mimo ní)
