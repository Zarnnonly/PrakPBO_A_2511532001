import shop.payment.BankTransferPayment;
import shop.service.CheckoutService;

public class PercobaanL3 {
    public static void main(String[] args) {
        CheckoutService checkout = new CheckoutService();

        checkout.refund(new BankTransferPayment("Bank Nagari"), 1000);
    }
}