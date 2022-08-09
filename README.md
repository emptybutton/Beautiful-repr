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
import beautiful_repr


class ShoppingCart(beautiful_repr.StylizedMixin):
    repr = beautiful_repr.BeautifulRepr([
        beautiful_repr.Field("token"),
        beautiful_repr.Field(
            "products",
            value_getter=beautiful_repr.tools.parse_length,
            formatter=beautiful_repr.tools.TemplateFormatter("{value} products")
        ),
    ])

    def __init__(self, token: str, products: Iterable[str,] = tuple()):
        self.token = token
        self.products = tuple(products)


print(ShoppingCart("s12345", ("Potato", "iPhone", "New Vegas")))
```

**output:** `ShoppingCart(token=s12345, 3 products)`
