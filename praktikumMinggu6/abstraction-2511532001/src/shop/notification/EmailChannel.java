package shop.notification;

public class EmailChannel extends AbstractChannel {
    @Override
    public String channelName() { return "Email"; }

    @Override
    protected String resolveRecipient(CustomerContact contact) {
        return contact.getEmail().contains("@") ? contact.getEmail() : "";
    }

    @Override
    protected boolean deliver(String recipient, String message) {
        System.out.println("[EMAIL to " + recipient + "] " + message);
        return true;
    }
}
