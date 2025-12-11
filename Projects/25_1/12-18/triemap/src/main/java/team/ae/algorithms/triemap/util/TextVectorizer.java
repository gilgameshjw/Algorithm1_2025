package team.ae.algorithms.triemap.util;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * Utility class for simple text vectorization and similarity measures.
 * <p>
 * We use two representations:
 * 1) Bag-of-Words (word -> frequency) for cosine search.
 * 2) Fixed-size character frequency vector (length 48) for clustering.
 */
public final class TextVectorizer {

    private TextVectorizer() {
    }

    // ---------- Bag-of-Words (words) ----------

    private static final Pattern NON_ALNUM_SPLIT = Pattern.compile("[^a-z0-9]+");

    /**
     * Builds a simple Bag-of-Words map: token (lowercased) -> frequency.
     */
    public static Map<String, Integer> toBagOfWords(String text) {
        Map<String, Integer> wordFrequencies = new HashMap<>();
        if (text == null) {
            return wordFrequencies;
        }

        String normalized = text.toLowerCase(Locale.ROOT);
        String[] tokens = NON_ALNUM_SPLIT.split(normalized);

        for (String token : tokens) {
            if (token.isEmpty()) continue;
            wordFrequencies.merge(token, 1, Integer::sum);
        }
        return wordFrequencies;
    }

    /**
     * Computes cosine similarity between two Bag-of-Words maps.
     * Uses standard formula: cos = dot / (||A|| * ||B||).
     */
    public static double cosineFromBagOfWords(Map<String, Integer> first,
                                              Map<String, Integer> second) {
        if (first.isEmpty() || second.isEmpty()) {
            return 0.0;
        }

        // dot product
        double dotProduct = 0.0;
        for (Map.Entry<String, Integer> entry : first.entrySet()) {
            Integer secondValue = second.get(entry.getKey());
            if (secondValue != null) {
                dotProduct += entry.getValue() * secondValue;
            }
        }

        // norms
        double normFirstSquared = 0.0;
        for (int value : first.values()) {
            normFirstSquared += value * value;
        }

        double normSecondSquared = 0.0;
        for (int value : second.values()) {
            normSecondSquared += value * value;
        }

        if (normFirstSquared == 0.0 || normSecondSquared == 0.0) {
            return 0.0;
        }

        return dotProduct / (Math.sqrt(normFirstSquared) * Math.sqrt(normSecondSquared));
    }

    // ---------- Character-based vector (length 48) ----------

    /**
     * We use a fixed alphabet of characters. Each position in the vector
     * counts how many times the corresponding character appears in the text.
     */
    private static final char[] ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789 -_./:@#,+()[]".toCharArray();

    private static final Map<Character, Integer> CHARACTER_INDEX = new HashMap<>();

    static {
        for (int index = 0; index < ALPHABET.length; index++) {
            CHARACTER_INDEX.put(ALPHABET[index], index);
        }
    }

    /**
     * Builds a 48-dimensional vector of character frequencies and applies L2-normalization.
     */
    public static double[] toCharacterVector48(String text) {
        double[] vector = new double[ALPHABET.length];
        if (text == null) {
            return vector;
        }

        String normalized = text.toLowerCase(Locale.ROOT);
        for (int i = 0; i < normalized.length(); i++) {
            char character = normalized.charAt(i);
            Integer index = CHARACTER_INDEX.get(character);
            if (index != null) {
                vector[index] += 1.0;
            }
        }

        l2Normalize(vector);
        return vector;
    }

    /**
     * Applies L2-normalization in-place: v = v / ||v||.
     */
    public static void l2Normalize(double[] vector) {
        double sumSquares = 0.0;
        for (double value : vector) {
            sumSquares += value * value;
        }
        if (sumSquares == 0.0) {
            return;
        }
        double inverseNorm = 1.0 / Math.sqrt(sumSquares);
        for (int i = 0; i < vector.length; i++) {
            vector[i] *= inverseNorm;
        }
    }

    /**
     * Computes cosine similarity between two numeric vectors of the same length.
     * Uses standard formula: cos = dot / (||A|| * ||B||).
     */
    public static double cosine(double[] first, double[] second) {
        if (first == null || second == null || first.length == 0 || first.length != second.length) {
            return 0.0;
        }

        double dotProduct = 0.0;
        double normFirstSquared = 0.0;
        double normSecondSquared = 0.0;

        for (int i = 0; i < first.length; i++) {
            double a = first[i];
            double b = second[i];
            dotProduct += a * b;
            normFirstSquared += a * a;
            normSecondSquared += b * b;
        }

        if (normFirstSquared == 0.0 || normSecondSquared == 0.0) {
            return 0.0;
        }

        return dotProduct / (Math.sqrt(normFirstSquared) * Math.sqrt(normSecondSquared));
    }

}
