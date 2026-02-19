package com.josephbkasanga.e_commerceapp.data.model;
/**
 * Product model class represents a product in the store.
 * Holds product details like name, price, category, and stock quantity.
 */
public class Product {
    private String id;             // Unique product ID
    private String name;           // Product name
    private String description;    // Product description
    private double price;          // Product price
    private String category;       // Product category
    private int stockQuantity;     // Number of items in stock

    /**
     * Constructor to create a Product object
     */
    public Product(String id, String name, String description, double price, String category, int stockQuantity) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.price = price;
        this.category = category;
        this.stockQuantity = stockQuantity;
    }

    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getDescription() { return description; }
    public double getPrice() { return price; }
    public String getCategory() { return category; }
    public int getStockQuantity() { return stockQuantity; }
}