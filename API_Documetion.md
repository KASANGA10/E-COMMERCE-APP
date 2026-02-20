# API Documentation: E-Commerce Multi-Vendor System
This API facilitates multi vendor shopping, allowing customers to aggregate products from different shops into a single cart and checkout, which then partitions orders by vendor.



## 1. Authentication

All protected endpoints require a **JWT Access Token**.

 - **Header:** `Authorization: Bearer <access_token>`
## 2. Product & Shop Discovery

| Method |  Endpoint | Description |
|--|--|--|
|GET  | /api/products/ |List all available products.
|GET|/api/products/{id}/|Retrieve specific product details.
|GET|/api/shops/|List all registered shops.
##  3. Shopping Cart (Customer)
Manages the active session items before purchase.
## View Cart

 - **Endpoint:** `GET /api/cart/`
 - Responce:

```
{
    "id": 1,
    "items": [
        { "product": 101, "product_name": "Laptop", "quantity": 1, "subtotal": 1200.00 }
    ],
    "total_price": 1200.00
}
```
## Add Item

 - **Endpoint:** `POST /api/cart/add_item/`
 - **Payload:** `{ "product_id": 101, "quantity": 1 }`
 
 ## Remove Item
 
 - **Endpoint:** `POST /api/cart/remove_item/`
 - **Payload:** `{ "product_id": 101 }`
 ## 4. Checkout & Orders (Customer)
 The checkout process converts the `Cart` into a `Order` and sub-divided `ShopOrders`.

## Checkout

 - **Endpoint:** `POST /api/cart/checkout/`
 - **Action:** Validates cart, creates orders, and clears the cart.
 ## Order History
 
 - **Endpoint:** `GET /api/orders/`
 -  Structure:
	 
	 - **Order:** Parent container (Total Amount).
	 - **ShopOrder:** Vendor-specific slice (Tracking/Status).
	 - **OrderDetail:** Specific products purchased.
## 5. Vendor Management (Shop Managers)
Endpoints restricted to users with a `ManagerProfile`.
## Manage Shop Orders
 - **Endpoint:** `GET /api/vendor-orders/`
 - **Description:** Returns only the `ShopOrder` segments belonging to the manager's shop.
## Update Order Status
 - **Endpoint:** `POST /api/vendor-orders/{id}/update_status/`
 - **Payload:** `{ "status": "shipped" }`
 - **Valid Statuses:** `pending`, `completed`, `cancelled`.
## 6. Workflow Summary
 
 1. **Discover:** Customer browses `/api/products/`.
 2. **Collect:** Customer adds items via `/api/cart/add_item/`.
 3. **Purchase:** Customer executes `/api/cart/checkout/`.
 4. **Fulfill:** Vendor views slice via `/api/vendor-orders/` and updates status to `completed`.

 
