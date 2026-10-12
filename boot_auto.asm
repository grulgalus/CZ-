
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
    
    ; BEZPEČNOST: Tvrdý reset řadiče disku před čtením!
    mov ah, 0x00
    mov dl, [BOOT_DRIVE]
    int 0x13
    
    ; Čtení 4 sektorů (2048 bajtů = naše jádro)
    mov ah, 0x02
    mov al, 4
    mov ch, 0
    mov dh, 0
    mov cl, 2
    mov bx, 0x8000
    mov dl, [BOOT_DRIVE]
    int 0x13
    jc disk_error
    
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

disk_error:
    mov dx, 0x3F8
    mov si, msg_err
    call print_str
    cli
    hlt

BOOT_DRIVE db 0
msg_boot db "[BOOT] Zacinam nacitat CZ++ jadro...", 10, 13, 0
msg_err  db "[BOOT] KRITICKA CHYBA DISKU!", 10, 13, 0
times 510-($-$$) db 0
dw 0xAA55
