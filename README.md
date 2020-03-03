# Automatický přepis notových zápisů pomocí hlubokých neuronových sítí

Cílem bakalářské práce je převést vstupní obrázek notového zápisu
(foto nebo scan) do formátu MusicXML, se kterým umí pracovat
nástroje pro zápis not (Sibelius, Finale, MuseScore).


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


## Jiné poznámky

Normalizovat výšku: 64px je ideální, 32px pro základní symboly projde


## Teď pracuj na / pokračuj s

Naprogramuj vícekanálový CTC výstup. (zatím pro jednoduché vstupy)

Vymysli nějakou lepší reprezentaci not (třída `Symbol`).

Vyčisti zdrojové kódy.

Přidej *trainer* - nějakou třídu, co provede postupné trénování sítě.
(a s tím souvisí perzistence sítě (automaticky ulož při zlepšení))
