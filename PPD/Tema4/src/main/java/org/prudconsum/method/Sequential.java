package org.prudconsum.method;

import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.linkedList.LinkedListE;
import org.prudconsum.utils.Constants;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.util.Scanner;

public class Sequential {
    public static void  run() throws FileNotFoundException {
        LinkedList list = new LinkedList();

        for(int i = 1; i <= Constants.NO_OF_PROBLEMS; i++) {
            File file = new File(Constants.OUTPUT_DIR+ "/proiect"+i+".txt");
            Scanner scanner = new Scanner(file);

            while (scanner.hasNext()) {
                String participant = scanner.next();
                Integer nota = scanner.nextInt();
                LinkedListE element = new LinkedListE(participant, nota);
                list.addOrUpdate(element);
            }
            scanner.close();
        }
        try(BufferedWriter writer = new BufferedWriter(new FileWriter("resultsSequential.txt")))
        {
            while(list.getHead() != null)
            {
                writer.write(list.getHead().participant + " " + list.getHead().nota + "\n");
                list.remove(list.getHead().participant);
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}
