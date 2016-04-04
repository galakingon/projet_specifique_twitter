package words;

import data.Dataset;
import tweets.Tweet;
import words.Word;

import java.util.*;

/**
 * Created by paul on 22/03/16.
 */
public class Vocabulary{


    Map<String, Word> vocab;
    Map<String, Double> idf;
    int vectorLength;

    public Vocabulary(Dataset d){
        vocab = new HashMap<String, Word>();
        idf = new HashMap<String, Double>();

        vectorLength = d.getVectorLength();
        for(String s : d.keySet()){
            vocab.put(s, new Word(s, d.getVector(s)));
            idf.put(s, new Double(0));
        }
    }

    public void calculateIdfOverTweets(ArrayList<Tweet> tweets) {
        for (Tweet t : tweets) {
            for(String s : t.words()){
                if(this.contains(s)) idf.put(s, idf.get(s)+1);
            }
        }
        for(String s : idf.keySet()){
            idf.put(s, Math.log(tweets.size()/idf.get(s)));
        }
    }

    public boolean contains(String word){
        return vocab.containsKey(word);
    }

    public Word getWord(String word){
        return vocab.get(word);
    }

    public Double idf(String word){
        return idf.get(word);
    }

    public int getVectorLength(){
        return vectorLength;
    }
}

