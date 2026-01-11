import pytest

from tau2.data_model.message import ToolCall
from tau2.domains.retail_banking_consumers.data_model import (
    Account,
    Card,
    Customer,
    RetailBankingDB,
)
from tau2.domains.retail_banking_consumers.environment import get_environment
from tau2.environment.environment import Environment


@pytest.fixture
def retail_banking_db() -> RetailBankingDB:
    """Create a sample retail banking database for testing."""
    return RetailBankingDB(
        customers={
            "cus_01": Customer(full_name="Dylan Parker"),
            "cus_02": Customer(full_name="Sarah Johnson"),
        },
        accounts={
            "acc_01": Account(
                account_number="07895034807",
                customer_id="cus_01",
                associated_products=["fp_01", "fp_03"],
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
            "fp_03": Card(
                customer_id="cus_01",
                type="debit_card",
                card_number="450087654321098",
                currency="EUR",
                available_credit=1500.0,
            ),
        },
    )


@pytest.fixture
def environment(retail_banking_db: RetailBankingDB) -> Environment:
    """Create an environment with the test database."""
    return get_environment(retail_banking_db)


class TestGetCurrentAvailableCredit:
    """Test the get_current_available_credit tool."""

    def test_get_available_credit_success(self, environment: Environment):
        """Test successfully getting available credit for a card."""
        tool_call = ToolCall(
            id="1",
            name="get_current_available_credit",
            arguments={"card_id": "fp_01"},
        )
        response = environment.get_response(tool_call)

        assert not response.error
        assert "fp_01" in response.content
        assert "****6417" in response.content  # Masked card number
        assert "credit_card" in response.content
        assert "2900" in response.content
        assert "USD" in response.content

    def test_get_available_credit_card_not_found(self, environment: Environment):
        """Test error when card is not found."""
        tool_call = ToolCall(
            id="2",
            name="get_current_available_credit",
            arguments={"card_id": "fp_99"},
        )
        response = environment.get_response(tool_call)

        assert response.error
        assert "not found" in response.content.lower()


class TestLockCard:
    """Test the lock_card tool."""

    def test_lock_card_success(self, environment: Environment):
        """Test successfully locking a card."""
        tool_call = ToolCall(
            id="3",
            name="lock_card",
            arguments={"card_id": "fp_01", "reason": "lost"},
        )
        response = environment.get_response(tool_call)

        assert not response.error
        assert "locked" in response.content.lower()
        assert "****6417" in response.content  # Masked card number
        assert "lost" in response.content.lower()

    def test_lock_card_different_reasons(self, environment: Environment):
        """Test locking a card with different reasons."""
        reasons = ["stolen", "suspicious_activity", "customer_request"]

        for i, reason in enumerate(reasons):
            tool_call = ToolCall(
                id=str(10 + i),
                name="lock_card",
                arguments={"card_id": "fp_02", "reason": reason},
            )
            response = environment.get_response(tool_call)

            assert not response.error
            assert "locked" in response.content.lower()
            assert reason in response.content.lower()

    def test_lock_card_empty_reason(self, environment: Environment):
        """Test error when reason is empty."""
        tool_call = ToolCall(
            id="4",
            name="lock_card",
            arguments={"card_id": "fp_01", "reason": ""},
        )
        response = environment.get_response(tool_call)

        assert response.error
        assert "reason" in response.content.lower()

    def test_lock_card_not_found(self, environment: Environment):
        """Test error when card is not found."""
        tool_call = ToolCall(
            id="5",
            name="lock_card",
            arguments={"card_id": "fp_99", "reason": "lost"},
        )
        response = environment.get_response(tool_call)

        assert response.error
        assert "not found" in response.content.lower()


class TestListCards:
    """Test the list_cards tool."""

    def test_list_cards_single_card(self, environment: Environment):
        """Test listing cards for a customer with one card."""
        # cus_02 has only one card
        tool_call = ToolCall(
            id="6",
            name="list_cards",
            arguments={"customer_id": "cus_02"},
        )
        response = environment.get_response(tool_call)

        assert not response.error
        assert "fp_02" in response.content
        assert "****8901" in response.content  # Masked card number
        assert "debit_card" in response.content

    def test_list_cards_multiple_cards(self, environment: Environment):
        """Test listing cards for a customer with multiple cards."""
        # cus_01 has two cards
        tool_call = ToolCall(
            id="7",
            name="list_cards",
            arguments={"customer_id": "cus_01"},
        )
        response = environment.get_response(tool_call)

        assert not response.error
        assert "fp_01" in response.content
        assert "fp_03" in response.content
        assert "****6417" in response.content  # First card
        assert "****1098" in response.content  # Second card
        assert "credit_card" in response.content
        assert "debit_card" in response.content
        assert "USD" in response.content
        assert "EUR" in response.content

    def test_list_cards_customer_not_found(self, environment: Environment):
        """Test error when customer is not found."""
        tool_call = ToolCall(
            id="8",
            name="list_cards",
            arguments={"customer_id": "cus_99"},
        )
        response = environment.get_response(tool_call)

        assert response.error
        assert "not found" in response.content.lower()


class TestTransferToHumanAgent:
    """Test the transfer_to_human_agent tool."""

    def test_transfer_success(self, environment: Environment):
        """Test successfully transferring to a human agent."""
        tool_call = ToolCall(
            id="9",
            name="transfer_to_human_agent",
            arguments={"summary": "Customer needs help with a complex transaction"},
        )
        response = environment.get_response(tool_call)

        assert not response.error
        assert "transfer" in response.content.lower()
        assert "human agent" in response.content.lower()
        assert "complex transaction" in response.content.lower()

    def test_transfer_empty_summary(self, environment: Environment):
        """Test error when summary is empty."""
        tool_call = ToolCall(
            id="10",
            name="transfer_to_human_agent",
            arguments={"summary": ""},
        )
        response = environment.get_response(tool_call)

        assert response.error
        assert "summary" in response.content.lower()


class TestCardNumberMasking:
    """Test that card numbers are properly masked in all responses."""

    def test_all_tools_mask_card_numbers(self, environment: Environment):
        """Verify that no tool exposes full card numbers."""
        tools_to_test = [
            ToolCall(
                id="mask_1",
                name="get_current_available_credit",
                arguments={"card_id": "fp_01"},
            ),
            ToolCall(
                id="mask_2",
                name="list_cards",
                arguments={"customer_id": "cus_01"},
            ),
            ToolCall(
                id="mask_3",
                name="lock_card",
                arguments={"card_id": "fp_01", "reason": "test"},
            ),
        ]

        # Full card numbers that should NOT appear in responses
        full_card_numbers = ["342979928736417", "450012345678901", "450087654321098"]

        for tool_call in tools_to_test:
            response = environment.get_response(tool_call)
            for full_number in full_card_numbers:
                # First 12 digits should never appear
                assert full_number[:12] not in response.content
