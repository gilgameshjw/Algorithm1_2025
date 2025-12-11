package team.ae.algorithms.triemap.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import team.ae.algorithms.triemap.dto.Item;
import team.ae.algorithms.triemap.dto.LoadRequest;
import team.ae.algorithms.triemap.dto.SearchResultDto;
import team.ae.algorithms.triemap.util.KMeansSimple;
import team.ae.algorithms.triemap.util.TextVectorizer;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * In-memory search and clustering service.
 * <p>
 * Responsibilities:
 * 1) Load textual items from JSON (data.json or request payload).
 * 2) Vectorize items using character-based vectors and run K-Means clustering.
 * 3) Provide cluster-aware semantic search using Bag-of-Words + cosine similarity.
 */
@Service
public class InMemorySearchService {

    private final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * All items loaded in memory. Each item knows its clusterId and character vector.
     */
    private volatile List<Item> items = List.of();

    /**
     * Centroids produced by K-Means clustering.
     * centroids[clusterIndex] is the numeric vector of that cluster center.
     */
    private volatile double[][] centroids = new double[0][];

    /**
     * How many clusters we consider during search.
     * For example, if there are 10 clusters in total,
     * we may search only in the 3 best matching clusters.
     */
    private static final int MAX_CLUSTERS_TO_USE_IN_SEARCH = 3;

    // -------------------------------------------------------------------------
    // Loading
    // -------------------------------------------------------------------------

    /**
     * Loads items from classpath resource "static/data.json" and runs clustering.
     * This method is synchronized to avoid concurrent reloads that could
     * corrupt the shared items/centroids state.
     */
    public synchronized Map<String, Object> loadFromClasspath() {
        try (InputStream inputStream =
                     new ClassPathResource("static/data.json").getInputStream()) {

            LoadRequest request = objectMapper.readValue(inputStream, LoadRequest.class);
            return load(request);

        } catch (Exception exception) {
            throw new RuntimeException("Failed to load static/data.json", exception);
        }
    }

    /**
     * Loads items from request DTO, vectorizes them and runs K-Means clustering.
     * This method is synchronized to ensure that items and centroids are updated
     * atomically in a multi-threaded environment.
     */
    public synchronized Map<String, Object> load(LoadRequest request) {
        List<String> texts = request.texts() == null ? List.of() : request.texts();
        int requestedClusterCount = Math.max(1, request.kClusters());

        int numberOfItems = texts.size();
        double[][] allVectors = new double[numberOfItems][];
        List<Item> temporaryItems = new ArrayList<>(numberOfItems);

        // 1) Vectorize all texts using character-based 48-dimensional vectors.
        for (int index = 0; index < numberOfItems; index++) {
            String text = texts.get(index);
            double[] vector = TextVectorizer.toCharacterVector48(text);
            allVectors[index] = vector;
            temporaryItems.add(new Item("id-" + index, text, vector, -1));
        }

        // 2) Run K-Means clustering if we have any items.
        if (numberOfItems > 0) {
            int actualClusterCount = Math.min(requestedClusterCount, numberOfItems);
            KMeansSimple kMeans = new KMeansSimple(actualClusterCount, 50);
            KMeansSimple.Result result = kMeans.fit(allVectors);

            for (int i = 0; i < numberOfItems; i++) {
                int clusterId = result.labels[i];
                temporaryItems.set(i, temporaryItems.get(i).withCluster(clusterId));
            }
            this.centroids = result.centroids;
        } else {
            this.centroids = new double[0][];
        }

        // 3) Publish the new immutable snapshot of items.
        this.items = List.copyOf(temporaryItems);

        return Map.of(
                "items", items.size(),
                "kClusters", centroids.length
        );
    }

    // -------------------------------------------------------------------------
    // Cluster-aware semantic search
    // -------------------------------------------------------------------------

