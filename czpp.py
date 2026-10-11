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

# Náš obří slovník - tentokrát jako čistá slova (už žádné regex \b)
slovnik = {
    'vypis': 'print', 'vstup': 'input', 'delka': 'len', 'typ': 'type',
    'text': 'str', 'cele_cislo': 'int', 'desetinne': 'float', 
    'seznam': 'list', 'slovnik': 'dict', 'mnozina': 'set', 'pravdivost': 'bool',
    'komplexni': 'complex', 'bajty': 'bytes', 'pevna_mnozina': 'frozenset',
    
    'definuj': 'def', 'vrat': 'return', 'poskytni': 'yield', 
    'pokud': 'if', 'nebo_pokud': 'elif', 'jinak': 'else',
    'pro': 'for', 'v': 'in', 'dokud': 'while',
    'Pravda': 'True', 'Nepravda': 'False', 'Nic': 'None',
    'a': 'and', 'nebo': 'or', 'ne': 'not', 'neni': 'is not', 'je': 'is',
    
    'asynchronni': 'async', 'pockej': 'await', 'funkcicka': 'lambda',
    'nelokalni': 'nonlocal', 'globalni': 'global',
    
    'rozmezi': 'range', 'ocisluj': 'enumerate', 'zazipuj': 'zip',
    'vyfiltruj': 'filter', 'namapuj': 'map', 'vsechno': 'all', 'cokoliv': 'any',
    'zaokrouhli': 'round', 'absolutni': 'abs', 'minimum': 'min', 
    'maximum': 'max', 'soucet': 'sum', 'mocnina': 'pow', 'deleni_se_zbytkem': 'divmod',
    
    'vyhodnot': 'eval', 'spust': 'exec', 'obsah': 'dir', 
    'totoznost': 'id', 'otisk': 'hash', 'kod_znaku': 'ord', 'znak': 'chr',
    'globalni_promenne': 'globals', 'lokalni_promenne': 'locals',
    'ma_atribut': 'hasattr', 'ziskej_atribut': 'getattr', 'nastav_atribut': 'setattr',
    
    'trida': 'class', 'ja': 'self', 'rodic': 'super',
    'vlastnost': 'property', 'staticka_metoda': 'staticmethod', 'tridni_metoda': 'classmethod',
    '__zacatek__': '__init__', '__text__': '__str__', '__delka__': '__len__',
    '__secti__': '__add__', '__zavolej__': '__call__',
    
    'nacti': 'import', 'jako': 'as', 's': 'with',
    'smaz': 'del', 'tvrzeni': 'assert',
    'zkus': 'try', 'chyt': 'except', 'konecne': 'finally', 'vyvolej': 'raise',
    'preskoc': 'pass', 'prerus': 'break', 'pokracuj': 'continue',
    
    'pridej': 'append', 'rozsir': 'extend', 'vloz': 'insert', 
    'odeber': 'pop', 'vycisti': 'clear', 'najdi_index': 'index',
    'serad': 'sort', 'otoc': 'reverse',
    'klice': 'keys', 'hodnoty': 'values', 'polozky': 'items', 'ziskej': 'get',
    'sjednoceni': 'union', 'prunik': 'intersection', 'rozdil': 'difference',
    
    'nahrad': 'replace', 'rozdel': 'split', 'spoj': 'join',
    'mala_pismena': 'lower', 'velka_pismena': 'upper', 'velke_prvni': 'capitalize',
    'orez': 'strip', 'vypln_nulami': 'zfill',
    'zacina_na': 'startswith', 'konci_na': 'endswith', 'najdi': 'find',
    'spocitej': 'count', 'je_cislo': 'isdigit', 'je_abecedni': 'isalpha'
}

# Zpracujeme kod přes Tokenize (čte to jako opravdový Python)
with open(soubor, 'r', encoding='utf-8') as f:
    tokens = []
    for tok in tokenize.generate_tokens(f.readline):
        if tok.type == tokenize.NAME and tok.string in slovnik:
            # Tohle je regulérní příkaz (např. 'pokud' -> 'if')
            tokens.append((tokenize.NAME, slovnik[tok.string]))
        elif tok.type == tokenize.STRING:
            # Tohle je text v uvozovkách (na ten nesahej!)
            val = tok.string
            # ALE pokud je to f-string, musíme přeložit JEN proměnné uvnitř složených závorek {}
            if val.startswith('f') or val.startswith('F'):
                def repl_fstr(m):
                    inner = m.group(1)
                    for cz, py in slovnik.items():
                        inner = re.sub(r'\b' + cz + r'\b', py, inner)
                    return "{" + inner + "}"
                val = re.sub(r'\{([^{}]+)\}', repl_fstr, val)
            tokens.append((tokenize.STRING, val))
        else:
            # Zbytek (závorky, tečky, čísla) necháme jak je
            tokens.append((tok.type, tok.string))

# Složíme kód zpět dohromady
kod = tokenize.untokenize(tokens)

docasny_soubor = soubor.replace(".czpp", "_prelozeno.py")
with open(docasny_soubor, 'w', encoding='utf-8') as f:
    f.write(kod)

os.system(f"python {docasny_soubor}")
os.remove(docasny_soubor)
