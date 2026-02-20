package com.josephbkasanga.e_commerceapp.ui.main;

import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.josephbkasanga.e_commerceapp.R;
import com.josephbkasanga.e_commerceapp.viewmodel.CartViewModel;

/**
 * CartActivity
 * ------------
 * Shows cart items and checkout
 */
public class CartActivity extends AppCompatActivity {

    private CartViewModel cartViewModel;
    private Button checkoutBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cart);

        checkoutBtn = findViewById(R.id.btnCheckout);
        cartViewModel = new ViewModelProvider(this).get(CartViewModel.class);

        cartViewModel.loadCart();

        checkoutBtn.setOnClickListener(v -> {
            cartViewModel.clearCart();
            Toast.makeText(this, "Checkout successful", Toast.LENGTH_SHORT).show();
            finish();
        });
    }
}
