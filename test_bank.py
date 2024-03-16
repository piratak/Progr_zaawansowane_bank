import pytest
from main import BankDB, Bank

@pytest.fixture
def test_db():
    """Fixture to set up the database for testing."""
    test_db = BankDB(":memory:")
    yield test_db
    test_db.conn.close()

@pytest.fixture
def test_bank(test_db):
    """Fixture to set up the bank object for testing."""
    return Bank(test_db)

def test_dodaj_konto(test_bank):
    numer_konta = test_bank.dodaj_konto(100.0)
    assert numer_konta is not None
    assert test_bank.podglad_konta(numer_konta) == 100.0

def test_usun_konto(test_bank):
    numer_konta = test_bank.dodaj_konto(50.0)
    test_bank.usun_konto(numer_konta)
    assert test_bank.podglad_konta(numer_konta) is None

@pytest.mark.parametrize("initial_balance, deposit_amount, expected_balance", [
    (100.0, 50.0, 150.0),
    (200.0, -100.0, 100.0),
])
def test_zmien_stan_konta(test_bank, initial_balance, deposit_amount, expected_balance):
    numer_konta = test_bank.dodaj_konto(initial_balance)
    test_bank.zmien_stan_konta(numer_konta, deposit_amount)
    assert test_bank.podglad_konta(numer_konta) == expected_balance

def test_wszystkie_konta(test_bank):
    numer_konta1 = test_bank.dodaj_konto(100.0)
    numer_konta2 = test_bank.dodaj_konto(200.0)
    konta = test_bank.wszystkie_konta()
    assert len(konta) == 2
    assert konta[0][0] == numer_konta1 and konta[0][1] == 100.0
    assert konta[1][0] == numer_konta2 and konta[1][1] == 200.0

if __name__ == "__main__":
    pytest.main()
