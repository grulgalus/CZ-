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
    echo "[*] Aktualizuji a stahuji závislosti..."
    pkg update -y && pkg install python nano -y
    echo "$NOW" > "$UPDATE_FILE"
else
    echo "[*] Aktualizace závislostí přeskočena (proběhla před méně než týdnem)."
fi

echo "[*] Vytvářím jádro překladače (czpp.py)..."
cat << 'PYTHONEOF' > czpp.py
import sys
import os
import re

if len(sys.argv) < 2:
    print("Chyba: Zadej soubor! Použití: czpp <soubor.czpp>")
    sys.exit(1)

soubor = sys.argv[1]

if not os.path.exists(soubor):
    print(f"Chyba: Soubor {soubor} nebyl nalezen!")
    sys.exit(1)

with open(soubor, 'r', encoding='utf-8') as f:
    kod = f.read()

slovnik = {
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
    r'\btrida\b': 'class', r'\bja\b': 'self', r'\b__zacatek__\b': '__init__',
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

echo "[*] Nastavuji globální příkaz (alias) 'czpp'..."
if [ -d "$PREFIX/bin" ]; then
    echo '#!/bin/bash' > $PREFIX/bin/czpp
    echo "python $(pwd)/czpp.py \"\$@\"" >> $PREFIX/bin/czpp
    chmod +x $PREFIX/bin/czpp
fi

echo "[=============== HOTOVO ===============]"
echo "Instalátor dokončen! Závislosti a příkaz 'czpp' jsou ready."
