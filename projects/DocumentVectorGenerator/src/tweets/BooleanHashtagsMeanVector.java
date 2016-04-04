package tweets;

import words.Vocabulary;
import java.util.ArrayList;

/**
 * Created by paul on 01/04/16.
 */
public class BooleanHashtagsMeanVector extends MeanVector{

    double[] booleanHashtagsMeanVector;

    public BooleanHashtagsMeanVector(){

    }

    public BooleanHashtagsMeanVector(String text, Vocabulary v, ArrayList<String> hashtags){
        String[] words = text.split(" ");
        int nbWords = 0;

        meanVector = new double[v.getVectorLength()];
        for(int i = 0; i < meanVector.length; i++){
            meanVector[i] = 0;
        }

        for(String s : words){
            if(v.contains(s) && hashtags.contains(s)){
                double[] word_vec = v.getWord(s).getVector();
                for(int i =0; i<meanVector.length; i++){
                    meanVector[i] = word_vec[i] + meanVector[i];
                    i++;
                }
                nbWords++;
            }
        }

        for(int i = 0; i< meanVector.length; i++){
            meanVector[i] /= nbWords;
        }
    }
}
