package com.example.socialnetworwfx.domain.event;

import com.example.socialnetworwfx.domain.Message;

public class MessageEntityChange extends jdk.jfr.Event implements Event{
    private ChangeEventType eventType;
    private Message message,oldmessage;

    public MessageEntityChange(ChangeEventType eventType,Message message) {
        this.eventType = eventType;
        this.message = message;
    }

    public MessageEntityChange(ChangeEventType eventType,Message oldmessage,Message message) {
        this.eventType = eventType;
        this.oldmessage = oldmessage;
        this.message = message;
    }

    public ChangeEventType getEventType() {
        return eventType;
    }

    public Message getMessage() {
        return message;
    }
    public Message getOldMessage() {
        return oldmessage;
    }
}
