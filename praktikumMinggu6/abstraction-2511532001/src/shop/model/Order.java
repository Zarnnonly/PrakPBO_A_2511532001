package shop.model;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
public class Order {
    private final String orderId;
    private final Address shippingAddress;
    private final List<Line> lines = new ArrayList<>();
    public Order(String orderId, Address shippingAddress) {
        if (orderId == null || orderId.isBlank() || shippingAddress == null) {
            throw new IllegalArgumentException("Order id and address are required");
        }
        this.orderId = orderId;
        this.shippingAddress = shippingAddress;
    }
    public String getOrderId() { return orderId; }
    public Address getShippingAddress() { return shippingAddress; }
    public void addLine(Product product, int quantity) {
        lines.add(new Line(product, quantity));
    }
    public List<Line> getLines() { return Collections.unmodifiableList(lines); }

    public long getItemsTotal() {
        long total = 0;
        for (Line line : lines) {
            total += line.subtotal();
        }
        return total;
    }

    public Receipt createReceipt() {
        return new Receipt();
    }

    public static class Line {
        private final Product product;
        private final int quantity;

        public Line(Product product, int quantity) {
            if (product == null || quantity <= 0) {
                throw new IllegalArgumentException("Product and positive quantity are required");
            }
            this.product = product;
            this.quantity = quantity;
        }

        public Product getProduct() { return product; }
        public int getQuantity() { return quantity; }
        public long subtotal() { return product.getFinalPrice() * quantity; }
    }

    public class Receipt {
        public String toText() {
            StringBuilder text = new StringBuilder("STRUK PESANAN " + Order.this.orderId);
            for (Line line : lines) {
                text.append("\n- ").append(line.getProduct().getName())
                        .append(" x").append(line.getQuantity())
                        .append(" = Rp").append(line.subtotal());
            }
            text.append("\nTotal pesanan: Rp").append(getItemsTotal());
            text.append("\nKirim ke: ").append(Order.this.shippingAddress);
            return text.toString();
        }
    }
}
