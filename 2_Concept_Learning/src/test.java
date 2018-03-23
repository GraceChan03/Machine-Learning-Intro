/**
 * Created by xiaoyic on 9/16/17.
 */
public class test {
    public static void main(String[] args) {
        int b = 0;
        String str = Integer.toBinaryString(b);
        System.out.println(str);
        int[] arr = new int[16];
        String[] split = str.split("");
        for (String s : split) {
            System.out.print(s + "\t");
        }
        System.out.println();
        int j = arr.length - 1;
        for (int i = split.length - 1; i >= 0; i--, j--) {
            arr[j] = Integer.parseInt(split[i]);
        }
        for (Integer i : arr) {
            System.out.print(i + "\t");
        }
    }
}
