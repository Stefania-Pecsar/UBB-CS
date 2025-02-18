package com.example.socialnetworwfx.domain;

import java.time.LocalDateTime;
import java.util.List;

public class ReplyMessage extends Message {
    private Message reply;

    public ReplyMessage(User from, List<User> to, String message, LocalDateTime data, Message reply) {
        super(from,to,message,data);
        setReply(reply);
    }

    @Override
    public Message getReply() {
        return reply;
    }

    @Override
    public void setReply(Message reply) {
        this.reply = reply;
    }
}
