package shop.demo;

/** L2 part D: run from the terminal with different arguments. */
public class CariProdukDemo {

    public static void main(String[] args) {
        String[] skus = {"KOPI-001", "RDG-002", "TEH-004"};
        try {
            if (args.length == 0) {
                throw new IllegalArgumentException("Berikan satu nomor produk.");
            }
            int number = Integer.parseInt(args[0]);
            System.out.println("D1 SKU: " + skus[number - 1]);
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        } catch (NumberFormatException e) {
            System.out.println(e.getMessage());
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println(e.getMessage());
        } finally {
            System.out.println("D5 pencarian selesai");
        }
    }
}
