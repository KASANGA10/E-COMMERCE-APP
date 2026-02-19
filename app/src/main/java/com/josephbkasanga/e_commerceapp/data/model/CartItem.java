package com.josephbkasanga.e_commerceapp.data.model;

/**
 * CartItem model represents a single item in the shopping cart.
 * Contains the product and the quantity selected by the user.
 */
public class CartItem {
    private Product product;   // Product added to the cart
    private int quantity;      // Quantity of the product

    /**
     * Constructor to create a CartItem object
     */
    public CartItem(Product product, int quantity) {
        this.product = product;
        this.quantity = quantity;
    }

    // Getters
    public Product getProduct() { return product; }
    public int getQuantity() { return quantity; }

    // Setter for quantity
    public void setQuantity(int quantity) { this.quantity = quantity; }
}
