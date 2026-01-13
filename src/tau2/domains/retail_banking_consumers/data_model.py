from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field

from tau2.domains.retail_banking_consumers.utils import RETAIL_BANKING_DB_PATH
from tau2.environment.db import DB


class Customer(BaseModel):
    """Represents a bank customer with their personal information"""

    full_name: str = Field(description="Customer's full name")
    customer_login_id: str = Field(description="Customer's login ID for authentication")


class Account(BaseModel):
    """Represents a bank account belonging to a customer"""

    account_number: str = Field(description="Unique account number")
    customer_id: str = Field(
        description="ID of the customer who owns this account"
    )
    associated_products: List[str] = Field(
        default_factory=list,
        description="List of product IDs (cards, loans, etc.) associated with this account",
    )


CardType = Literal["credit_card", "debit_card"]


class Card(BaseModel):
    """Represents a credit or debit card"""

    customer_id: str = Field(description="ID of the customer who owns this card")
    type: CardType = Field(description="Type of card (credit_card or debit_card)")
    card_number: str = Field(description="Card number")
    currency: str = Field(description="Currency code (e.g., USD, EUR)")
    available_credit: float = Field(
        description="Available credit limit (for credit cards) or available balance (for debit cards)"
    )


class RetailBankingDB(DB):
    """Database containing all retail banking data including customers, accounts, and cards"""

    customers: Dict[str, Customer] = Field(
        description="Dictionary of all customers indexed by customer ID"
    )
    accounts: Dict[str, Account] = Field(
        description="Dictionary of all accounts indexed by account ID"
    )
    cards: Dict[str, Card] = Field(
        description="Dictionary of all cards indexed by card ID"
    )

    def get_statistics(self) -> dict[str, Any]:
        """Get the statistics of the database."""
        num_customers = len(self.customers)
        num_accounts = len(self.accounts)
        num_cards = len(self.cards)

        return {
            "num_customers": num_customers,
            "num_accounts": num_accounts,
            "num_cards": num_cards,
        }


def get_db():
    """Get an instance of the retail banking database."""
    return RetailBankingDB.load(RETAIL_BANKING_DB_PATH)


if __name__ == "__main__":
    db = get_db()
    print(db.get_statistics())
