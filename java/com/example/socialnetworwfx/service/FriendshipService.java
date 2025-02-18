package com.example.socialnetworwfx.service;

import com.example.socialnetworwfx.domain.Friendship;
import com.example.socialnetworwfx.domain.User;
import com.example.socialnetworwfx.domain.event.ChangeEventType;
import com.example.socialnetworwfx.domain.event.FriendshipEntityChange;
import com.example.socialnetworwfx.repository.FriendshipDbRepository;
import com.example.socialnetworwfx.repository.Paginare.Page;
import com.example.socialnetworwfx.repository.Paginare.Pageable;
import com.example.socialnetworwfx.repository.UserDbRepository;
import com.example.socialnetworwfx.utils.Observable;
import com.example.socialnetworwfx.utils.Observer;

import java.util.ArrayList;
import java.util.List;

public class FriendshipService implements Service<Friendship>, Observable<FriendshipEntityChange> {
    FriendshipDbRepository repository;
    UserDbRepository userRepository;
    private List<Observer<FriendshipEntityChange>> observers=new ArrayList<>();

    public FriendshipService(FriendshipDbRepository repository, UserDbRepository userRepository) {
        this.repository = repository;
        this.userRepository = userRepository;
    }

    @Override
    public Friendship delete(Long ID) {
        Friendship a=repository.delete(ID).orElseThrow(() -> new IllegalArgumentException("Service says: invalid ID"));
        FriendshipEntityChange change=new FriendshipEntityChange(ChangeEventType.DELETE,a);
        notifyObservers(change);
        return a;
    }

    public Friendship save(Long ID1, Long ID2) {
        Friendship friendship = new Friendship(ID1, ID2);
        Friendship a=repository.save(friendship).orElse(null);
        FriendshipEntityChange event=new FriendshipEntityChange(ChangeEventType.ADD, friendship);
        notifyObservers(event);
        return a;
    }

    @Override
    public Iterable<Friendship> findAll() {
        return repository.findAll();
    }

    public Page<User> getPaginatedFriendships(Long userId, int pageNr, int pageSize) {
        Pageable pageable = new Pageable(pageSize, pageNr);
        Page<Friendship> friendshipPage = repository.findAllOnPage(pageable);

        List<User> friends = new ArrayList<>();
        for (Friendship friendship : friendshipPage.getElementsOnPage()) {
            Long friendId = friendship.getFirstFriend().equals(userId)
                    ? friendship.getSecondFriend()
                    : friendship.getFirstFriend();
            Friendship existingFriendship = findOne(userId, friendId);
            if (existingFriendship != null) {
                User friend = userRepository.findOne(friendId).orElseThrow(() -> new IllegalArgumentException("User not found"));
                friends.add(friend);
            }
        }

        return new Page<>(friendshipPage.getTotalNrOfElems(), friends);
    }


    public Friendship findOne(Long ID1,Long ID2){
        Iterable<Friendship> friendships = repository.findAll();
        for(Friendship friendship:friendships){
            if(friendship.getFirstFriend().equals(ID1) && friendship.getSecondFriend().equals(ID2)) {
                return friendship;
            }
            if(friendship.getSecondFriend().equals(ID1) && friendship.getFirstFriend().equals(ID2)) {
                return friendship;
            }
        }
        return null;
    }
    @Override
    public void addObserver(Observer<FriendshipEntityChange> e) {
        observers.add(e);

    }

    @Override
    public void removeObserver(Observer<FriendshipEntityChange> e) {
        //observers.remove(e);
    }

    @Override
    public void notifyObservers(FriendshipEntityChange t) {

        observers.stream().forEach(x->x.update(t));
    }
}
