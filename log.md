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
