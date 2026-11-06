package shop.notification;

public class WhatsAppChannel extends AbstractChannel {
    @Override
    public String channelName() { return "WhatsApp"; }

    @Override
    protected String resolveRecipient(CustomerContact contact) {
        String phone = contact.getPhone();
        return phone.length() >= 10 && (phone.startsWith("08") || phone.startsWith("+62"))
                ? phone : "";
    }

    @Override
    protected String prepare(String message) {
        return "[Toko UMKM] " + message;
    }

    @Override
    protected boolean deliver(String recipient, String message) {
        System.out.println("[WA to " + recipient + "] " + message);
        return true;
    }
}
