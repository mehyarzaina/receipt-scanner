from typing import Optional, List
from sqlmodel import Field, SQLModel
from sqlmodel import SQLModel, Field, Relationship



class Receipt(SQLModel, table=True):
    __tablename__ = "receipts"

    id: Optional[int] = Field(default=None, primary_key=True)
    receipt_num: Optional[int] = Field(default=None)
    shop_name: Optional[str] = Field(default=None, max_length=255)
    date: Optional[str] = Field(default=None)
    currency: Optional[str] = Field(default=None, max_length=10)
    subtotal: Optional[float] = Field(default=None)
    tax_amount: Optional[float] = Field(default=None)
    grand_total: Optional[float] = Field(default=None)
    receipt_filename: Optional[str] = Field(default=None, max_length=255)

    # Relationship to items
    items: List["Item"] = Relationship(back_populates="receipt")
    
class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    receipt_id: Optional[int] = Field(default=None, foreign_key="receipts.id")  # point to id, not receipt_num
    product_name: Optional[str] = Field(default=None, max_length=255)
    quantity: Optional[float] = Field(default=None)
    price: Optional[float] = Field(default=None)

    receipt: Optional["Receipt"] = Relationship(back_populates="items")