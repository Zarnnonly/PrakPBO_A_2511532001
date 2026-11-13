import shop.shipping.ShippingService;

public class PercobaanL4 extends ShippingService {
    public PercobaanL4() {
        super("Gratis");
    }

    @Override
    protected long ratePerKg() {
        return 0;
    }

    @Override
    public long calculateCost(int weightGrams) {
        return 0;
    }
}