    /**
     * Performs semantic search using Bag-of-Words + cosine similarity.
     * <p>
     * Steps:
     * 1) Convert the query to Bag-of-Words.
     * 2) Select the best matching clusters for the query using character-based vectors.
     * 3) For items from these clusters, compute cosine similarity in BOW space.
     * 4) Sort by similarity (descending) and return top-K as SearchResultDto.
     */
    public List<SearchResultDto> searchCosine(String query, int topK) {
        if (topK <= 0 || items.isEmpty()) {
            return List.of();
        }

        Map<String, Integer> queryBagOfWords = TextVectorizer.toBagOfWords(query);

        // If there are no centroids, this set will be empty and we will search in all items.
        Set<Integer> allowedClusters = selectBestClustersForQuery(query, MAX_CLUSTERS_TO_USE_IN_SEARCH);

        List<SearchResultDto> scoredResults = new ArrayList<>();

        for (Item item : items) {
            // If clustering is enabled, skip items that do not belong to selected clusters.
            if (!allowedClusters.isEmpty() && !allowedClusters.contains(item.clusterId())) {
                continue;
            }

            Map<String, Integer> documentBagOfWords = TextVectorizer.toBagOfWords(item.text());
            double similarity =
                    TextVectorizer.cosineFromBagOfWords(queryBagOfWords, documentBagOfWords);

            scoredResults.add(new SearchResultDto(
                    item.id(),
                    item.text(),
                    item.clusterId(),
                    similarity
            ));
        }

        // Sort by similarity (largest first).
        scoredResults.sort((first, second) ->
                Double.compare(second.similarity(), first.similarity()));

        if (scoredResults.size() > topK) {
            return scoredResults.subList(0, topK);
        }
        return scoredResults;
    }

    /**
     * Selects best-matching clusters for a given query using character-based vectors
     * and cosine similarity between the query vector and each cluster centroid.
     * <p>
     * If there are no centroids, returns an empty set, and the caller should
     * interpret this as "do not restrict by cluster" (search in all items).
     */
    private Set<Integer> selectBestClustersForQuery(String query, int maxClustersToUse) {
        if (centroids == null || centroids.length == 0) {
            return Set.of();
        }

        double[] queryVector = TextVectorizer.toCharacterVector48(query);

        List<Map.Entry<Integer, Double>> clusterSimilarities = new ArrayList<>();
        for (int clusterIndex = 0; clusterIndex < centroids.length; clusterIndex++) {
            double similarity = TextVectorizer.cosine(queryVector, centroids[clusterIndex]);
            clusterSimilarities.add(Map.entry(clusterIndex, similarity));
        }

        // Sort clusters by similarity descending.
        clusterSimilarities.sort((first, second) ->
                Double.compare(second.getValue(), first.getValue()));

        int limit = Math.min(maxClustersToUse, clusterSimilarities.size());
        Set<Integer> result = new HashSet<>();
        for (int i = 0; i < limit; i++) {
            result.add(clusterSimilarities.get(i).getKey());
        }
        return result;
    }

    // -------------------------------------------------------------------------
    // Cluster inspection APIs
    // -------------------------------------------------------------------------

    /**
     * Returns list of cluster ids (0..k-1).
     */
    public List<Integer> clusterIds() {
        List<Integer> ids = new ArrayList<>();
        for (int i = 0; i < centroids.length; i++) {
            ids.add(i);
        }
        return ids;
    }

    /**
     * Returns up to 'limit' items from the given cluster.
     * This endpoint is mainly for inspection and UI display.
     */
    public List<Item> byCluster(int clusterId, int limit) {
        List<Item> bucket = new ArrayList<>();
        for (Item item : items) {
            if (item.clusterId() == clusterId) {
                bucket.add(item);
            }
        }
        if (bucket.size() <= limit) {
            return bucket;
        }
        return bucket.subList(0, limit);
    }

    /**
     * Returns all items currently loaded in memory.
     */
    public List<Item> all() {
        return items;
    }

}
