package words;

/**
 * Created by paul on 22/03/16.
 */
public class Word {

    String word;
    double[] vector;


    public Word(String word, double[] vector){
        this.word = word;
        this.vector = vector;
    }

    public double[] getVector(){
        return vector;
    }
}