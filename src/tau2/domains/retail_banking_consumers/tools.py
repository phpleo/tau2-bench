"""Toolkit for the retail banking consumers domain."""

from typing import Dict, List

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

    @is_tool(ToolType.READ)
    def get_current_available_credit(self, card_id: str) -> Dict[str, any]:
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
    def list_cards(self, customer_id: str) -> List[Dict[str, any]]:
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

    print("=== Testing Retail Banking Tools ===\n")

    # Test list_cards
    print("1. Listing cards for customer cus_01:")
    cards = tools.list_cards("cus_01")
    print(f"   Found {len(cards)} card(s)")
    for card in cards:
        print(f"   - {card}")

    # Test get_current_available_credit
    print("\n2. Getting available credit for card fp_01:")
    credit_info = tools.get_current_available_credit("fp_01")
    print(f"   {credit_info}")

    # Test lock_card
    print("\n3. Locking card fp_01:")
    result = tools.lock_card("fp_01", "customer_request")
    print(f"   {result}")

    print("\n=== All tests completed ===")
