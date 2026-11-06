package shop.payment;
public interface InstallmentPayment extends PaymentMethod {
    int maxInstallmentMonths();
    default String policy() {
        return "Cicilan maksimal " + maxInstallmentMonths() + " bulan";
    }
    /** Monthly amount, rounded up. */
    default long monthlyInstallment(long amount, int months) {
        if (months < 1 || months > maxInstallmentMonths()) {
            throw new IllegalArgumentException(
                    "Months must be between 1 and " + maxInstallmentMonths());
        }
        return (amount + months - 1) / months;
    }
}
