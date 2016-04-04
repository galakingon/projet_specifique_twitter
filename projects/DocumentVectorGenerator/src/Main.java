import data.Dataset;
import words.Vocabulary;
import tweets.Tweet;

import java.io.*;
import java.util.ArrayList;

/**
 * Created by paul on 07/03/16.
 */
public class Main {

    public static void main(String[] args) {

        System.out.println("debut");
        Vocabulary vocab = new Vocabulary(new Dataset(new File(args[0])));

        File tweets_file = new File(args[1]);
        ArrayList<Tweet> tweets = new ArrayList<Tweet>();
        try {
            BufferedReader bf = new BufferedReader(new FileReader(tweets_file));
            int i = 0;

            while (bf.ready()) {
                tweets.add(new Tweet(bf.readLine()));
                i++;
            }

            bf.close();

        } catch (IOException exception) {
            System.out.println("Erreur lors de la lecture : " + exception.getMessage());
        }

        if(args[3].equals("tfidf")){
            vocab.calculateIdfOverTweets(tweets);


            for(Tweet t : tweets){
                t.calculatePonderateMeanVector(vocab);
            }

        }
        if(args[3].equals("hashtags")){
            File hashtags_file = new File(args[4]);
            ArrayList<String> hashtags = new ArrayList<String>();
            try {
                BufferedReader bf = new BufferedReader(new FileReader(hashtags_file));

                while (bf.ready()) {
                    hashtags.add(bf.readLine());
                }

                bf.close();

            } catch (IOException exception) {
                System.out.println("Erreur lors de la lecture : " + exception.getMessage());
            }

            for(Tweet t : tweets){
                t.calculateHashtagsMeanVector(vocab, hashtags);
            }
        }

        try{
            FileWriter fw = new FileWriter(new File(args[2]));
            fw.write("id");
            for(int i = 1; i <=100; i++){
                fw.write(" , ");
                fw.write(String.valueOf(i));
            }
            fw.write("\n\r");

            int i = 1;
            for(Tweet t : tweets){
                fw.write((String.valueOf(i)));
                double[] values = t.getDocumentVector().getMeanVector();
                for(double v : values){
                    fw.write(",");
                    fw.write(String.valueOf(v));
                }
                fw.write("\n\r");
                i++;
            }

            fw.close();
        }
        catch(Exception e){

        }
    }

}