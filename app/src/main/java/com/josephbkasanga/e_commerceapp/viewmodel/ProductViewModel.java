package com.josephbkasanga.e_commerceapp.viewmodel;


import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.josephbkasanga.e_commerceapp.data.model.Product;
import com.josephbkasanga.e_commerceapp.repository.ProductRepository;

import java.util.List;

/**
 * ProductViewModel
 * ----------------
 * Manages product UI state
 */
public class ProductViewModel extends ViewModel {

    private ProductRepository repository = new ProductRepository();
    public MutableLiveData<List<Product>> productsLiveData = new MutableLiveData<>();

    public void loadProducts() {
        repository.getProducts(productsLiveData);
    }
}

