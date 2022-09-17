## Beautiful-repr
Helps structure the formatting of objects in Python.

### Installation
`pip install beautiful-repr`

### Why Beautiful-repr ?
* Beautiful repr out of the box
* Great expansion possibilities
* Very small and simple
* No external dependencies

### Example
```python
from beautiful_repr import *


class ShoppingCart(StylizedMixin):
    _repr_fields = (
        Field("token"),
        Field(
            "products",
            value_getter=parse_length,
            formatter=TemplateFormatter("{value} products")
        ),
    )

    def __init__(self, token: str, products: tuple[str, ] = tuple()):
        self.token = token
        self.products = tuple(products)


print(ShoppingCart("s12345", ("Potato", "iPhone", "New Vegas")))
```

**output:** `ShoppingCart(token=s12345, 3 products)`
