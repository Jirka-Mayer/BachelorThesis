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
