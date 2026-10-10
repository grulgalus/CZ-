# 🇨🇿 cz++ 
Nejlepší český programovací jazyk postavený na Pythonu!

## Jak to funguje?
Kód se píše v češtině (soubory `.czpp`). Transpiler `czpp.py` ho před spuštěním bleskově přeloží do čistého Pythonu a ihned spustí. Běží na ARM (mobil/Termux) i x86 (PC/Windows/Linux).

## Ukázka kódu
python
trida Robot:
    definuj __zacatek__(ja, jmeno):
        ja.jmeno = jmeno
    
    definuj pozdrav(ja):
        vypis(f"Ahoj, ja jsem {ja.jmeno}")

    muj_robot = Robot("Karel")
    muj_robot.pozdrav()


## Instalace a spuštění
1. Stáhněte si repo.
2. Spusťte `bash install.sh` (na Termuxu/Linuxu).
3. Spouštějte skripty pomocí `czpp soubor.czpp`.
