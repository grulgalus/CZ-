import sys, os, re

if "--os" in sys.argv:
    sys.argv.remove("--os")
    soubor = sys.argv[1]
    
    with open(soubor, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    print("[⚙️] Krok 1: Analyzuji tvuj cz++ kod pro OS...")
    asm_kod = ["[BITS 16]", "[ORG 0x8000]", "start:", "    cld", "    xor ax, ax", "    mov ds, ax", "    mov es, ax"]
    data_sekce = []
    string_id = 0
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"): continue
        
        # PŘÍKAZ: vypis("text")
        if line.startswith("vypis("):
            try:
                text = line.split('"')[1]
                asm_kod.append("    mov dx, 0x3F8")
                asm_kod.append(f"    mov si, str_{string_id}")
                asm_kod.append("    call print_string")
                data_sekce.append(f'str_{string_id} db "{text}", 10, 13, 0')
                string_id += 1
            except: pass
                
        # PŘÍKAZ: vycisti() (Smaže obrazovku)
        elif line == "vycisti()":
            asm_kod.append("    mov dx, 0x3F8")
            asm_kod.append(f"    mov si, str_{string_id}")
            asm_kod.append("    call print_string")
            data_sekce.append(f'str_{string_id} db 27, "[2J", 27, "[H", 0')
            string_id += 1
            
        # PŘÍKAZ: cekej_na_klavesu() (Čeká na stisk klávesy ze sériového portu)
        elif line == "cekej_na_klavesu()":
            asm_kod.append("    call wait_key")
            
        # PŘÍKAZ: pipni() (Terminálový zvonek)
        elif line == "pipni()":
            asm_kod.append("    mov dx, 0x3F8")
            asm_kod.append("    mov al, 7")
            asm_kod.append("    out dx, al")
                
        # PŘÍKAZ: zastav()
        elif line == "zastav()":
            asm_kod.append("    cli")
            asm_kod.append("    hlt")

    asm_kod.extend([
        "    cli", "    hlt",
        "print_string:", "    cld", ".loop:", "    lodsb", "    or al, al", "    jz .done",
        "    out dx, al", "    jmp .loop", ".done:", "    ret",
        "wait_key:", "    mov dx, 0x3FD", ".wait:", "    in al, dx", "    test al, 1", "    jz .wait",
        "    mov dx, 0x3F8", "    in al, dx", "    ret"
    ])
    
    with open("jadro_auto.asm", "w", encoding="utf-8") as f:
        f.write("\n".join(asm_kod) + "\n\n" + "\n".join(data_sekce) + "\n\ntimes 2048-($-$$) db 0\n")

    print("[⚙️] Krok 2: Kompiluji cz++ do strojoveho kodu...")
    os.system("nasm -f bin jadro_auto.asm -o jadro.bin")
    
    bootloader_asm = """
[BITS 16]
[ORG 0x7C00]
    mov [BOOT_DRIVE], dl
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00
    mov dx, 0x3F8
    mov si, msg_boot
    call print_str
    mov ah, 0x00
    mov dl, [BOOT_DRIVE]
    int 0x13
    mov ah, 0x02
    mov al, 4
    mov ch, 0
    mov dh, 0
    mov cl, 2
    mov bx, 0x8000
    mov dl, [BOOT_DRIVE]
    int 0x13
    jmp 0:0x8000
print_str:
    cld
.loop:
    lodsb
    or al, al
    jz .done
    out dx, al
    jmp .loop
.done:
    ret
BOOT_DRIVE db 0
msg_boot db "[BOOT] Zacinam nacitat CZ++ jadro...", 10, 13, 0
times 510-($-$$) db 0
dw 0xAA55
"""
    with open("boot_auto.asm", "w") as f: f.write(bootloader_asm)
    os.system("nasm -f bin boot_auto.asm -o bootloader.bin")

    print("[⚙️] Krok 3: Sestavuji bezpecny diskovy obraz...")
    os.system("dd if=/dev/zero of=os.img bs=512 count=32 2>/dev/null")
    os.system("dd if=bootloader.bin of=os.img bs=512 conv=notrunc 2>/dev/null")
    os.system("dd if=jadro.bin of=os.img bs=512 seek=1 conv=notrunc 2>/dev/null")
    
    print("[🚀] ZAPINAM QEMU! TVUJ VLASTNI OS STARTUJE!\n")
    os.system("qemu-system-x86_64 -nographic -drive format=raw,file=os.img")
    sys.exit(0)

# (Tady by pokračoval tvůj stávající kód pro python režim)
