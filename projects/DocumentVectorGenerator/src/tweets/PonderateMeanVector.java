package tweets;

import words.Vocabulary;

import java.util.Map;

/**
 * Created by paul on 22/03/16.
 */
public class PonderateMeanVector extends MeanVector {

    double[] ponderateMeanVector;

    public PonderateMeanVector(){
    }

    public PonderateMeanVector(String text, Vocabulary v, Map<String, Double> tf){
        String[] words = text.split(" ");
        int nbWords = 0;

        meanVector = new double[v.getVectorLength()];
        for(int i = 0; i < meanVector.length; i++){
            meanVector[i] = 0;
        }

        for(String s : words){
            if(v.contains(s)){
                double[] word_vec = v.getWord(s).getVector();
                double coef = v.idf(s)*tf.get(s);
                for(int i =0; i<meanVector.length; i++){
                    meanVector[i] = word_vec[i]*coef + meanVector[i];
                    i++;
                }
                nbWords++;
            }
        }

        for(int i = 0; i< meanVector.length; i++){
            meanVector[i] /= nbWords;
        }
    }

    public double[] getMeanVector() {
        return meanVector;
    }
}