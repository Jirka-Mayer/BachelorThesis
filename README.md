# Automatický přepis notových zápisů pomocí hlubokých neuronových sítí

## Zadání

Automatický přepis (rozpoznávání) notových zápisů (Optical Music
Recognition) je úloha, při níž je obrazový vstup obsahující notový
zápis (tištěný nebo ručně psaný) automaticky převeden do strojově
čitelné, strukturované podoby, která umožňuje další zpracování, jako
např. přehrání zaznamenané hudby, editaci zápisu, vysázení apod. Výzkum
i v této oblasti v poslední době ovlivnilo využití hlubokých
neuronových sítí. Většina metod, je ale založena na rozdělení úlohy na
podčásti, které jsou řešeny postupně (binarizace, odstranění osnov,
detekce objektů, rozpoznání jejich typů a dalších parametrů, syntéza
získané informace, zápis v požadovaném formátu). Cílem práce je
prozkoumat a implemetovat alternativní, tzv. end-to-end přístup, kdy se
celá úloha bude řešit najednou, vstupem bude jeden řádek notového
zápisu, výstupem jeho přepis do formátu musicXML. V práci budou použita
data MUSCIMA++.


## Přehled

Převod bude probíhat řádek po řádku, čili před samotným modelem bude muset
být logika, která vstupní obrázek na řádky převede. Prozatím se ale zabývám
čistě jen neuronovou sítí.

Cílem je použít neuronovou síť s následujícími částmi:

- `CNN blok` Vstupní konvoluční vrstvy, které převedou obrázek o fixní
  výšce a proměnlivé délce na sekvenci vektorů
- `RNN blok` Renkurentní část, která by měla propagovat informace horizontálně
- `CTC` Výsledná klasifikace pomocí chybové funkce
  *connectionist temporal classification*

Inspirace pochází z mého předešlého projektu
[Texio](https://play.google.com/store/apps/details?id=io.texio),
který používal stejnou architekturu pro parsování textu účtenek.


## Dokumentace

[Tady je zápis](log.md), kam píšu co jsem kdy udělal a co mě kdy napadlo.
V podstatě by tu měl být zachycený myšlenkový proces.

Tady je dokumentace jednotlivých větších komponent:

- [Dataset a generování dat](docs/dataset-generation.md)
- [Kód definice neuronové sítě `Network.py`](docs/network.md)
