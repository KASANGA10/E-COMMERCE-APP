package com.josephbkasanga.e_commerceapp.viewmodel;

import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.josephbkasanga.e_commerceapp.data.model.CartItem;
import com.josephbkasanga.e_commerceapp.data.model.Product;
import com.josephbkasanga.e_commerceapp.repository.CartRepository;

import java.util.List;

/**
 * CartViewModel
 * -------------
 * Handles cart UI logic
 */
public class CartViewModel extends ViewModel {

    private CartRepository repository = new CartRepository();
    public MutableLiveData<List<CartItem>> cartLiveData = new MutableLiveData<>();

    public void loadCart() {
        repository.getCartItems(cartLiveData);
    }

    public void addToCart(Product product) {
        repository.addToCart(product);
        loadCart();
    }

    public void clearCart() {
        repository.clearCart();
        loadCart();
    }
}
