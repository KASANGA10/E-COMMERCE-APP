package com.josephbkasanga.e_commerceapp.ui.main;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.josephbkasanga.e_commerceapp.R;
import com.josephbkasanga.e_commerceapp.viewmodel.CartViewModel;

/**
 * ProductDetailActivity
 * ---------------------
 * Displays product details
 */
public class ProductDetailActivity extends AppCompatActivity {

    private CartViewModel cartViewModel;
    private Button addToCartBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_detail);

        // ViewModel
        cartViewModel = new ViewModelProvider(this).get(CartViewModel.class);

        addToCartBtn = findViewById(R.id.btnAddToCart);

        addToCartBtn.setOnClickListener(v -> {
            // TODO: Pass actual product object
            Toast.makeText(this, "Added to cart", Toast.LENGTH_SHORT).show();
        });
    }
}
