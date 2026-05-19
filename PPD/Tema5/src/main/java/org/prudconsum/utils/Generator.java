package org.prudconsum.utils;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Generator {

    public static String generateString()
    {
        Random random = new Random();
        int length = random.nextInt(10);
        StringBuilder stringBuilder = new StringBuilder();
        for (int i = 0; i < length; i++) {
            stringBuilder.append((char) (random.nextInt(26) + 'a'));
        }
        return stringBuilder.toString();
    }
    public static void generate() {

        try {
            Files.createDirectories(Paths.get(Constants.OUTPUT_DIR));
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        Random random = new Random();

        List<String> participants = new ArrayList<>();
        for (int i = 1; i <= Constants.NO_OF_PARTICIPANTS; i++) {
            participants.add("S" + i);
        }

        for (int problem = 1; problem <= Constants.NO_OF_PROBLEMS; problem++) {
            String filePath = Constants.OUTPUT_DIR + "/proiect" + problem + ".txt";

            try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {

                int noOfNotes = Constants.MIN_NO_OF_NOTES +
                        random.nextInt(Constants.NO_OF_PARTICIPANTS - Constants.MIN_NO_OF_NOTES + 1);

                List<Integer> availableIndices = new ArrayList<>();
                for(int i = 0; i < Constants.NO_OF_PARTICIPANTS; i++) {
                    availableIndices.add(i);
                }

                // Iterăm pentru numărul necesar de note
                for (int i = 0; i < noOfNotes; i++) {

                    int listIndex = random.nextInt(availableIndices.size());

                    int participantIndex = availableIndices.get(listIndex);

                    availableIndices.remove(listIndex); // Eliminăm indexul pentru a asigura unicitatea

                    String participant = participants.get(participantIndex);
                    int score = random.nextInt(101); // Am schimbat 'nota' în 'score'

                    // Format corect: ID spațiu Nota
                    writer.write( participant + " " + score );
                    writer.newLine();
                }

                System.out.println("Fișier " + filePath + " generat cu " + noOfNotes + " note");

            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        System.out.println("Toate fișierele de input au fost generate în: " + Constants.OUTPUT_DIR);
    }
}