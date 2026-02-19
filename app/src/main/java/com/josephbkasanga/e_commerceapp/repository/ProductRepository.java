package com.josephbkasanga.e_commerceapp.repository;

import androidx.lifecycle.MutableLiveData;

import com.josephbkasanga.e_commerceapp.data.model.Product;

import java.util.ArrayList;
import java.util.List;

/**
 * ProductRepository
 * -----------------
 * Responsible for fetching product data
 * from the external database (PHP + MySQL).
 */
public class ProductRepository {

    /**
     * Fetch products from database
     * (Later: GET products.php)
     */
    public void getProducts(MutableLiveData<List<Product>> productsLiveData) {

        // TODO: Replace with Retrofit API call

        // Temporary dummy data to simulate API response
        List<Product> products = new ArrayList<>();
        products.add(new Product("1", "Laptop", "Powerful laptop", 1200, "Electronics", 10));
        products.add(new Product("2", "Shoes", "Comfortable shoes", 50, "Fashion", 20));

        productsLiveData.postValue(products);
    }

    /**
     * Add product (Admin only)
     * (Later: POST add_product.php)
     */
    public void addProduct(Product product) {
        // TODO: API call
    }

    /**
     * Delete product (Admin only)
     * (Later: POST delete_product.php)
     */
    public void deleteProduct(String productId) {
        // TODO: API call
    }
}