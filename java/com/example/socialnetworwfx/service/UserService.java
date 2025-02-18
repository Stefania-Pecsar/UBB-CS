package com.example.socialnetworwfx.service;

import com.example.socialnetworwfx.domain.User;
import com.example.socialnetworwfx.domain.event.ChangeEventType;
import com.example.socialnetworwfx.domain.event.UserEntityChange;
import com.example.socialnetworwfx.repository.UserDbRepository;
import com.example.socialnetworwfx.utils.Observable;
import com.example.socialnetworwfx.utils.Observer;

import java.util.ArrayList;
import java.util.List;

public class UserService implements Service<User>, Observable<UserEntityChange> {
    private UserDbRepository repository;
    private List<Observer<UserEntityChange>> observers=new ArrayList<>();

    public UserService(UserDbRepository repository) {
        this.repository = repository;
    }

    @Override
    public User delete(Long ID) {
        User user = repository.findOne(ID).orElseThrow(() -> new IllegalArgumentException("User not found"));
        repository.delete(ID).orElseThrow(null);
        UserEntityChange event=new UserEntityChange(ChangeEventType.DELETE, user);
        notifyObservers(event);
        return user;
    }

    public User save(String firstName, String lastName,String email,String password) {
        User newUser = new User(firstName, lastName, email, password);
        System.out.println("Sunt in Service save");
        User a=repository.save(newUser).orElse(null);
        System.out.println("Am salvat in bd");
        UserEntityChange event=new UserEntityChange(ChangeEventType.ADD,newUser);
        notifyObservers(event);
        return a;
    }

    public User update(Long ID, String firstName, String lastName,String email,String password) {
        User toBeUpdated = new User(firstName, lastName, email, password);
        toBeUpdated.setID(ID);
        return repository.update(toBeUpdated).orElse(null);
    }
    @Override
    public Iterable<User> findAll(){

        return repository.findAll();
    }

    public User findOne(Long ID) {
        return repository.findOne(ID).orElseThrow(()-> new IllegalArgumentException("User not found"));
    }
    public User findByEmail(String email, String password) {
        Iterable<User> users = repository.findAll();
        for (User user : users) {
            if (user.getEmail().equals(email) && user.getPassword().equals(password)) {
                return user;
            }
        }
        return null;
    }

    public Long findUserByNames(String firstName, String lastName) {
        Iterable<User> users = repository.findAll();
        for (User user : users) {
            if (user.getFirstName().equals(firstName) && user.getLastName().equals(lastName)) {
                return user.getID();
            }
        }
        return null;
    }
    @Override
    public void addObserver(Observer<UserEntityChange> e) {
        observers.add(e);

    }

    @Override
    public void removeObserver(Observer<UserEntityChange> e) {
        observers.remove(e);
    }

    @Override
    public void notifyObservers(UserEntityChange t) {

        observers.stream().forEach(x->x.update(t));
    }
}

