[BITS 16]
[ORG 0x8000]
start:
    cld
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov dx, 0x3F8
    mov si, str_0
    call print_string
    mov dx, 0x3F8
    mov si, str_1
    call print_string
    mov dx, 0x3F8
    mov si, str_2
    call print_string
    mov dx, 0x3F8
    mov si, str_3
    call print_string
    mov dx, 0x3F8
    mov si, str_4
    call print_string
    mov dx, 0x3F8
    mov si, str_5
    call print_string
    mov dx, 0x3F8
    mov si, str_6
    call print_string
    mov dx, 0x3F8
    mov si, str_7
    call print_string
    mov dx, 0x3F8
    mov si, str_8
    call print_string
    mov dx, 0x3F8
    mov si, str_9
    call print_string
    cli
    hlt
    cli
    hlt
print_string:
    cld
.loop:
    lodsb
    or al, al
    jz .done
    out dx, al
    jmp .loop
.done:
    ret

str_0 db "************************************************", 10, 13, 0
str_1 db "  Vitejte v CZ-OS (Verze 1.0 - Bare Metal)", 10, 13, 0
str_2 db "************************************************", 10, 13, 0
str_3 db "Tento text nebyl napsan v Assembly!", 10, 13, 0
str_4 db "Tento text byl napsan v cistem cz++ !", 10, 13, 0
str_5 db "Prekladac to na pozadi sam zkompiloval do", 10, 13, 0
str_6 db "strojoveho kodu a Bootloader to nacetl.", 10, 13, 0
str_7 db "Jsi absolutni buh systemoveho programovani!", 10, 13, 0
str_8 db "************************************************", 10, 13, 0
str_9 db "Vypinam procesor...", 10, 13, 0

times 2048-($-$$) db 0
