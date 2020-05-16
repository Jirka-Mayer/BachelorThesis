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

Ale to můžeme stejně tak dělat pro kanály podle hlasů. Takže můžu zkusit např
natrénovat model, co bude detekovat právě druhé hlasy.


## 2020-03-04

- zkontroluj, že se neodchyluješ od zadání v přechodu od psaných k sázeným
- omezení na monofonní hudbu by mělo být ok
- jak moc jsem vázán na muscimu?

...

- Zahoď vícekanálový výstup sítě, kdyžtak současné věci serializujeme za sebe
- Zkus generovat delší monofonní hudbu a jak na ní konverguješ (~3 takty).
- Zkus jestli zkonverguješ na něčem o rozměrech muscimy
- Vzít muscimu, vytahat z ní monofonní data, anotovat je a využít toho, že je
    tam jen 20 děl, ale každé v 50 variantách. (méně anotování)

Plán tedy je:

- klasifikuj jen takty (nic delšího), data použij z muscimy, vyber nějaké
lehké, anotuj je. Použij síť předtrénovanou na generovaných datech.


## 2020-03-12

Síť nechce zkonvergovat na generovaných datech z muscimy. Zjistil jsem, že
má vliv počet výstupních tříd. Když nechám všechny třídy, edit distance se
zasekne kolem 50%. Když dám jen dvě výstupní třídy, tak zkonverguje.

> Zajímavé: síť se zasekne i když délka sekvencí je 1
> To hintuje na nějaký fundamentální problém při velkém počtu tříd
> (Délka vstupu nemá vliv na konvergenci, pouze počet tříd)

Možnosti jsou:
- je něco špatně se sítí (existuje nějaké tvrzení o CTC, že větší počet tříd je těžší)
- je špatně něco s kódem někde jinde, že se síť potom špatně trénuje

Tak jako tak teď konverguje v rozmezí 100-200 batchů.

Teď budu vracet složitost generování a nechám prozatím malý počet tříd.

---

Vrátil jsem 64px rozlišení a vše zůstalo ok.
Vrátil jsem variabilitu ve vzdálenostech not a jejich tvaru a trénování to
ještě urychlylo (ED spadne dříve pryč z 1.0, ale na 0.0 se dostane opět
během zhruba 200 batchů).

---

Začínám experimentovat s počtem výstupních tříd. (do teď jsem měl jen 2)

Když přidám 5 dummy tříd, které se nikdy v labelech neobjeví, tak síť konverguje
normálně. Jako když tam jsou pouze dvě chtěné třídy.

Když přidám 100 dummy tříd. Tak mám zase problémy s konvergencí. Jaké?
Síť mi začne vracet jen jednu výstupní třídu. (cílové třídy jsou vedle sebe)

Když přidám 100 dummy tříd, ale cílové třídy na opačné konce slovní zásoby,
tak taky nekonverguje. Takže pořadí tříd nemá vliv (což by tak být mělo).

> Hypotéza: Problémy jsou způsobené tím, že přebytečné třídy nevyužívám.

Ano, vypadá to tak:

Když mám 9 tříd a uniformě je generuju, tak síť zkonverguje. Sice čím víc tříd,
tím pomaleji konverguje, ale konverguje konzistentně. Když mám ale těchto 9
tříd a přidám k nim 8 dalších co nepoužívám, tak síť nezkonverguje.

Super, tak teď mi přestala konvergovat i na těch 9 třídách na kterých
ještě před chvílí konvergovala.

Ale na 5 třídách je zase OK. Jsou to noty umístěné na linkách.

> Třeba má problém rozlišit mezi notou na lince a notou v mezeře
> a třeba by zvýšení rozlišení na 128px pomohlo

---

DROPOUT!!!!!!! DROPOUT TO VYŘEŠIL !!!!!!

Všechny problémy s konvergencí jsou pryč. Na dropout jsem narazil zde:
https://github.com/OMR-Research/tf-end-to-end/blob/master/ctc_model.py#L88
Takže jsem ho přidal na RNN vrstvy a výsledkem je:
- navýšení počtu tříd už funguje
- konvergence je pomalejší, ale konzistentní
    (už se nezasekáváme v lokálním minimu)
    
    
## 2020-03-22 ... 2020-04-01

Psaní generátoru dat.


## 2020-04-04

Příprava obrázků z CVC muscimy -- detekce řádek a jejich ořezávání.
Příprava na validaci na reálných datech.


## 2020-04-06

Ukládání modelu a implementace validace na CVC muscimě pro přepisovatele 1.


## 2020-04-07

