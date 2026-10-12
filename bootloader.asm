[BITS 16]
[ORG 0x7C00]

    ; 1. ZÁLOHA ČÍSLA DISKU (BIOS ho dává do DL, musíme si ho schovat!)
    mov [BOOT_DRIVE], dl

    ; 2. Inicializace stacku
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    ; 3. Tisk na sériový port (tohle zničí DX, proto ta záloha výše!)
    mov dx, 0x3F8
    mov si, msg_boot
    call print_string

    ; 4. Cteni sektoru 2 (Nase jadro)
    mov ah, 0x02       ; Povel pro cteni
    mov al, 1          ; Pocet sektoru
    mov ch, 0          ; Valec 0
    mov dh, 0          ; Hlavicka 0
    mov cl, 2          ; Sektor 2
    mov bx, 0x8000     ; Cilova adresa v RAM
    mov dl, [BOOT_DRIVE] ; !!! OBNOVENÍ SPRAVNÉHO ČÍSLA DISKU !!!
    
    int 0x13           ; ZAVOLEJ BIOS!
    jc disk_error      ; Skok pri chybe

    ; 5. Tisk a Skok na Jádro
    mov dx, 0x3F8
    mov si, msg_ok
    call print_string
    jmp 0x8000

print_string:
    lodsb
    or al, al
    jz .done
    out dx, al
    jmp print_string
.done:
    ret

disk_error:
    mov dx, 0x3F8
    mov si, msg_err
    call print_string
    cli
    hlt

; --- Proměnné a texty ---
BOOT_DRIVE db 0
msg_boot db "[BOOT] Jsem v Sektoru 1. Hledam OS jadro...", 10, 13, 0
msg_ok   db "[BOOT] Jadro precteno z disku do RAM! Skacu na 0x8000!", 10, 13, 0
msg_err  db "[BOOT] CHYBA: Nelze cist disk!", 10, 13, 0

times 510-($-$$) db 0
dw 0xAA55
