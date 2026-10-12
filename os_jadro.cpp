#include <iostream>
using namespace std;

int main() {
    cout << "========================================" << endl;
    cout << "🔥 cz++ KOMPILOVANY BARE-METAL REZIM 🔥" << endl;
    cout << "========================================" << endl;
    
    int pamet = 1024;
    char verze = 'A';
    
    cout << "Nacitam hardware procesoru..." << endl;
    cout << "Dostupna pamet RAM: " << pamet << " MB" << endl;
    
    int pocitadlo = 0;
    while (pocitadlo < 3) {
        cout << "Startuji jadro systemu (Boot " << pocitadlo << ")..." << endl;
        pocitadlo = pocitadlo + 1;
    }
    
    cout << "Systemove jadro nacteno!" << endl;
    return 0;
}