Kreslení legát.

Pozn. legáto se váže na notu nebo taktovou čáru. Problém je, že když první
nota na řádku má legáto z předchozího řádku, tak tam není žádná taktová
čára na kterou by se chytla. Takže tam vygeneruju taktovou čáru, která nebude
mít žádný sprite a `generic_annotation` bude mít `None`. Tím pádem se ani
nevykreslí, ani se pro ní nevygeneruje anotace. A legáto tím pádem nepoleze
až na začátek řádku do kolíče a předznamenání.


## 2020-04-09

Načítání anotací z datasetu Primus.

Základ generování obrázku z mashcima anotace.


## 2020-04-11

Generování obrázku z mashcima anotace.


## 2020-05-16

Vybírání děl na evaluaci. Potřebuju vybrat 5 přepisovatelů, kteří jsou co nejpestřejší a od nich vzít ta díla, která mají MUSCIMA++ anotaci - aby se to dalo potažmo dále analyzovat, bylo-li by třeba.

Idea: seřadím si díla podle toho, jak dobře půjdou anotovat. (abych mohl posoudit, která díla brát v potaz)

03 - ok
12 - ok
02 - trilky, 2x gracenote
11 - jeden otazník, fermata
09 - 2x "?", fermata
05 - trilky
01 - triplets, fermata, pomlky v beamed skupinách
13 - jeden "?", jeden trámec na obě strany
14 - jeden akord, triplets
17 - dva řádky s akordy
15 - trámce na obě strany, pomlky v trámcích
16 - trámce přes empty noteheads, akcenty "<", chci až na ten jeden řádek
--------------------------------------------------------------------------------
06 - spíš nechci - trilky, gracenotes, zapiš gracenotes jako normální noty
04 - spíš nechci - tenuto, triplets, nested slur, bar repeat, fermata
18 - spíš nechci - dva řádky akordy, jeden akord i mimo
07 - ne - současné noty na mnoha místech trilky
08 - ne - gracenotes, čtvrťové pomlky přes půlové noty, dvojhlas v base
20 - ne - akordy na mnoha místech, potřeba hodně filtrovat
10 - ne - akordy
19 - ne - vícehlas


Vybereme všechny přepisovatele, kteří jsou v MUSCIMA++ pro nějaké dílo které prošlo výberem nahoře:
03 - 06 13 20 27 34 41 49
12 - 04 11 18 25 32 39 47
02 - 06 13 20 27 34 41 48
11 - 05 12 19 26 35 42 49
09 - 04 11 18 25 28 32 49
05 - 07 14 21 28 35 42 49
01 - 03 10 17 24 31 38 45
13 - 02 09 16 23 30 37 44
14 - 01 08 15 22 29 36 43
17 - 02 09 16 23 30 37 44
15 - 08 15 22 29 36 43 50
16 - 06 13 20 27 34 41 48

Seřadíme si přepisovatele podle četnosti děl a zjistíme krasopis:
49 49 49 49 - spíš škrábe, hlavičky jsou čárky                   TAKE
06 06 06 - spíš úhledné, hlavičky jsou kuličky                    --
13 13 13 - normální, hlavičky jsou kuličky                       TAKE
20 20 20 - normální, hlavičky jsou spíš čárky                    TAKE
27 27 27 - spíš úhledné, hlavičky jsou kuličky                    --
34 34 34 - normální, hlavičky jsou kuličky, rozházený sklon      TAKE
41 41 41 - velmi úhledné, hlavičky jsou kuličky                  TAKE

Zbývající přepisovatelé s málo díly:
02 02           44 44
04 04           48 48
08 08           01
09 09           03
11 11           05
15 15           07
16 16           10
18 18           12
22 22           14
23 23           17
25 25           19
28 28           21
29 29           24
30 30           26
32 32           31
35 35           38
36 36           39
37 37           45
42 42           47
43 43           50

Jaká díla nám teda zbyla:
03 - 06 13 20 27 34 41 49
12 - .. .. .. .. .. .. ..
02 - 06 13 20 27 34 41 ..
11 - .. .. .. .. .. .. 49
09 - .. .. .. .. .. .. 49
05 - .. .. .. .. .. .. 49
01 - .. .. .. .. .. .. ..
13 - .. .. .. .. .. .. ..
14 - .. .. .. .. .. .. ..
17 - .. .. .. .. .. .. ..
15 - .. .. .. .. .. .. ..
16 - 06 13 20 27 34 41 ..
     --       --

Autoři, kteří padnou na evaluaci:
13, 20, 34, 41, 49
