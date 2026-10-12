import sys
import os
import re
import tokenize

if len(sys.argv) < 2:
    print("Chyba: Zadej soubor! Použití: czpp <soubor.czpp>")
    sys.exit(1)

soubor = sys.argv[1]

if not os.path.exists(soubor):
    print(f"Chyba: Soubor {soubor} nebyl nalezen!")
    sys.exit(1)

slovnik = {
    # MATCH-CASE (Nejnovější Python 3.10+)
    'porovnej': 'match', 'pripad': 'case',
    
    # ČESKÉ VÝJIMKY (Errors)
    'Vyjimka': 'Exception', 'ChybaHodnoty': 'ValueError', 'ChybaTypu': 'TypeError',
    'ChybaIndexu': 'IndexError', 'ChybaKlice': 'KeyError', 'ChybaBehu': 'RuntimeError',

    # ZÁKLADY, TYPY A FUNKCE
    'vypis': 'print', 'vstup': 'input', 'delka': 'len', 'typ': 'type',
    'text': 'str', 'cele_cislo': 'int', 'desetinne': 'float', 
    'seznam': 'list', 'slovnik': 'dict', 'mnozina': 'set', 'pravdivost': 'bool',
    'komplexni': 'complex', 'bajty': 'bytes', 'pevna_mnozina': 'frozenset',
    
    # CYKLY A LOGIKA
    'definuj': 'def', 'vrat': 'return', 'poskytni': 'yield', 
    'pokud': 'if', 'nebo_pokud': 'elif', 'jinak': 'else',
    'pro': 'for', 'v': 'in', 'dokud': 'while',
    'Pravda': 'True', 'Nepravda': 'False', 'Nic': 'None',
    'a': 'and', 'nebo': 'or', 'ne': 'not', 'neni': 'is not', 'je': 'is',
    
    # ASYNCHRONNÍ A POKROČILÉ FUNKCE
    'asynchronni': 'async', 'pockej': 'await', 'funkcicka': 'lambda',
    'nelokalni': 'nonlocal', 'globalni': 'global',
    
    # ITERÁTORY A MATEMATIKA
    'rozmezi': 'range', 'ocisluj': 'enumerate', 'zazipuj': 'zip',
    'vyfiltruj': 'filter', 'namapuj': 'map', 'vsechno': 'all', 'cokoliv': 'any',
    'zaokrouhli': 'round', 'absolutni': 'abs', 'minimum': 'min', 'maximum': 'max', 
    'soucet': 'sum', 'mocnina': 'pow', 'deleni_se_zbytkem': 'divmod',
    'dalsi': 'next', 'obracene': 'reversed',
    
    # ČÍSELNÉ SOUSTAVY
    'dvojkove': 'bin', 'sestnactkove': 'hex', 'osmickove': 'oct',
    
    # SYSTÉM, PAMĚŤ A INTROSPEKCE
    'vyhodnot': 'eval', 'spust': 'exec', 'obsah': 'dir', 
    'totoznost': 'id', 'otisk': 'hash', 'kod_znaku': 'ord', 'znak': 'chr',
    'globalni_promenne': 'globals', 'lokalni_promenne': 'locals',
    'ma_atribut': 'hasattr', 'ziskej_atribut': 'getattr', 'nastav_atribut': 'setattr',
    'je_instance': 'isinstance', 'je_podtrida': 'issubclass', 'lze_zavolat': 'callable',
    
    # OOP, DEKORÁTORY A MAGICKÉ METODY
    'trida': 'class', 'ja': 'self', 'rodic': 'super',
    'vlastnost': 'property', 'staticka_metoda': 'staticmethod', 'tridni_metoda': 'classmethod',
    '__zacatek__': '__init__', '__text__': '__str__', '__delka__': '__len__',
    '__secti__': '__add__', '__zavolej__': '__call__',
    
    # IMPORTY A VÝJIMKY (Logika)
    'nacti': 'import', 'jako': 'as', 's': 'with',
    'smaz': 'del', 'tvrzeni': 'assert',
    'zkus': 'try', 'chyt': 'except', 'konecne': 'finally', 'vyvolej': 'raise',
    'preskoc': 'pass', 'prerus': 'break', 'pokracuj': 'continue',
    
    # METODY POLE, MNOŽIN A SLOVNÍKŮ
    'pridej': 'append', 'rozsir': 'extend', 'vloz': 'insert', 
    'odeber': 'pop', 'vycisti': 'clear', 'najdi_index': 'index',
    'serad': 'sort', 'otoc': 'reverse',
    'klice': 'keys', 'hodnoty': 'values', 'polozky': 'items', 'ziskej': 'get',
    'sjednoceni': 'union', 'prunik': 'intersection', 'rozdil': 'difference',
    
    # METODY TEXTU
    'nahrad': 'replace', 'rozdel': 'split', 'spoj': 'join',
    'mala_pismena': 'lower', 'velka_pismena': 'upper', 'velke_prvni': 'capitalize',
    'orez': 'strip', 'vypln_nulami': 'zfill',
    'zacina_na': 'startswith', 'konci_na': 'endswith', 'najdi': 'find',
    'spocitej': 'count', 'je_cislo': 'isdigit', 'je_abecedni': 'isalpha'
}

with open(soubor, 'r', encoding='utf-8') as f:
    tokens = []
    for tok in tokenize.generate_tokens(f.readline):
        if tok.type == tokenize.NAME and tok.string in slovnik:
            tokens.append((tokenize.NAME, slovnik[tok.string]))
        elif tok.type == tokenize.STRING:
            val = tok.string
            if val.startswith('f') or val.startswith('F'):
                def repl_fstr(m):
                    inner = m.group(1)
                    for cz, py in slovnik.items():
                        inner = re.sub(r'\b' + cz + r'\b', py, inner)
                    return "{" + inner + "}"
                val = re.sub(r'\{([^{}]+)\}', repl_fstr, val)
            tokens.append((tokenize.STRING, val))
        else:
            tokens.append((tok.type, tok.string))

kod = tokenize.untokenize(tokens)

docasny_soubor = soubor.replace(".czpp", "_prelozeno.py")
with open(docasny_soubor, 'w', encoding='utf-8') as f:
    f.write(kod)

os.system(f"python {docasny_soubor}")
os.remove(docasny_soubor)
