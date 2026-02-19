package com.josephbkasanga.e_commerceapp.ui.main;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.josephbkasanga.e_commerceapp.R;
import com.josephbkasanga.e_commerceapp.viewmodel.ProductViewModel;

/**
 * ProductListActivity
 * -------------------
 * Shows list of products using RecyclerView
 */
public class ProductListActivity extends AppCompatActivity {

    private ProductViewModel productViewModel;
    private RecyclerView recyclerView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_list);

        // RecyclerView setup
        recyclerView = findViewById(R.id.recyclerProducts);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        // ViewModel
        productViewModel = new ViewModelProvider(this).get(ProductViewModel.class);

        // Load products
        productViewModel.loadProducts();

        // Observe product list
        productViewModel.productsLiveData.observe(this, products -> {
            // TODO: Attach ProductAdapter here
            // recyclerView.setAdapter(new ProductAdapter(products, product -> {
            //     Intent intent = new Intent(this, ProductDetailActivity.class);
            //     intent.putExtra("product_id", product.getId());
            //     startActivity(intent);
            // }));
        });
    }
}
