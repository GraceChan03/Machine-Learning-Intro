import java.io.*;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by xiaoyic on 9/14/17.
 */
public class partA {
    static String POSITIVE = "high";
    static String NEGATIVE = "low";

    public static void main(String[] args) {
        // 1. the size of the input space
        int X = (int)Math.pow(2, 9);
        System.out.println(X);
        // 2. the number of decimal digit in the size of concept space
        String C = Double.toString(Math.pow(2, X));
        int index = C.indexOf('E');
        String decimalDigit = C.substring(index + 1);
        System.out.println(Integer.parseInt(decimalDigit) + 1);
        // 3. the size of the hypothesis space H
        int H = 1 + (int)Math.pow(3, 9);
        System.out.println(H);
        // 4. new size of hypothesis space:
        //    add a new binary feature to dataset
        int H1 = 1 + (int)Math.pow(3, 10);
        System.out.println(H1);
        // 5. new size of hypothesis space:
        //    a feature can take on 3 different values
        int H2 = 1 + 4 * (int)Math.pow(3, 8);
        System.out.println(H2);

        // 6. FIND-S
        String trainPath = "9Cat-Train.labeled";
        try {

            Map<Integer, String> map = new HashMap<>();
            for (int i = 0; i < 9; i++) {
                map.put(i, null);
            }
            int count = 0;
            FileWriter writer = new FileWriter("partA6.txt");
            InputStreamReader isrTrain = new InputStreamReader(new FileInputStream(new File(trainPath)), "UTF-8");
            BufferedReader brTrain = new BufferedReader(isrTrain);
            String line;
            while ((line = brTrain.readLine()) != null) {
                String[] kv = line.split("[\t ]+");
                count++;
                // print the current hypothesis every 30 instances
                if (count == 30) {
                    StringBuilder sb = new StringBuilder();
                    for(int i = 0; i < 9; i++) {
                        sb.append(map.get(i) + "\t");
                    }
                    sb.deleteCharAt(sb.lastIndexOf("\t"));
                    sb.append("\n");
                    writer.write(sb.toString());
                    count = 0;
                }
                if (kv[kv.length - 1].equals(NEGATIVE)) {
                    continue;
                }
                // a(i) -> h(2 * i + 1)
                for (int i = 0; i < 9; i++) {
                    if (map.get(i) == null) {
                        map.put(i, kv[2 * i + 1]);
                    } else if (!map.get(i).equals(kv[2 * i + 1])){
                        map.put(i, "?");
                    }
                }
            }
            writer.close();
            isrTrain.close();
            brTrain.close();

            // 7. apply the final hypothesis to "9Cat-Dev.labeled"
            String devPath = "9Cat-Dev.labeled";
            InputStreamReader isrDev = new InputStreamReader(new FileInputStream(new File(devPath)), "UTF-8");
            BufferedReader brDev = new BufferedReader(isrDev);
            Map<Integer, String> finalH = new HashMap<>();
            for (Integer key : map.keySet()) {
                if (map.get(key).equals("?")) {
                    continue;
                }
                finalH.put(key, map.get(key));
            }
            int mis = 0, total = 0;
            while ((line = brDev.readLine()) != null) {
                String[] kv = line.split("[\t ]+");
                String label = kv[kv.length - 1];
                total ++;
                boolean match = true;
                for (Integer key : finalH.keySet()) {
                    if (!finalH.get(key).equals(kv[2 * key + 1])) {
                        match = false;
                        break;
                    }
                }
                if (match && !label.equals(POSITIVE)) {
                    mis ++;
                } else if (!match && label.equals(POSITIVE)) {
                    mis ++;
                }
            }
            if (total != 0) {
                double misRate = 1.0 * mis / total;
                System.out.println(misRate);
            }
            isrDev.close();
            brDev.close();

            // 8. apply the final hypothesis to input file
            InputStreamReader isrTest = new InputStreamReader(new FileInputStream(new File(args[0])), "UTF-8");
            BufferedReader brTest = new BufferedReader(isrTest);
            while ((line = brTest.readLine()) != null) {
                String[] kv = line.split("[\t ]+");
                boolean match = true;
                for (Integer key : finalH.keySet()) {
                    if (!finalH.get(key).equals(kv[2 * key + 1])) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    System.out.println(POSITIVE);
                } else {
                    System.out.println(NEGATIVE);
                }
            }
            isrTest.close();
            brTest.close();

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
