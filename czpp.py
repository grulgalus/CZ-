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
