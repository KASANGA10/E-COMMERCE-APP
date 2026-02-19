package com.josephbkasanga.e_commerceapp.repository;


import androidx.lifecycle.MutableLiveData;

import com.josephbkasanga.e_commerceapp.data.model.CartItem;
import com.josephbkasanga.e_commerceapp.data.model.Product;

import java.util.ArrayList;
import java.util.List;

/**
 * CartRepository
 * --------------
 * Handles cart operations using backend database.
 */
public class CartRepository {

    /**
     * Fetch cart items for a user
     * (Later: GET cart.php?user_id=)
     */
    public void getCartItems(MutableLiveData<List<CartItem>> cartLiveData) {

        // TODO: Replace with API call
        cartLiveData.postValue(new ArrayList<>());
    }

    /**
     * Add product to cart
     * (Later: POST add_to_cart.php)
     */
    public void addToCart(Product product) {
        // TODO: API call
    }

    /**
     * Update product quantity
     * (Later: POST update_cart.php)
     */
    public void updateQuantity(CartItem item, int quantity) {
        // TODO: API call
    }

    /**
     * Clear user cart
     * (Later: POST clear_cart.php)
     */
    public void clearCart() {
        // TODO: API call
    }
}