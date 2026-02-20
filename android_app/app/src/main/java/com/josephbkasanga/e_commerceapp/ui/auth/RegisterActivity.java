package com.josephbkasanga.e_commerceapp.ui.auth;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.josephbkasanga.e_commerceapp.R;
import com.josephbkasanga.e_commerceapp.viewmodel.AuthViewModel;

/**
 * RegisterActivity
 * ----------------
 * Handles new user registration
 */
public class RegisterActivity extends AppCompatActivity {

    private AuthViewModel authViewModel;
    private EditText nameInput, emailInput;
    private Button registerButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        // Initialize UI
        nameInput = findViewById(R.id.etName);
        emailInput = findViewById(R.id.etEmail);
        registerButton = findViewById(R.id.btnRegister);

        // ViewModel
        authViewModel = new ViewModelProvider(this).get(AuthViewModel.class);

        // Register button click
        registerButton.setOnClickListener(v -> {
            String name = nameInput.getText().toString().trim();
            String email = emailInput.getText().toString().trim();

            if (name.isEmpty() || email.isEmpty()) {
                Toast.makeText(this, "All fields required", Toast.LENGTH_SHORT).show();
                return;
            }

            authViewModel.register(name, email);
        });

        // Observe success
        authViewModel.userLiveData.observe(this, user -> {
            Toast.makeText(this, "Registered successfully", Toast.LENGTH_SHORT).show();
            finish(); // return to login
        });

        // Observe error
        authViewModel.errorLiveData.observe(this, error -> {
            Toast.makeText(this, error, Toast.LENGTH_SHORT).show();
        });
    }
}
