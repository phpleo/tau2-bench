"""Toolkit for the retail banking consumers domain."""

from typing import Any, Dict, List, Optional

from tau2.domains.retail_banking_consumers.data_model import (
    Card,
    RetailBankingDB,
)
from tau2.environment.toolkit import ToolKitBase, ToolType, is_tool


class RetailBankingTools(ToolKitBase):
    """All the tools for the retail banking consumers domain."""

    db: RetailBankingDB

    def __init__(self, db: RetailBankingDB) -> None:
        super().__init__(db)

    def _get_session_customer_id(self) -> Optional[str]:
        """Get the customer ID from the active session if available.

        Returns:
            The customer ID from the session, or None if no session is active.
        """
        if self.db.session and self.db.session.authenticated:
            return self.db.session.customer_id
        return None

    def _get_card(self, card_id: str) -> Card:
        """Get a card from the database.

        Args:
            card_id: The card ID, such as 'fp_01'.

        Returns:
            The card.

        Raises:
            ValueError: If the card is not found.
        """
        if card_id not in self.db.cards:
            raise ValueError(f"Card {card_id} not found")
        return self.db.cards[card_id]

    def _get_customer_cards(self, customer_id: str) -> List[Card]:
        """Get all cards belonging to a customer.

        Args:
            customer_id: The customer ID.

        Returns:
            List of cards belonging to the customer.

        Raises:
            ValueError: If the customer is not found.
        """
        if customer_id not in self.db.customers:
            raise ValueError(f"Customer {customer_id} not found")

        return [
            card for card in self.db.cards.values() if card.customer_id == customer_id
        ]

    def _get_account(self, account_id: str):
        """Get an account from the database.

        Args:
            account_id: The account ID.

        Returns:
            The account.

        Raises:
            ValueError: If the account is not found.
        """
        if account_id not in self.db.accounts:
            raise ValueError(f"Account {account_id} not found")
        return self.db.accounts[account_id]

    def _get_customer_accounts(self, customer_id: str) -> List[str]:
        """Get all account IDs belonging to a customer.

        Args:
            customer_id: The customer ID.

        Returns:
            List of account IDs belonging to the customer.

        Raises:
            ValueError: If the customer is not found.
        """
        if customer_id not in self.db.customers:
            raise ValueError(f"Customer {customer_id} not found")

        return [
            account_id
            for account_id, account in self.db.accounts.items()
            if account.customer_id == customer_id
        ]

    @is_tool(ToolType.READ)
    def get_session_info(self) -> Dict[str, Any]:
        """
        Get the current session information for the logged-in customer.
        This tool is only available when the customer is already authenticated
        (e.g., logged into the mobile app or web portal).

        Returns:
            A dictionary containing the session information:
            - customer_id: The internal customer ID
            - full_name: The customer's full name
            - first_name: The customer's first name
            - authenticated: Whether the customer is authenticated

        Raises:
            ValueError: If no active session exists.
        """
        if not self.db.session or not self.db.session.authenticated:
            raise ValueError("No active session found. Customer must be authenticated first.")

        # Extract first name from full name
        first_name = self.db.session.full_name.split()[0]

        return {
            "customer_id": self.db.session.customer_id,
            "full_name": self.db.session.full_name,
            "first_name": first_name,
            "authenticated": self.db.session.authenticated,
        }

    @is_tool(ToolType.READ)
    def authenticate_customer(self, customer_login_id: str) -> Dict[str, Any]:
        """
        Authenticate a customer using their login ID and retrieve their customer information.
        This tool should be used at the beginning of the conversation to verify the customer's
        identity before providing any account information or services.

        Args:
            customer_login_id: The customer's login ID. Example: '45682409'

        Returns:
            A dictionary containing the customer information:
            - customer_id: The internal customer ID
            - full_name: The customer's full name
            - customer_login_id: The customer's login ID (for confirmation)

        Raises:
            ValueError: If the customer login ID is not found.
        """
        # Search for the customer by their login ID
        for customer_id, customer_data in self.db.customers.items():
            if customer_data.customer_login_id == customer_login_id:
                return {
                    "customer_id": customer_id,
                    "full_name": customer_data.full_name,
                    "customer_login_id": customer_data.customer_login_id,
                }
        
        # If no customer found, raise an error
        raise ValueError(f"Customer with login ID {customer_login_id} not found. Please verify the login ID and try again.")

    @is_tool(ToolType.READ)
    def get_current_available_credit(self, card_id: str) -> Dict[str, Any]:
        """
        Get the current available credit for a specific card.

        Args:
            card_id: The ID of the card to check. Example: 'fp_01'

        Returns:
            A dictionary containing the card information including:
            - card_id: The card ID
            - card_number: Last 4 digits of the card number (masked)
            - type: Type of card (credit_card or debit_card)
            - available_credit: The current available credit or balance
            - currency: The currency code (e.g., USD, EUR)

        Raises:
            ValueError: If the card is not found.
        """
        card = self._get_card(card_id)

        # Mask the card number, showing only last 4 digits
        masked_card_number = f"****{card.card_number[-4:]}"

        return {
            "card_id": card_id,
            "card_number": masked_card_number,
            "type": card.type,
            "available_credit": card.available_credit,
            "currency": card.currency,
        }

    @is_tool(ToolType.WRITE)
    def lock_card(self, card_id: str, reason: str) -> str:
        """
        Lock a card to prevent unauthorized transactions. Once locked, the card cannot
        be used for any transactions until it is unlocked. This is a security measure
        to protect the customer's account.

        Args:
            card_id: The ID of the card to lock. Example: 'fp_01'
            reason: The reason for locking the card (e.g., 'lost', 'stolen', 'suspicious_activity', 'customer_request')

        Returns:
            A confirmation message indicating that the card has been locked.

        Raises:
            ValueError: If the card is not found or if the reason is empty.
        """
        if not reason or not reason.strip():
            raise ValueError("A reason must be provided to lock the card")

        card = self._get_card(card_id)

        # In a real system, we would add a 'status' field to the Card model
        # For now, we'll return a confirmation message
        # TODO: Add a 'status' field to the Card model in data_model.py

        masked_card_number = f"****{card.card_number[-4:]}"

        return f"Card {masked_card_number} ({card.type}) has been successfully locked. Reason: {reason}. The card can no longer be used for transactions until it is unlocked."

    @is_tool(ToolType.READ)
    def list_cards(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        List all cards associated with a customer account.

        Args:
            customer_id: The ID of the customer. Example: 'cus_01'

        Returns:
            A list of dictionaries, each containing information about a card:
            - card_id: The card ID
            - card_number: Last 4 digits of the card number (masked)
            - type: Type of card (credit_card or debit_card)
            - available_credit: The current available credit or balance
            - currency: The currency code

        Raises:
            ValueError: If the customer is not found or has no cards.
        """
        cards = self._get_customer_cards(customer_id)

        if not cards:
            raise ValueError(f"No cards found for customer {customer_id}")

        result = []
        for card_id, card in self.db.cards.items():
            if card.customer_id == customer_id:
                masked_card_number = f"****{card.card_number[-4:]}"
                result.append(
                    {
                        "card_id": card_id,
                        "card_number": masked_card_number,
                        "type": card.type,
                        "available_credit": card.available_credit,
                        "currency": card.currency,
                    }
                )

        return result

    @is_tool(ToolType.READ)
    def get_routing_numbers(self, account_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the routing numbers for a customer's deposit account.
        Routing numbers are used for different types of transactions.

        Args:
            account_id: The ID of the account. If not provided and the customer is logged in,
                       the primary account for the logged-in customer will be used. Example: 'acc_01'

        Returns:
            A dictionary containing the routing numbers:
            - account_number: The account number (masked)
            - routing_number_ach: Routing number for electronic transfers, payments, direct deposits and ordering checks
            - routing_number_wire: Routing number for U.S. wire transfers

        Raises:
            ValueError: If the account is not found or does not have routing numbers.
        """
        # If no account_id provided, try to get it from the session
        if account_id is None:
            session_customer_id = self._get_session_customer_id()
            if session_customer_id is None:
                raise ValueError("No account_id provided and no active session found. Please provide an account_id or authenticate first.")

            # Get the customer's accounts
            account_ids = self._get_customer_accounts(session_customer_id)
            if not account_ids:
                raise ValueError(f"No accounts found for customer {session_customer_id}")

            # Use the first account (primary account)
            account_id = account_ids[0]

        account = self._get_account(account_id)

        # Mask the account number, showing only last 4 digits
        masked_account_number = f"****{account.account_number[-4:]}"

        if not account.routing_number_ach or not account.routing_number_wire:
            raise ValueError(f"Routing numbers not available for account {account_id}")

        return {
            "account_number": masked_account_number,
            "routing_number_ach": account.routing_number_ach,
            "routing_number_ach_purpose": "For electronic transfers, payments, direct deposits and ordering checks",
            "routing_number_wire": account.routing_number_wire,
            "routing_number_wire_purpose": "For U.S. wire transfers",
        }

    @is_tool(ToolType.GENERIC)
    def transfer_to_human_agent(self, summary: str) -> str:
        """
        Transfer the customer to a human agent with a summary of their issue.
        Only use this when:
        - The customer explicitly asks to speak with a human agent
        - Given the policy and available tools, you cannot solve the customer's issue
        - The issue requires human judgment or authorization beyond your capabilities

        Args:
            summary: A brief summary of the customer's issue and what has been attempted so far

        Returns:
            A confirmation message that the customer is being transferred to a human agent
        """
        if not summary or not summary.strip():
            raise ValueError("A summary must be provided when transferring to a human agent")

        return f"Transferring you to a human agent. Summary of your issue: {summary}. A representative will be with you shortly."


if __name__ == "__main__":
    from tau2.domains.retail_banking_consumers.data_model import get_db

    db = get_db()
    tools = RetailBankingTools(db)

    # print("=== Testing Retail Banking Tools ===\n")

    # # Test list_cards
    # print("1. Listing cards for customer cus_01:")
    # cards = tools.list_cards("cus_01")
    # print(f"   Found {len(cards)} card(s)")
    # for card in cards:
    #     print(f"   - {card}")

    # # Test get_current_available_credit
    # print("\n2. Getting available credit for card fp_01:")
    # credit_info = tools.get_current_available_credit("fp_01")
    # print(f"   {credit_info}")

    # # Test lock_card
    # print("\n3. Locking card fp_01:")
    # result = tools.lock_card("fp_01", "customer_request")
    # print(f"   {result}")

    # print("\n=== All tests completed ===")
