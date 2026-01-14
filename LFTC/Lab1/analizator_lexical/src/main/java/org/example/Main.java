package org.example;

public class Main {
    public static void main(String[] args) {
        LexicalAnalyzer analyzer = new LexicalAnalyzer();

        String cppFile = "build/resources/main/raza.cpp";
        String jsonFile = "build/resources/main/token.json";

        analyzer.lexicalAnalysis(cppFile, jsonFile);

        LexicalAnalyzer analyzerHashTable = new LexicalAnalyzer();
        analyzerHashTable.lexicalAnalysis(cppFile, jsonFile);
    }
}
