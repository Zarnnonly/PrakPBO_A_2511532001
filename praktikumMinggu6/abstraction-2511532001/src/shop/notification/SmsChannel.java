package shop.notification;

public class SmsChannel extends AbstractChannel {
    private final int maxLength;

    public SmsChannel(int maxLength) {
        if (maxLength < 3) {
            throw new IllegalArgumentException("SMS length must be at least 3");
        }
        this.maxLength = maxLength;
    }

    @Override
    public String channelName() { return "SMS"; }

    @Override
    protected String resolveRecipient(CustomerContact contact) {
        return contact.getPhone().startsWith("08") ? contact.getPhone() : "";
    }

    @Override
    protected String prepare(String message) {
        return message.length() > maxLength
                ? message.substring(0, maxLength - 3) + "..." : message;
    }

    @Override
    protected boolean deliver(String recipient, String message) {
        System.out.println("[SMS to " + recipient + "] " + message);
        return true;
    }
}
