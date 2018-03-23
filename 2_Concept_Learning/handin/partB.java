import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by xiaoyic on 9/15/17.
 */
public class partB {

    public static void main(String[] args) throws IOException {
        // 1. size of the input space
        int X = (int)Math.pow(2, 4);
        System.out.println(X);
        // 2. size of the concept space
        int C = (int)Math.pow(2, X);
        System.out.println(C);

        // 3. List-Then-Eliminate
        String trainPath = "4Cat-Train.labeled";
        // training data
        List<List<String>> attrList = new ArrayList<>();
        int[][] vs = trainVersionSpace(trainPath, C, X, attrList);

        // 4. take votes for test data
        List<String[]> test = readDoc(args[0]);
        for (String[] data : test) {
            int col = getInputColumn(data, attrList);
            int high = 0;
            for (int i = 0; i < vs.length; i++) {
                if (vs[i][col] == 1) {
                    high ++;
                }
            }
            int low = vs.length - high;
            System.out.println(high + " " + low);
        }
    }

    private static int[][] trainVersionSpace(String trainPath, int C, int X, List<List<String>> attrList) throws IOException {
        List<String[]> train = readDoc(trainPath);
        getAttributeList(train, attrList);
        int attrSize = attrList.size();
        // input space
//        List<List<String>> comb = new ArrayList<>();
//        List<String> subset = new ArrayList<>();
//        getInputCombination(comb, subset, attrList, 0);
        // concept space
        // final position is used to keep the condition of a hypothesis: 0 -> removed
        int[][] conceptSpace = new int[C][X + 1];
        for (int i = 0; i < C; i++) {
            String binary = Integer.toBinaryString(i);
            String[] split = binary.split("");
            int j = X - 1;
            for (int si = split.length - 1; si >= 0; si--, j--) {
                conceptSpace[i][j] = Integer.parseInt(split[si]);
            }
            conceptSpace[i][X] = 1;
        }
        // Train
        for (String[] data : train) {
            int col = getInputColumn(data, attrList);
            String label = data[attrSize];
            int code = 0;
            if (label.equals("high")) {
                code = 1;
            }
            for (int i = 0; i < C; i++) {
                // 0 -> hypothesis has been deleted from H
                if (conceptSpace[i][X] == 1 && conceptSpace[i][col] != code) {
                    conceptSpace[i][X] = 0;
                }
            }
        }
        // create version space and calculate the size of vs
        int vsSize = 0;
        for (int[] h : conceptSpace) {
            if (h[X] == 1) {
                vsSize ++;
            }
        }
        System.out.println(vsSize);

        int[][] vs = new int[vsSize][X];
        int index = 0;
        for (int i = 0; i < C; i++) {
            if (conceptSpace[i][X] == 1) {
                for (int j = 0; j < X; j++) {
                    vs[index][j] = conceptSpace[i][j];
                }
                index ++;
            }
        }
        return vs;
    }

    private static int getInputColumn(String[] data, List<List<String>> attrList) {
        int col = 0;
        int bin = 0;
        int ai = 0;
        int attrSize = attrList.size();
        // find out the input's index in combination which will be used to modify conceptSpace
        for (String attr : data) {
            // attr is label of the current training data
            if (ai == attrSize) {
                break;
            }
            if (attr.equals(attrList.get(ai).get(1))) {
                bin = 1;
            }
            col = col * 2 + bin;
            bin = 0;
            ai ++;
        }
        return col;
    }

    private static List<String[]> readDoc(String path) throws IOException {
        List<String[]> input = new ArrayList<>();
        InputStreamReader isr = new InputStreamReader(new FileInputStream(new File(path)), "UTF-8");
        BufferedReader br = new BufferedReader(isr);
        String line;
        int index = 0;
        while ((line = br.readLine()) != null) {
            String[] attr = line.split("[\t ]+");
            int size = attr.length;
            input.add(new String[size / 2]);
            for (int i = 1; i < size; i += 2) {
                int j = (i - 1)/2;
                input.get(index)[j] = attr[i];
            }
            index ++;
        }
        return input;
    }

    private static void getAttributeList(List<String[]> train, List<List<String>> attrList) {
        int attrSize = train.get(0).length - 1;
        for (int i = 0; i < attrSize; i++) {
            attrList.add(new ArrayList<>());
        }
        for (int i = 0; i < train.size(); i++) {
            for (int j = 0; j < attrSize; j++) {
                if (!attrList.get(j).contains(train.get(i)[j])) {
                    attrList.get(j).add(train.get(i)[j]);
                }
            }
        }
    }

    private static void getInputCombination(List<List<String>> comb,
                                            List<String> subset,
                                            List<List<String>> attrList,
                                            int startIndex) {
        if (subset.size() == attrList.size()) {
            comb.add(new ArrayList<String>(subset));
            return;
        }

        for (int i = 0; i < attrList.get(0).size(); i++) {
            for (int j = startIndex; j < attrList.size(); j++) {
                subset.add(attrList.get(j).get(i));
                getInputCombination(comb, subset, attrList, j + 1);
                subset.remove(subset.size() - 1);
            }
        }
    }
}
