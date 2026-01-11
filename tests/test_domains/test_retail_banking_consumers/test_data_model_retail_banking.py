import pytest

from tau2.domains.retail_banking_consumers.data_model import (
    Account,
    Card,
    Customer,
    RetailBankingDB,
)


@pytest.fixture
def sample_db() -> RetailBankingDB:
    """Create a sample database for testing."""
    return RetailBankingDB(
        customers={
            "cus_01": Customer(full_name="Dylan Parker"),
            "cus_02": Customer(full_name="Sarah Johnson"),
        },
        accounts={
            "acc_01": Account(
                account_number="07895034807",
                customer_id="cus_01",
                associated_products=["fp_01"],
            ),
            "acc_02": Account(
                account_number="12345678901",
                customer_id="cus_02",
                associated_products=["fp_02"],
            ),
        },
        cards={
            "fp_01": Card(
                customer_id="cus_01",
                type="credit_card",
                card_number="342979928736417",
                currency="USD",
                available_credit=2900.0,
            ),
            "fp_02": Card(
                customer_id="cus_02",
                type="debit_card",
                card_number="450012345678901",
                currency="USD",
                available_credit=5000.0,
            ),
        },
    )


class TestCustomer:
    """Test Customer data model."""

    def test_customer_creation(self):
        customer = Customer(full_name="John Doe")
        assert customer.full_name == "John Doe"

    def test_customer_in_db(self, sample_db: RetailBankingDB):
        assert "cus_01" in sample_db.customers
        assert sample_db.customers["cus_01"].full_name == "Dylan Parker"


class TestAccount:
    """Test Account data model."""

    def test_account_creation(self):
        account = Account(
            account_number="123456789",
            customer_id="cus_01",
            associated_products=["fp_01"],
        )
        assert account.account_number == "123456789"
        assert account.customer_id == "cus_01"
        assert len(account.associated_products) == 1

    def test_account_without_products(self):
        account = Account(
            account_number="987654321",
            customer_id="cus_02",
        )
        assert len(account.associated_products) == 0

    def test_account_in_db(self, sample_db: RetailBankingDB):
        assert "acc_01" in sample_db.accounts
        account = sample_db.accounts["acc_01"]
        assert account.account_number == "07895034807"
        assert account.customer_id == "cus_01"
        assert "fp_01" in account.associated_products


class TestCard:
    """Test Card data model."""

    def test_credit_card_creation(self):
        card = Card(
            customer_id="cus_01",
            type="credit_card",
            card_number="1234567890123456",
            currency="USD",
            available_credit=5000.0,
        )
        assert card.type == "credit_card"
        assert card.card_number == "1234567890123456"
        assert card.available_credit == 5000.0
        assert card.currency == "USD"

    def test_debit_card_creation(self):
        card = Card(
            customer_id="cus_02",
            type="debit_card",
            card_number="9876543210987654",
            currency="EUR",
            available_credit=1500.0,
        )
        assert card.type == "debit_card"
        assert card.currency == "EUR"

    def test_card_in_db(self, sample_db: RetailBankingDB):
        assert "fp_01" in sample_db.cards
        card = sample_db.cards["fp_01"]
        assert card.customer_id == "cus_01"
        assert card.type == "credit_card"
        assert card.available_credit == 2900.0


class TestRetailBankingDB:
    """Test RetailBankingDB data model."""

    def test_db_creation(self, sample_db: RetailBankingDB):
        assert len(sample_db.customers) == 2
        assert len(sample_db.accounts) == 2
        assert len(sample_db.cards) == 2

    def test_db_statistics(self, sample_db: RetailBankingDB):
        stats = sample_db.get_statistics()
        assert stats["num_customers"] == 2
        assert stats["num_accounts"] == 2
        assert stats["num_cards"] == 2

    def test_db_hash(self, sample_db: RetailBankingDB):
        hash1 = sample_db.get_hash()
        assert isinstance(hash1, str)
        assert len(hash1) > 0

        # Same database should produce same hash
        hash2 = sample_db.get_hash()
        assert hash1 == hash2

    def test_db_json_schema(self, sample_db: RetailBankingDB):
        schema = sample_db.get_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "customers" in schema["properties"]
        assert "accounts" in schema["properties"]
        assert "cards" in schema["properties"]

    def test_empty_db(self):
        empty_db = RetailBankingDB(customers={}, accounts={}, cards={})
        stats = empty_db.get_statistics()
        assert stats["num_customers"] == 0
        assert stats["num_accounts"] == 0
        assert stats["num_cards"] == 0


class TestDatabasePersistence:
    """Test database load/dump functionality."""

    def test_load_from_file(self):
        """Test loading database from actual db.json file."""
        from tau2.domains.retail_banking_consumers.data_model import get_db

        db = get_db()
        assert isinstance(db, RetailBankingDB)
        assert len(db.customers) > 0
        assert len(db.accounts) > 0
        assert len(db.cards) > 0

    def test_dump_and_load(self, sample_db: RetailBankingDB, tmp_path):
        """Test dumping and loading database to/from file."""
        import json

        # Dump to temporary file
        temp_file = tmp_path / "test_db.json"
        sample_db.dump(str(temp_file))

        # Verify file exists and is valid JSON
        assert temp_file.exists()
        with open(temp_file) as f:
            data = json.load(f)
        assert "customers" in data
        assert "accounts" in data
        assert "cards" in data

        # Load from file and verify
        loaded_db = RetailBankingDB.load(str(temp_file))
        assert len(loaded_db.customers) == len(sample_db.customers)
        assert len(loaded_db.accounts) == len(sample_db.accounts)
        assert len(loaded_db.cards) == len(sample_db.cards)

        # Verify data integrity
        assert loaded_db.customers["cus_01"].full_name == "Dylan Parker"
        assert loaded_db.accounts["acc_01"].account_number == "07895034807"
        assert loaded_db.cards["fp_01"].available_credit == 2900.0


class TestDataRelationships:
    """Test relationships between entities."""

    def test_customer_account_relationship(self, sample_db: RetailBankingDB):
        """Test that accounts correctly reference customers."""
        account = sample_db.accounts["acc_01"]
        customer = sample_db.customers[account.customer_id]
        assert customer.full_name == "Dylan Parker"

    def test_account_card_relationship(self, sample_db: RetailBankingDB):
        """Test that cards are correctly associated with accounts."""
        account = sample_db.accounts["acc_01"]
        assert "fp_01" in account.associated_products

        card = sample_db.cards["fp_01"]
        assert card.customer_id == account.customer_id

    def test_all_cards_have_valid_customers(self, sample_db: RetailBankingDB):
        """Test that all cards reference existing customers."""
        for card_id, card in sample_db.cards.items():
            assert card.customer_id in sample_db.customers

    def test_all_accounts_have_valid_customers(self, sample_db: RetailBankingDB):
        """Test that all accounts reference existing customers."""
        for account_id, account in sample_db.accounts.items():
            assert account.customer_id in sample_db.customers
