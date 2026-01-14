package org.example;

public class Main {
    public static void main(String[] args) {
        LexicalAnalyzer analyzer = new LexicalAnalyzer();

        String cppFile = "build/resources/main/1.cpp";
        String jsonFile = "build/resources/main/token.json";

        analyzer.lexicalAnalysis(cppFile, jsonFile);

        LexicalAnalyzer analyzerHashTable = new LexicalAnalyzer();
        analyzerHashTable.lexicalAnalysis(cppFile, jsonFile);
    }
}
