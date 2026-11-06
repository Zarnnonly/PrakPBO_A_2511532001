package shop.model;

import shop.discount.Discountable;

public class DigitalProduct extends Product implements Discountable {
    private static final int DIGITAL_DISCOUNT_PERCENT = 10;
    private String downloadUrl;

    public DigitalProduct(String sku, String name, long price, String downloadUrl) {
        super(sku, name, price);

        if (downloadUrl == null) {
            throw new NullPointerException("downloadUrl Tidak Boleh Kosong");
        }
        this.downloadUrl = downloadUrl;
    }

    public String getDownloadUrl() { return downloadUrl;}

    @Override
    public int discountPercent() {return DIGITAL_DISCOUNT_PERCENT;}

    @Override
    public long getFinalPrice() {return applyDiscount(getPrice());}

    @Override
    public String category() { return "Digital";}
}
