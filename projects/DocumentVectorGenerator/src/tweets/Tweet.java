package tweets;

import words.Vocabulary;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;

/**
 * Created by paul on 07/03/16.
 */
public class Tweet {

    String text;
    MeanVector documentVector;
    HashMap<String, Double> tf;

    public Tweet(){
    }

    public Tweet(String text){
        this.text = text;
        documentVector = new MeanVector();
        tf = new HashMap<String, Double>();

        for(String s : text.split(" ")){
            if(!tf.containsKey(s)) tf.put(s, new Double(1));
            else tf.put(s, tf.get(s)+1);
        }

        for(String s : tf.keySet()){
            tf.put(s, tf.get(s)/tf.size());
        }
    }

    public void calculateDocumentVector(Vocabulary v){
        documentVector = new MeanVector(text, v);
    }

    public void calculatePonderateMeanVector(Vocabulary v){
        documentVector = new PonderateMeanVector(text, v, (Map<String, Double>) tf);
    }

    public void calculateHashtagsMeanVector(Vocabulary v, ArrayList<String> hashtags){
        documentVector = new BooleanHashtagsMeanVector(text, v, hashtags);
    }

    public String getText() {
        return text;
    }

    public MeanVector getDocumentVector(){
        return documentVector;
    }

    public double getTF(String word){
        return tf.get(word);
    }

    public Collection<String> words(){
        return tf.keySet();
    }

    public void deleteWords(ArrayList<String> wordsToDelete){
        for(String word : wordsToDelete){
            if(tf.containsKey(word)){
                tf.remove(word);
            }
        }
    }
}