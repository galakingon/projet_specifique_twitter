package data;

import tweets.Tweet;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Created by paul on 07/03/16.
 */
public class Dataset {

    Map<String, double[]> dataset;
    int vectorLength;

    public Dataset(){
    }

    public Dataset(Collection<String> labels, double[][] values) {
        int i = 0;
        dataset = new HashMap<String, double[]>();
        for (String s : labels) {
            dataset.put(s, values[i]);
            i++;
        }
    }

    public Dataset(File f){
        dataset = new HashMap<String, double[]>();
        try {
            BufferedReader bf = new BufferedReader(new FileReader(f));
            while (bf.ready()) {
                String s = bf.readLine();
                String[] cells = s.split(" ");

                String key = cells[0];
                double[] values = new double[cells.length-1];
                for(int i = 1; i < cells.length; i++){
                    values[i-1] = Double.parseDouble(cells[i]);
                }
                dataset.put(key, values);
                vectorLength = values.length;
            }
            bf.close();
        } catch (IOException exception) {
            System.out.println("Erreur lors de la lecture : " + exception.getMessage());
        }
    }

    public boolean contains(String s) {
        return dataset.containsKey(s);
    }

    public double[] getVector(String s) {
        return dataset.get(s);
    }

    public Collection<String> keySet(){return dataset.keySet();}

    public int getVectorLength(){
        return vectorLength;
    }
}