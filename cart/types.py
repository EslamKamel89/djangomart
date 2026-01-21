from typing import Optional, TypedDict


class CartItem(TypedDict):
    title: str
    price: float
    count: int
    image: str
    brand: str
    category: Optional[str]


Cart = dict[str, CartItem]
