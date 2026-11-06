package review.fixed;

import java.util.ArrayList;
import java.util.List;
import shop.discount.Discountable;
import shop.payment.PaymentMethod;
import shop.shipping.ExpressShipping;
import shop.shipping.ShippingService;

public class BadShopRefactored {
    public static void main(String[] args) {
        Cart cart = new Cart();
        cart.add(new Cart.Item("Kopi Gayo", 85_000, 2));
        System.out.println("Total cart: " + cart.total());
        ShippingService courier = new ExpressShipping();
        System.out.println("Ongkir Ekspres 2 kg: " + courier.calculateCost(2_000));
        Address home = new Address("Jl. Sudirman 10", "Padang");
        SimpleOrder first = new SimpleOrder("ORD-1", home);
        SimpleOrder second = new SimpleOrder("ORD-2", new Address(home.getStreet(), "Bukittinggi"));
        System.out.println(first);
        System.out.println(second);
        Discountable flashSale = new FlashSaleDiscount();
        System.out.println("Harga flash sale: " + flashSale.applyDiscount(100_000));
        GiftVoucher voucher = new GiftVoucher();
        PaymentMethod payment = voucher;
        System.out.println(payment.pay(30_000) + " | sisa Rp" + voucher.getBalance());
    }
}

final class GiftVoucher implements PaymentMethod {
    private long balance = 100_000;
    @Override
    public String getName() { return "Voucher"; }
    @Override
    public boolean pay(long amount) {
        if (amount <= 0 || amount > balance) {
            return false;
        }
        balance -= amount;
        return true;
    }
    public long getBalance() { return balance; }
}

class Cart {
    private final List<Item> items = new ArrayList<>();
    static class Item {
        private final String name;
        private final long price;
        private final int quantity;
        Item(String name, long price, int quantity) {
            if (name == null || name.isBlank() || price < 0 || quantity <= 0) {
                throw new IllegalArgumentException("Invalid cart item");
            }
            this.name = name;
            this.price = price;
            this.quantity = quantity;
        }
        long subtotal() { return price * quantity; }
        String getName() { return name; }
    }
    void add(Item item) {
        if (item == null) {
            throw new IllegalArgumentException("Item is required");
        }
        items.add(item);
    }
    long total() {
        long total = 0;
        for (Item item : items) {
            total += item.subtotal();
        }
        return total;
    }
}

final class Address {
    private final String street;
    private final String city;
    Address(String street, String city) {
        if (street == null || street.isBlank() || city == null || city.isBlank()) {
            throw new IllegalArgumentException("Street and city are required");
        }
        this.street = street;
        this.city = city;
    }
    String getStreet() { return street; }
    String getCity() { return city; }
    @Override
    public String toString() { return street + ", " + city; }
}

final class SimpleOrder {
    private final String id;
    private final Address address;
    SimpleOrder(String id, Address address) {
        if (id == null || id.isBlank() || address == null) {
            throw new IllegalArgumentException("Order id and address are required");
        }
        this.id = id;
        this.address = address;
    }
    Address getAddress() { return address; }
    @Override
    public String toString() { return id + " -> " + address; }
}

class MemberDiscount implements Discountable {
    @Override
    public int discountPercent() { return 5; }
}

class FlashSaleDiscount implements Discountable {
    @Override
    public int discountPercent() { return 30; }
}
