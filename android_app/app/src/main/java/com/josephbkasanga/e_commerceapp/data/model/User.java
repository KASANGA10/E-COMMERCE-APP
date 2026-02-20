package com.josephbkasanga.e_commerceapp.data.model;
/**
 * User model class represents a user of the e-commerce app.
 * Holds basic user information and admin status.
 */
public class User {
    private String uid;       // Unique user ID
    private String name;      // User's name
    private String email;     // User's email address
    private boolean isAdmin;  // True if user is an admin

    /**
     * Constructor to create a User object.
     */
    public User(String uid, String name, String email, boolean isAdmin) {
        this.uid = uid;
        this.name = name;
        this.email = email;
        this.isAdmin = isAdmin;
    }

    // Getters
    public String getUid() { return uid; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public boolean isAdmin() { return isAdmin; }

    // Setters
    public void setName(String name) { this.name = name; }
    public void setEmail(String email) { this.email = email; }
    public void setAdmin(boolean admin) { isAdmin = admin; }
}
