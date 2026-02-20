package com.josephbkasanga.e_commerceapp;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import com.josephbkasanga.e_commerceapp.ui.auth.LoginActivity;
import com.josephbkasanga.e_commerceapp.R;

/**
 * MainActivity
 * ------------
 * This is the launcher activity that appears when the app starts.
 * It can navigate the user to the Login screen.
 */
public class MainActivity extends AppCompatActivity {

    private Button btnGoToLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // layout file for MainActivity

        // Connect button from layout
        btnGoToLogin = findViewById(R.id.btnGoToLogin);

        // Set click listener to navigate to LoginActivity
        btnGoToLogin.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, LoginActivity.class);
            startActivity(intent); // open LoginActivity
        });
    }
}
