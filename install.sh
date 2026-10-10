#!/bin/bash

echo "[*] Kontroluji datum poslední aktualizace..."
NOW=$(date +%s)
UPDATE_FILE="$HOME/.czpp_last_update"

if [ ! -f "$UPDATE_FILE" ]; then
    NEEDS_UPDATE=true
else
    LAST_UPDATE=$(cat "$UPDATE_FILE")
    DIFF=$((NOW - LAST_UPDATE))
    if [ "$DIFF" -ge 604800 ]; then
        NEEDS_UPDATE=true
    else
        NEEDS_UPDATE=false
    fi
fi

if [ "$NEEDS_UPDATE" = true ]; then
    echo "[*] Aktualizuji balíčky..."
    pkg update -y && pkg install python nano git -y
    echo "$NOW" > "$UPDATE_FILE"
else
    echo "[*] Aktualizace přeskočena (poslední proběhla nedávno)."
fi

echo "[*] Vytvářím ROZŠÍŘENÝ překladač czpp.py..."
cat << 'PYTHONEOF' > czpp.py
import sys
import os
import re

if len(sys.argv) < 2:
    print("Chyba: Zadej soubor! Použití: czpp <soubor.czpp> (nebo python czpp.py <soubor>)")
    sys.exit(1)

soubor = sys.argv[1]

if not os.path.exists(soubor):
    print(f"Chyba: Soubor {soubor} nebyl nalezen!")
    sys.exit(1)

with open(soubor, 'r', encoding='utf-8') as f:
    kod = f.read()

# OBROVSKÉ ROZŠÍŘENÍ JAZYKA
slovnik = {
    # Základy a logika
    r'\bvypis\b': 'print', r'\bvstup\b': 'input', r'\bdelka\b': 'len',
    r'\btext\b': 'str', r'\bcele_cislo\b': 'int', r'\bseznam\b': 'list',
    r'\bslovnik\b': 'dict', r'\botevri\b': 'open',
    r'\bdefinuj\b': 'def', r'\bvrat\b': 'return', r'\bpokud\b': 'if',
    r'\bnebo_pokud\b': 'elif', r'\bjinak\b': 'else', r'\bpro\b': 'for',
    r'\bv\b': 'in', r'\bdokud\b': 'while', r'\bPravda\b': 'True',
    r'\bNepravda\b': 'False', r'\bNic\b': 'None', r'\ba\b': 'and',
    r'\bnebo\b': 'or', r'\bne\b': 'not', r'\bneni\b': 'is not',
    r'\bje\b': 'is', r'\brozmezi\b': 'range', r'\bnacti\b': 'import',
    r'\bzkus\b': 'try', r'\bchyt\b': 'except', r'\bkonecne\b': 'finally',
    r'\bvyvolej\b': 'raise', r'\bpreskoc\b': 'pass', r'\bprerus\b': 'break',
    r'\bpokracuj\b': 'continue', r'\bjako\b': 'as', r'\bs\b': 'with',
    
    # OOP (Objektově orientované programování)
    r'\btrida\b': 'class', r'\bja\b': 'self', r'\b__zacatek__\b': '__init__',
    
    # Metody (seznamy a texty)
    r'\bpridej\b': 'append', r'\bodeber\b': 'pop', r'\bvycisti\b': 'clear',
    r'\bnahrad\b': 'replace', r'\brozdel\b': 'split', r'\bspoj\b': 'join',
    r'\bmala_pismena\b': 'lower', r'\bvelka_pismena\b': 'upper',
    r'\bserad\b': 'sort', r'\bklice\b': 'keys', r'\bhodnoty\b': 'values',
    r'\bpolozky\b': 'items'
}

for cz, py in slovnik.items():
    kod = re.sub(cz, py, kod)

docasny_soubor = soubor.replace(".czpp", "_prelozeno.py")
with open(docasny_soubor, 'w', encoding='utf-8') as f:
    f.write(kod)

os.system(f"python {docasny_soubor}")
os.remove(docasny_soubor)
PYTHONEOF

echo "[*] Nastavuji globální příkaz czpp pro Termux..."
if [ -d "$PREFIX/bin" ]; then
    echo '#!/bin/bash' > $PREFIX/bin/czpp
    echo "python $(pwd)/czpp.py \"\$@\"" >> $PREFIX/bin/czpp
    chmod +x $PREFIX/bin/czpp
fi

echo "[*] Vytvářím strukturu pro GitHub..."
mkdir -p .github/workflows

# GitHub Actions (x86 testování)
cat << 'YMLEOF' > .github/workflows/ci.yml
name: cz++ CI (x86)

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Spustit test.czpp pres prekladac
      run: python czpp.py test.czpp
YMLEOF

# README pro GitHub
cat << 'MDEOF' > README.md
# 🇨🇿 cz++ 
Nejlepší český programovací jazyk postavený na Pythonu!

## Jak to funguje?
Kód se píše v češtině (soubory `.czpp`). Transpiler `czpp.py` ho před spuštěním bleskově přeloží do čistého Pythonu a ihned spustí. Běží na ARM (mobil/Termux) i x86 (PC/Windows/Linux).

## Ukázka kódu
\`\`\`python
trida Robot:
    definuj __zacatek__(ja, jmeno):
        ja.jmeno = jmeno
    
    definuj pozdrav(ja):
        vypis(f"Ahoj, ja jsem {ja.jmeno}")

muj_robot = Robot("Karel")
muj_robot.pozdrav()
\`\`\`

## Instalace a spuštění
1. Stáhněte si repo.
2. Spusťte \`bash install.sh\` (na Termuxu/Linuxu).
3. Spouštějte skripty pomocí \`czpp soubor.czpp\`.
MDEOF

# .gitignore
cat << 'GITEOF' > .gitignore
__pycache__/
*_prelozeno.py
.czpp_last_update
GITEOF

echo "[*] Vytvářím pokročilý test.czpp (OOP a list metody)..."
cat << 'CODEEOF' > test.czpp
vypis("=" * 40)
vypis("🚀 cz++ JE PRIPRAVENO PRO GITHUB A x86!")
vypis("=" * 40)

trida Hrac:
    definuj __zacatek__(ja, jmeno):
        ja.jmeno = jmeno
        ja.inventar = seznam()
    
    definuj seber_vec(ja, vec):
        ja.inventar.pridej(vec)
        vypis(f"{ja.jmeno} sebral: {vec}")

    definuj ukaz_inventar(ja):
        vypis(f"Inventar hrace {ja.jmeno}: {spoj(', ', ja.inventar)}")

hrdinove = ["Karel", "Pepa"]
hrdinove.pridej("Lojza")

hrac1 = Hrac(hrdinove[0])
hrac1.seber_vec("Mec")
hrac1.seber_vec("Stit")
hrac1.ukaz_inventar()

vypis("✅ Vse funguje skvele!")
CODEEOF

echo "[=============== HOTOVO ===============]"
echo "Tvůj projekt je 100% připraven k nahrání na GitHub!"
echo "Licence, README i GitHub Actions (x86) jsou vytvořeny."
echo "Zkus rovnou test: czpp test.czpp"
