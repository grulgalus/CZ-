# 🇨🇿 CZ++ (Český Programovací Jazyk)
CZ++ je plně počeštěný programovací jazyk a framework, který nabízí nevídanou flexibilitu.

## 🚀 Tři Režimy Běhu
1. **Interpretovaný (Python) Backend:**
   Slouží k běžnému psaní skriptů, používá kompletně českou syntaxi (např. `pokud`, `dokud`, `porovnej`, `pripad`).
2. **Kompilovaný (C++) Backend:**
   Překládá `cz++` do čistého strojového kódu přes C/C++ (Cython & Clang). Ideální pro maximální výkon.
3. **Bare-Metal OS Backend:**
   Ultimátní nástroj! Umožňuje z českých příkazů vygenerovat čistý Assembly kód, propojí ho s Master Boot Recordem (Sektor 1) a vytvoří obraz `.img`, který lze přímo bootovat jako samostatný operační systém!

## 🛠️ Ukázka kódu pro tvorbu OS
```python
vycisti()
vypis("Vitejte ve vlastnim systemu!")
vypis("Stiskni cokoliv pro pokracovani...")
cekej_na_klavesu()
zastav()
Spuštění: python czpp.py --os muj_system.czpp

Vyvinuto v Termuxu.
