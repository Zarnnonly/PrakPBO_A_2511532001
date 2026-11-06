package shop.notification;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class NotificationService {
    private final List<NotificationChannel> channels = new ArrayList<>();

    public void register(NotificationChannel channel) {
        channels.add(Objects.requireNonNull(channel, "Channel is required"));
    }

    public int broadcast(CustomerContact contact, String message) {
        int sent = 0;
        for (NotificationChannel channel : channels) {
            if (channel.send(contact, message)) {
                sent++;
            }
        }
        return sent;
    }
}
