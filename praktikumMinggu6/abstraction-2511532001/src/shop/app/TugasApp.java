package shop.app;

import java.util.List;
import shop.StudentInfo;
import shop.model.DigitalProduct;
import shop.model.PhysicalProduct;
import shop.model.Product;
import shop.notification.*;
import shop.payment.*;
import shop.service.CheckoutService;
import shop.shipping.ExpressShipping;
import shop.shipping.ShippingService;

public class TugasApp {
    public static void main(String[] args) {
        System.out.println("Tugas oleh " + StudentInfo.NAME + " (" + StudentInfo.NIM + ")");
        List<Product> cart = List.of(
                new PhysicalProduct("KOPI-001", "Kopi Arabika Gayo 250g", 85_000, 300),
                new PhysicalProduct("RDG-002", "Rendang Kemasan 250g", 120_000, 400),
                new DigitalProduct("EBK-003", "E-book Resep Kue Nusantara", 50_000,
                        "https://toko-umkm.example/unduh/ebk-003"));
        CheckoutService checkout = new CheckoutService();
        ShippingService express = new ExpressShipping();
        EWalletPayment wallet = new EWalletPayment("DompetKu", 300_000);
        CreditCardPayment card = new CreditCardPayment("Siti Rahma", 1_000_000);
        List<PaymentMethod> payments = List.of(wallet, new BankTransferPayment("Bank Nagari"), card);
        System.out.println("\n== T1: Total dengan biaya admin (Ekspres) ==");
        for (PaymentMethod payment : payments) {
            System.out.println(payment.getName() + " : Rp" + checkout.grandTotal(cart, express, payment)
                    + " (admin Rp" + payment.adminFee(checkout.total(cart, express)) + ")");
        }
        System.out.println("\nKebijakan kartu kredit : " + card.policy());
        System.out.println("Kebijakan e-wallet     : " + wallet.policy());
        NotificationService notifications = new NotificationService();
        notifications.register(new EmailChannel());
        notifications.register(new SmsChannel(StudentInfo.SMS_MAX_LENGTH));
        notifications.register(new WhatsAppChannel());
        notifications.register(new NotificationChannel() {
            @Override
            public String channelName() { return "Log konsol"; }

            @Override
            public boolean send(CustomerContact contact, String message) {
                if (contact == null || message == null || message.isBlank()) {
                    return false;
                }
                System.out.println("[LOG] " + contact.getName() + ": " + message);
                return true;
            }
        });
        String message = "Pesanan ORD-0001 sudah dikirim dengan kurir Ekspres. "
                + "Nomor resi akan muncul di aplikasi dalam 1x24 jam. "
                + "Terima kasih telah berbelanja produk UMKM Sumatera Barat di toko kami! "
                + "Silakan periksa alamat tujuan dan hubungi layanan pelanggan jika membutuhkan bantuan.";
        System.out.println("\n== T2: Notifikasi status pesanan ==");
        for (CustomerContact contact : List.of(
                new CustomerContact("Siti Rahma", "siti@example.com", "081234567890"),
                new CustomerContact("Budi", null, "+6281298765432"))) {
            int sent = notifications.broadcast(contact, message);
            System.out.println("Terkirim ke " + contact.getName() + " lewat " + sent + " kanal");
        }
    }
}
