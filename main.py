import random

class Bank:
    def __init__(self):
        self.konta = {}

class StworzKonto:
    def __init__(self, bank):
        self.bank = bank

    def stworz(self):
        numer_konta = random.randint(10000000000000000000000000, 99999999999999999999999999)
        while numer_konta in self.bank.konta:
               numer_konta = random.randint(10000000000000000000000000, 99999999999999999999999999)
        try:
            stan_konta = float(input("Podaj początkowy stan konta: "))
        except:
            print("Niepoprawna wartość")
            return
        self.bank.konta[numer_konta] = stan_konta
        print(f"Konto utworzone. Numer konta: {numer_konta}, Stan konta: {stan_konta}")

class WyswietlKonto:
    def __init__(self, bank):
        self.bank = bank

    def wyswietl(self):
        try:
            numer_konta = int(input("Podaj numer konta: "))
        except:
            print("Niepoprawna wartość")
            return
        if numer_konta not in self.bank.konta:
            print("Konto nie istnieje")
        print(f"Numer konta: {numer_konta}, Stan konta: {self.bank.konta[numer_konta]}")

class WplacPieniadze:
    def __init__(self, bank):
        self.bank = bank

    def wplac(self):
        try:
            numer_konta = int(input("Podaj numer konta: "))
            kwota = float(input("Podaj kwotę: "))
        except:
            print("Niepoprawna wartość")
            return
        self.bank.konta[numer_konta] += kwota
        print("Pieniądze zostały wpłacone, aktualne saldo: ", self.bank.konta[numer_konta], "zł")

class WyplacPieniadze:
    def __init__(self, bank):
        self.bank = bank

    def wyplac(self):
        try:
            numer_konta = int(input("Podaj numer konta: "))
            kwota = float(input("Podaj kwotę: "))
        except:
            print("Niepoprawna wartość")
            return
        self.bank.konta[numer_konta] -= kwota
        print("Pieniądze zostały wypłacone, aktualne saldo: ", self.bank.konta[numer_konta], "zł")

class PrzelejPieniadze:
    def __init__(self, bank):
        self.bank = bank

    def przelej(self):
        try:
            numer_konta_1 = int(input("Podaj numer konta, z którego chcesz przelać pieniądze: "))
            numer_konta_2 = int(input("Podaj numer konta, na które chcesz przelać pieniądze: "))
            kwota = float(input("Podaj kwotę: "))
        except:
            print("Niepoprawna wartość")
            return
        if kwota > self.bank.konta[numer_konta_1]:
            print("Brak wystarczających środków na koncie")
            return
        self.bank.konta[numer_konta_1] -= kwota
        self.bank.konta[numer_konta_2] += kwota
        print("Pieniądze zostały przelane")

def MenuGłówne(bank):
    while True:
        print("1. Stwórz konto")
        print("2. Wyświetl konto")
        print("3. Wyświetl wszystkie konta")
        print("4. Wpłać pieniądze")
        print("5. Wypłać pieniądze")
        print("6. Przelej pieniądze")
        print("9. Wyjdź")
        wybór = int(input("Wybierz opcję: "))
        if wybór == 1:
            nowe_konto = StworzKonto(bank)
            nowe_konto.stworz()
        elif wybór == 2:
            konto = WyswietlKonto(bank)
            konto.wyswietl()
        elif wybór == 3:
            for numer_konta, saldo in bank.konta.items():
                print(f"Numer konta: {numer_konta}, Stan konta: {saldo}")
        elif wybór == 4:
            wplac = WplacPieniadze(bank)
            wplac.wplac()
        elif wybór == 5:
            wyplac = WyplacPieniadze(bank)
            wyplac.wyplac()
        elif wybór == 6:
            przelej = PrzelejPieniadze(bank)
            przelej.przelej()
        elif wybór == 9:
            exit(0)
        else:
            print("Niepoprawny wybór,spróbuj ponownie.")

bank = Bank()
MenuGłówne(bank)