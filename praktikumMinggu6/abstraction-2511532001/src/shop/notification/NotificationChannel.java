package shop.notification;

public interface NotificationChannel {
    String channelName();
    boolean send(CustomerContact contact, String message);
}
