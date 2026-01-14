package com.example.socialnetworwfx.repository.Paginare;

import com.example.socialnetworwfx.domain.Entity;
import com.example.socialnetworwfx.repository.NewRepository;

public interface PagingRepository<ID,E extends Entity<ID>> extends NewRepository<ID, E > {
    Page<E> findAllOnPage(Pageable pageable);
}

