import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Listbox, END, Button
import random

class Bank:
    def __init__(self):
        self.konta = {}

    def dodaj_konto(self, numer_konta, stan_konta):
        if numer_konta in self.konta:
            raise ValueError("Konto o tym numerze już istnieje.")
        self.konta[numer_konta] = stan_konta

    def usun_konto(self, numer_konta):
        if numer_konta not in self.konta:
            raise ValueError("Konto nie istnieje.")
        del self.konta[numer_konta]

    def wplac_pieniadze(self, numer_konta, kwota):
        if numer_konta not in self.konta:
            raise ValueError("Konto nie istnieje.")
        if kwota <= 0:
            raise ValueError("Kwota wpłaty musi być większa od zera.")
        self.konta[numer_konta] += kwota

    def wyplac_pieniadze(self, numer_konta, kwota):
        if numer_konta not in self.konta or self.konta[numer_konta] < kwota:
            raise ValueError("Niewystarczające środki na koncie lub konto nie istnieje.")
        self.konta[numer_konta] -= kwota

    def podglad_konta(self, numer_konta):
        if numer_konta not in self.konta:
            raise ValueError("Konto nie istnieje.")
        return self.konta[numer_konta]

class DialogStworzKonto:
    def __init__(self, bank, root):
        self.bank = bank
        self.root = root

    def wykonaj(self):
        numer_konta = random.randint(10000000000000000000000000, 99999999999999999999999999)
        stan_konta = simpledialog.askfloat("Stan konta", "Podaj początkowy stan konta:", parent=self.root)
        if stan_konta is not None and stan_konta >= 0:
            try:
                self.bank.dodaj_konto(numer_konta, stan_konta)
                messagebox.showinfo("Konto utworzone", f"Numer konta: {numer_konta}\nStan konta: {stan_konta}", parent=self.root)
            except ValueError as e:
                messagebox.showerror("Błąd", str(e), parent=self.root)
        else:
            messagebox.showwarning("Anulowano", "Tworzenie konta zostało anulowane.", parent=self.root)

class DialogOperacjaPieniezna:
    def __init__(self, bank, root, title, wypłata=False):
        self.bank = bank
        self.root = root
        self.title = title
        self.wypłata = wypłata

    def wykonaj(self):
        numer_konta = simpledialog.askinteger(self.title, "Podaj numer konta:", parent=self.root)
        if numer_konta is None:
            messagebox.showwarning("Anulowano", "Operacja została anulowana.", parent=self.root)
            return
        kwota = simpledialog.askfloat(self.title, "Podaj kwotę:", parent=self.root)
        if kwota is None or kwota <= 0:
            messagebox.showwarning("Anulowano", "Operacja została anulowana lub podano nieprawidłową kwotę.", parent=self.root)
            return
        try:
            if self.wypłata:
                self.bank.wyplac_pieniadze(numer_konta, kwota)
            else:
                self.bank.wplac_pieniadze(numer_konta, kwota)
            messagebox.showinfo(self.title, "Operacja zakończona sukcesem", parent=self.root)
        except ValueError as e:
            messagebox.showerror("Błąd", str(e), parent=self.root)

class DialogUsunKonto:
    def __init__(self, bank, root):
        self.bank = bank
        self.root = root

    def wykonaj(self):
        numer_konta = simpledialog.askinteger("Usuń konto", "Podaj numer konta do usunięcia:", parent=self.root)
        if numer_konta is None:
            messagebox.showwarning("Anulowano", "Usuwanie konta zostało anulowane.", parent=self.root)
            return
        try:
            self.bank.usun_konto(numer_konta)
            messagebox.showinfo("Usuwanie konta", "Konto zostało usunięte.", parent=self.root)
        except ValueError as e:
            messagebox.showerror("Błąd", str(e), parent=self.root)

class ListaKontWindow:
    def __init__(self, bank, root):
        self.bank = bank
        self.root = root

    def show(self):
        window = Toplevel(self.root)
        window.title("Lista kont")

        lb = Listbox(window, width=50, height=15)
        lb.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(window, orient="vertical")
        scrollbar.config(command=lb.yview)
        scrollbar.pack(side="right", fill="y")

        lb.config(yscrollcommand=scrollbar.set)

        for numer_konta, stan_konta in self.bank.konta.items():
            lb.insert(END, f"Numer konta: {numer_konta}, Stan konta: {stan_konta}")

        Button(window, text="Zamknij", command=window.destroy).pack(pady=5)


class BankApp:
    def __init__(self, root, bank):
        self.bank = bank
        self.root = root
        self.root.title("BankApp")
        self.setup_ui()

    def setup_ui(self):
        tk.Button(self.root, text="Stwórz konto", command=self.stworz_konto).pack(fill=tk.X)
        tk.Button(self.root, text="Podgląd wszystkich kont", command=self.podglad_wszystkich_kont).pack(fill=tk.X)
        tk.Button(self.root, text="Wpłać pieniądze", command=lambda: DialogOperacjaPieniezna(self.bank, self.root, "Wpłata").wykonaj()).pack(fill=tk.X)
        tk.Button(self.root, text="Wypłać pieniądze", command=lambda: DialogOperacjaPieniezna(self.bank, self.root, "Wypłata", True).wykonaj()).pack(fill=tk.X)
        tk.Button(self.root, text="Usuń konto", command=lambda: DialogUsunKonto(self.bank, self.root).wykonaj()).pack(fill=tk.X)
        tk.Button(self.root, text="Wyjście", command=self.root.quit).pack(fill=tk.X)

    def stworz_konto(self):
        DialogStworzKonto(self.bank, self.root).wykonaj()

    def podglad_wszystkich_kont(self):
        ListaKontWindow(self.bank, self.root).show()

    def usun_konto(self):
        DialogUsunKonto(self.bank, self.root).wykonaj()

if __name__ == "__main__":
    root = tk.Tk()
    bank = Bank()
    app = BankApp(root, bank)
    root.mainloop()
