package com.example.socialnetworwfx.domain.validation;

import com.example.socialnetworwfx.domain.Message;

public class MessageValidation implements  Validation<Message>{

    @Override
    public void validate(Message entity) throws ValidationException {
        if(entity.getFrom() == null){
            throw new ValidationException("From is null");
        }

        if(entity.getTo() == null){
            throw new ValidationException("To is null");
        }

        if(entity.getMessage()==null || entity.getMessage().trim().isEmpty()){
            throw new ValidationException("Message is null or empty");
        }

        if (entity.getData() == null) {
            throw new ValidationException("Data is null");
        }
    }
}
