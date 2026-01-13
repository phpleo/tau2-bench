"""Tests for customer authentication in the retail banking consumers domain."""

import pytest

from tau2.domains.retail_banking_consumers.data_model import (
    Account,
    Card,
    Customer,
    RetailBankingDB,
)
from tau2.domains.retail_banking_consumers.tools import RetailBankingTools


@pytest.fixture
def retail_banking_db_with_auth() -> RetailBankingDB:
    """Create a sample retail banking database with authentication data for testing."""
    return RetailBankingDB(
        customers={
            "cus_01": Customer(
                full_name="Dylan Parker",
                customer_login_id="45682409"
            ),
            "cus_02": Customer(
                full_name="Sarah Johnson",
                customer_login_id="87654321"
            ),
            "cus_03": Customer(
                full_name="Michael Chen",
                customer_login_id="11223344"
            ),
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
            "acc_03": Account(
                account_number="99887766554",
                customer_id="cus_03",
                associated_products=["fp_03"],
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
            "fp_03": Card(
                customer_id="cus_03",
                type="credit_card",
                card_number="371449635398431",
                currency="EUR",
                available_credit=3500.0,
            ),
        },
    )


@pytest.fixture
def tools(retail_banking_db_with_auth: RetailBankingDB) -> RetailBankingTools:
    """Create a RetailBankingTools instance with the test database."""
    return RetailBankingTools(retail_banking_db_with_auth)


class TestCustomerAuthentication:
    """Test suite for customer authentication functionality."""

    def test_authenticate_customer_success(self, tools: RetailBankingTools):
        """Test successful customer authentication with valid login ID."""
        result = tools.authenticate_customer("45682409")
        
        assert result is not None
        assert result["customer_id"] == "cus_01"
        assert result["full_name"] == "Dylan Parker"
        assert result["customer_login_id"] == "45682409"

    def test_authenticate_customer_multiple_customers(self, tools: RetailBankingTools):
        """Test authentication works correctly for different customers."""
        # Authenticate first customer
        result1 = tools.authenticate_customer("45682409")
        assert result1["customer_id"] == "cus_01"
        assert result1["full_name"] == "Dylan Parker"
        
        # Authenticate second customer
        result2 = tools.authenticate_customer("87654321")
        assert result2["customer_id"] == "cus_02"
        assert result2["full_name"] == "Sarah Johnson"
        
        # Authenticate third customer
        result3 = tools.authenticate_customer("11223344")
        assert result3["customer_id"] == "cus_03"
        assert result3["full_name"] == "Michael Chen"

    def test_authenticate_customer_invalid_login_id(self, tools: RetailBankingTools):
        """Test authentication fails with invalid login ID."""
        with pytest.raises(ValueError) as exc_info:
            tools.authenticate_customer("wrong_id")
        
        assert "Customer with login ID wrong_id not found" in str(exc_info.value)
        assert "Please verify the login ID and try again" in str(exc_info.value)

    def test_authenticate_customer_empty_login_id(self, tools: RetailBankingTools):
        """Test authentication fails with empty login ID."""
        with pytest.raises(ValueError) as exc_info:
            tools.authenticate_customer("")
        
        assert "not found" in str(exc_info.value)

    def test_authenticate_customer_numeric_string(self, tools: RetailBankingTools):
        """Test authentication works with numeric string login IDs."""
        # All login IDs are numeric strings
        result = tools.authenticate_customer("45682409")
        assert result["customer_login_id"] == "45682409"
        
        # Ensure it's treated as string, not integer
        assert isinstance(result["customer_login_id"], str)

    def test_authenticate_customer_returns_complete_info(self, tools: RetailBankingTools):
        """Test that authentication returns all required customer information."""
        result = tools.authenticate_customer("45682409")
        
        # Check all required fields are present
        assert "customer_id" in result
        assert "full_name" in result
        assert "customer_login_id" in result
        
        # Ensure no extra fields are returned (for security)
        assert len(result) == 3

    def test_authenticate_customer_case_sensitive(self, tools: RetailBankingTools):
        """Test that login IDs use exact string matching."""
        # Current implementation uses exact match
        result = tools.authenticate_customer("45682409")
        assert result["customer_id"] == "cus_01"
        
        # Since login IDs are numeric strings, case conversion doesn't apply
        # This test documents that exact matching is used
        assert result["customer_login_id"] == "45682409"


class TestAuthenticationIntegration:
    """Integration tests for authentication in the context of other operations."""

    def test_authentication_before_card_operations(
        self, tools: RetailBankingTools
    ):
        """Test that authentication provides the customer_id needed for other operations."""
        # Authenticate first
        auth_result = tools.authenticate_customer("45682409")
        customer_id = auth_result["customer_id"]
        
        # Use customer_id to list their cards
        cards = tools.list_cards(customer_id)
        
        assert len(cards) == 1
        assert cards[0]["card_id"] == "fp_01"
        # Note: list_cards doesn't return customer_id, only card information

    def test_authentication_provides_correct_customer_context(
        self, tools: RetailBankingTools
    ):
        """Test that each authenticated customer gets their own data."""
        # Authenticate customer 1
        auth1 = tools.authenticate_customer("45682409")
        cards1 = tools.list_cards(auth1["customer_id"])
        
        # Authenticate customer 2
        auth2 = tools.authenticate_customer("87654321")
        cards2 = tools.list_cards(auth2["customer_id"])
        
        # Ensure they have different cards
        assert cards1[0]["card_id"] != cards2[0]["card_id"]
        assert cards1[0]["card_number"] != cards2[0]["card_number"]

    def test_full_workflow_with_authentication(
        self, tools: RetailBankingTools
    ):
        """Test a complete workflow: authenticate, list cards, check credit."""
        # Step 1: Authenticate
        auth_result = tools.authenticate_customer("45682409")
        assert auth_result["full_name"] == "Dylan Parker"
        
        # Step 2: List customer's cards
        customer_id = auth_result["customer_id"]
        cards = tools.list_cards(customer_id)
        assert len(cards) == 1
        
        # Step 3: Check available credit on the card
        card_id = cards[0]["card_id"]
        credit_info = tools.get_current_available_credit(card_id)
        
        assert credit_info["available_credit"] == 2900.0
        assert credit_info["currency"] == "USD"
        assert credit_info["card_number"].endswith("6417")


class TestAuthenticationDataModel:
    """Tests for the Customer data model with authentication fields."""

    def test_customer_has_login_id_field(self):
        """Test that Customer model includes customer_login_id field."""
        customer = Customer(
            full_name="Test User",
            customer_login_id="12345678"
        )
        
        assert customer.full_name == "Test User"
        assert customer.customer_login_id == "12345678"

    def test_customer_login_id_is_required(self):
        """Test that customer_login_id is a required field."""
        with pytest.raises(Exception):  # Pydantic will raise ValidationError
            Customer(full_name="Test User")  # Missing customer_login_id

    def test_database_loads_with_login_ids(self, retail_banking_db_with_auth: RetailBankingDB):
        """Test that database correctly loads customers with login IDs."""
        db = retail_banking_db_with_auth
        
        # Check all customers have login IDs
        for customer_id, customer in db.customers.items():
            assert hasattr(customer, "customer_login_id")
            assert customer.customer_login_id is not None
            assert len(customer.customer_login_id) > 0

    def test_login_id_uniqueness_in_db(self, retail_banking_db_with_auth: RetailBankingDB):
        """Test that all login IDs in the database are unique."""
        db = retail_banking_db_with_auth
        
        login_ids = [customer.customer_login_id for customer in db.customers.values()]
        
        # Check uniqueness
        assert len(login_ids) == len(set(login_ids)), "Login IDs should be unique"
