<h1>Odoo Product Detail Via Endpoint </h1>
<h2> Odoo Backend API </h2>
<h3> Books Route </h3>

```bash
http://localhost:8080/api/products
```

<h3> Books Route Output</h3>

```bash
{
   "success": true,
    "data": {
        "total": 2,
        "items": [
            {
                "name": "Product A",
                "description": "<p>DETIALS PRODUCT A</p>",
                "default_code": false,
                "detailed_type": "product",
                "categ_id": "All",
                "standard_price": 50000.0,
                "list_price": 100000.0,
                "qty_available": 300.0,
                "uom_id": "Units",
                "invoice_policy": "order"
            }
        ]
    }
}
```