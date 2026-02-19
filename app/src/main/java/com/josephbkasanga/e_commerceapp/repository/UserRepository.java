package com.josephbkasanga.e_commerceapp.repository;



import androidx.lifecycle.MutableLiveData;

import com.josephbkasanga.e_commerceapp.data.model.User;

/**
 * UserRepository
 * ----------------
 * This class acts as a bridge between the ViewModel
 * and the external database (PHP + MySQL).
 *
 * No HashMap (RAM storage)
 * Designed for API communication (Retrofit later)
 */
public class UserRepository {

    /**
     * Register a new user in the database
     * (This will later call register.php)
     */
    public void registerUser(User user,
                             MutableLiveData<User> userLiveData,
                             MutableLiveData<String> errorLiveData) {

        // TODO: Replace this block with Retrofit API call
        // For now, we simulate a successful response

        if (user.getEmail().equals("admin@example.com")) {
            errorLiveData.postValue("User already exists");
        } else {
            userLiveData.postValue(user);
        }
    }

    /**
     * Login user from database
     * (This will later call login.php)
     */
    public void loginUser(String email,
                          MutableLiveData<User> userLiveData,
                          MutableLiveData<String> errorLiveData) {

        // TODO: Replace with Retrofit call to login.php

        if (email.equals("admin@example.com")) {
            userLiveData.postValue(
                    new User("1", "Admin", email, true)
            );
        } else {
            errorLiveData.postValue("Invalid credentials");
        }
    }
}
