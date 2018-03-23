import java.io.*;

/**
 * Created by xiaoyic on 9/15/17.
 */
public class DocHandler {

    public static void main(String[] args) throws IOException {
        String path = "hw2data/9Cat-Train.labeled";
        FileWriter writer = new FileWriter("output.txt");
        InputStreamReader isr = new InputStreamReader(new FileInputStream(new File(path)), "UTF-8");
        BufferedReader br = new BufferedReader(isr);
        String line;
        int count = 0;
        while ((line = br.readLine()) != null) {
            String[] kv = line.split("[\t ]+");
            count ++;
            if (kv[kv.length - 1].equals("low")) {
                continue;
            }
            StringBuilder sb = new StringBuilder();
            sb.append(count + "\t");
            for (int i = 0; i < 9; i++) {
                sb.append(kv[2 * i + 1] + "\t");
            }
            sb.deleteCharAt(sb.lastIndexOf("\t"));
            sb.append("\n");
            writer.write(sb.toString());
        }
        writer.close();
        isr.close();
        br.close();
    }
}
