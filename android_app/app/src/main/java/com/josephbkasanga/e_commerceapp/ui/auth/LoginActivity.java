package com.josephbkasanga.e_commerceapp.ui.auth;


import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.josephbkasanga.e_commerceapp.R;
import com.josephbkasanga.e_commerceapp.ui.main.ProductListActivity;
import com.josephbkasanga.e_commerceapp.viewmodel.AuthViewModel;

/**
 * LoginActivity
 * -------------
 * Handles user login UI
 * Does NOT talk to database directly
 */
public class LoginActivity extends AppCompatActivity {

    private AuthViewModel authViewModel;
    private EditText emailInput;
    private Button loginButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //Initialize UI elements
        emailInput = findViewById(R.id.etEmail);
        loginButton = findViewById(R.id.btnLogin);

        //Initialize ViewModel
        authViewModel = new ViewModelProvider(this).get(AuthViewModel.class);

        //Login button click
        loginButton.setOnClickListener(v -> {
            String email = emailInput.getText().toString().trim();

            if (email.isEmpty()) {
                Toast.makeText(this, "Email required", Toast.LENGTH_SHORT).show();
                return;
            }

            // Ask ViewModel to login
            authViewModel.login(email);
        });

        //Observe successful login
        authViewModel.userLiveData.observe(this, user -> {
            // Navigate to Product List screen
            Intent intent = new Intent(this, ProductListActivity.class);
            startActivity(intent);
            finish(); // close login screen
        });

        //Observe errors
        authViewModel.errorLiveData.observe(this, error -> {
            Toast.makeText(this, error, Toast.LENGTH_SHORT).show();
        });
    }
}
