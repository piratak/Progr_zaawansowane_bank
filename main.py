import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Listbox, END, Button
import sqlite3

class BankDB:
    def __init__(self, db_name="bank.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS konta (
                               numer_konta INTEGER PRIMARY KEY AUTOINCREMENT,
                               stan_konta REAL NOT NULL)''')
        self.conn.commit()

    def dodaj_konto(self, stan_konta):
        self.cursor.execute('INSERT INTO konta (stan_konta) VALUES (?)', (stan_konta,))
        self.conn.commit()
        return self.cursor.lastrowid

    def usun_konto(self, numer_konta):
        self.cursor.execute('DELETE FROM konta WHERE numer_konta = ?', (numer_konta,))
        self.conn.commit()

    def zmien_stan_konta(self, numer_konta, kwota):
        self.cursor.execute('UPDATE konta SET stan_konta = stan_konta + ? WHERE numer_konta = ?', (kwota, numer_konta))
        self.conn.commit()

    def podglad_konta(self, numer_konta):
        self.cursor.execute('SELECT stan_konta FROM konta WHERE numer_konta = ?', (numer_konta,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def wszystkie_konta(self):
        self.cursor.execute('SELECT numer_konta, stan_konta FROM konta')
        return self.cursor.fetchall()

class Bank:
    def __init__(self, db):
        self.db = db

    def dodaj_konto(self, stan_konta):
        return self.db.dodaj_konto(stan_konta)

    def usun_konto(self, numer_konta):
        self.db.usun_konto(numer_konta)

    def zmien_stan_konta(self, numer_konta, kwota):
        self.db.zmien_stan_konta(numer_konta, kwota)

    def podglad_konta(self, numer_konta):
        return self.db.podglad_konta(numer_konta)

    def wszystkie_konta(self):
        return self.db.wszystkie_konta()

class DialogWplacPieniadze:
    def __init__(self, bank, root):
        self.bank = bank
        self.root = root

    def wykonaj(self):
        numer_konta = simpledialog.askinteger("Wpłata pieniędzy", "Podaj numer konta:", parent=self.root)
        kwota = simpledialog.askfloat("Wpłata pieniędzy", "Podaj kwotę wpłaty:", parent=self.root)
        if numer_konta and kwota and kwota > 0:
            self.bank.zmien_stan_konta(numer_konta, kwota)
            messagebox.showinfo("Wpłata zakończona", "Wpłata została zakończona pomyślnie.", parent=self.root)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy numer konta lub kwota.", parent=self.root)

class DialogWyplacPieniadze:
    def __init__(self, bank, root):
        self.bank = bank
        self.root = root

    def wykonaj(self):
        numer_konta = simpledialog.askinteger("Wypłata pieniędzy", "Podaj numer konta:", parent=self.root)
        kwota = simpledialog.askfloat("Wypłata pieniędzy", "Podaj kwotę wypłaty:", parent=self.root)
        if numer_konta and kwota and kwota > 0:
            self.bank.zmien_stan_konta(numer_konta, -kwota)
            messagebox.showinfo("Wypłata zakończona", "Wypłata została zakończona pomyślnie.", parent=self.root)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy numer konta lub kwota.", parent=self.root)

class DialogPodgladKonta:
    def __init__(self, bank, root):
        self.bank = bank
        self.root = root

    def wykonaj(self):
        numer_konta = simpledialog.askinteger("Podgląd konta", "Podaj numer konta:", parent=self.root)
        stan_konta = self.bank.podglad_konta(numer_konta)
        if stan_konta is not None:
            messagebox.showinfo("Stan konta", f"Stan konta: {stan_konta}", parent=self.root)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy numer konta.", parent=self.root)

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

        konta = self.bank.wszystkie_konta()
        for numer_konta, stan_konta in konta:
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
        tk.Button(self.root, text="Wpłać pieniądze", command=lambda: DialogWplacPieniadze(self.bank, self.root).wykonaj()).pack(fill=tk.X)
        tk.Button(self.root, text="Wypłać pieniądze", command=lambda: DialogWyplacPieniadze(self.bank, self.root).wykonaj()).pack(fill=tk.X)
        tk.Button(self.root, text="Podgląd konta", command=lambda: DialogPodgladKonta(self.bank, self.root).wykonaj()).pack(fill=tk.X)
        tk.Button(self.root, text="Usuń konto", command=self.usun_konto).pack(fill=tk.X)
        tk.Button(self.root, text="Wyjście", command=self.root.quit).pack(fill=tk.X)

    def stworz_konto(self):
        stan_konta = simpledialog.askfloat("Stan konta", "Podaj początkowy stan konta:", parent=self.root)
        if stan_konta is not None and stan_konta >= 0:
            numer_konta = self.bank.dodaj_konto(stan_konta)
            messagebox.showinfo("Konto utworzone", f"Numer konta: {numer_konta}\nStan konta: {stan_konta}", parent=self.root)
        else:
            messagebox.showwarning("Anulowano", "Tworzenie konta zostało anulowane.", parent=self.root)

    def podglad_wszystkich_kont(self):
        ListaKontWindow(self.bank, self.root).show()

    def usun_konto(self):
        numer_konta = simpledialog.askinteger("Usuń konto", "Podaj numer konta do usunięcia:", parent=self.root)
        if numer_konta:
            self.bank.usun_konto(numer_konta)
            messagebox.showinfo("Usuwanie konta", "Konto zostało usunięte.", parent=self.root)
        else:
            messagebox.showwarning("Anulowano", "Usuwanie konta zostało anulowane.", parent=self.root)

if __name__ == "__main__":
    db = BankDB()
    bank = Bank(db)
    root = tk.Tk()
    app = BankApp(root, bank)
    root.mainloop()
