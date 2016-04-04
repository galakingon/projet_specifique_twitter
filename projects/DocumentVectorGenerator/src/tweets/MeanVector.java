package tweets;

import words.Vocabulary;

/**
 * Created by paul on 07/03/16.
 */
public class MeanVector {

    double[] meanVector;

    public MeanVector(){
    }

    public MeanVector(String text, Vocabulary v){
        String[] words = text.split(" ");
        int nbWords = 0;

        meanVector = new double[400];
        for(int i = 0; i < meanVector.length; i++){
            meanVector[i] = 0;
        }

        for(String s : words){
            if(v.contains(s)){
                double[] vec = v.getWord(s).getVector();
                int i = 0;
                for(double value : vec){
                    meanVector[i] = value + meanVector[i];
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