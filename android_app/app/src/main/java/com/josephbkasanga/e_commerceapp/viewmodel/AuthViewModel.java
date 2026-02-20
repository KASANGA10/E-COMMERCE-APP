package com.josephbkasanga.e_commerceapp.viewmodel;


import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.josephbkasanga.e_commerceapp.data.model.User;
import com.josephbkasanga.e_commerceapp.repository.UserRepository;

/**
 * AuthViewModel
 * -------------
 * Handles authentication logic for UI
 */
public class AuthViewModel extends ViewModel {

    private UserRepository repository = new UserRepository();

    public MutableLiveData<User> userLiveData = new MutableLiveData<>();
    public MutableLiveData<String> errorLiveData = new MutableLiveData<>();

    /**
     * Register user
     */
    public void register(String name, String email) {
        User user = new User(null, name, email, false);
        repository.registerUser(user, userLiveData, errorLiveData);
    }

    /**
     * Login user
     */
    public void login(String email) {
        repository.loginUser(email, userLiveData, errorLiveData);
    }
}
