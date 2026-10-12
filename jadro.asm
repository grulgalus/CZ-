[BITS 16]
[ORG 0x8000]       ; Tady jsme pristali z bootloaderu!

main:
    mov dx, 0x3F8
    mov si, msg_jadro
    call print_string
    cli
    hlt

print_string:
    lodsb
    or al, al
    jz .done
    out dx, al
    jmp print_string
.done:
    ret

msg_jadro:
    db 10, 13
    db "==================================================", 10, 13
    db " 🔥 SYROVE JADRO ZKOMPILOVANE Z CZ++ BEZI! 🔥", 10, 13
    db "==================================================", 10, 13
    db "[JADRO] Jsem na adrese 0x8000 a ridim procesor.", 10, 13
    db "[JADRO] Bootloader me fyzicky nacetl z disku!", 10, 13
    db "[JADRO] Zadny Linux. Zadny Python. Jen Ty a Procesor.", 10, 13
    db "==================================================", 10, 13
    db "(Pro ukonceni stiskni: Ctrl+A a pak klavesu X)", 10, 13, 0

times 512-($-$$) db 0
