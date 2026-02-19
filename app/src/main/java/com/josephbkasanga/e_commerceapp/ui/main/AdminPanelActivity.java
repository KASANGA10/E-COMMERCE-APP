package com.josephbkasanga.e_commerceapp.ui.main;

// Android imports for Activity lifecycle and UI elements
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

// AndroidX imports for AppCompatActivity and ViewModel support
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

// App-specific imports
import com.josephbkasanga.e_commerceapp.R;
import com.josephbkasanga.e_commerceapp.viewmodel.ProductViewModel;

/**
 * AdminPanelActivity
 * ------------------
 * This Activity represents the Admin screen.
 * Only admin users should access this screen.
 *
 * Responsibilities:
 * - Display admin options
 * - Allow admin to add, edit, or delete products
 *
 * NOTE:
 * This class ONLY handles UI logic.
 * Business logic and data handling are delegated to ViewModel.
 */
public class AdminPanelActivity extends AppCompatActivity {

    // ViewModel that handles product-related logic
    // This connects the UI to the repository layer
    private ProductViewModel productViewModel;

    // Button for adding a new product
    private Button addProductBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Links this Activity to its XML layout file
        // activity_admin_panel.xml
        setContentView(R.layout.activity_admin_panel);

        // Initialize the ProductViewModel
        // ViewModelProvider ensures the ViewModel survives configuration changes
        productViewModel = new ViewModelProvider(this).get(ProductViewModel.class);

        // Connect the Add Product button to the XML view
        addProductBtn = findViewById(R.id.btnAddProduct);

        // Handle click events for the Add Product button
        addProductBtn.setOnClickListener(v -> {

            /*
             * This is where admin product creation logic will go.
             *
             * In a real implementation, this could:
             * - Open a dialog
             * - Open a new activity
             * - Allow admin to enter product details
             *
             * Later, productViewModel.addProduct(product) will be called here.
             */
            Toast.makeText(this, "Add product clicked", Toast.LENGTH_SHORT).show();
        });
    }
}
