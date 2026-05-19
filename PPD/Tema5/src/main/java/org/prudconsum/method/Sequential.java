package org.prudconsum.method;

import org.prudconsum.linkedList.LinkedList;
import org.prudconsum.linkedList.LinkedListE;
import org.prudconsum.utils.Constants;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class Sequential {
    public static void run() throws FileNotFoundException {
        LinkedList list = new LinkedList();
        Set<String> blackList = new HashSet<>();

        for (int i = 1; i <= Constants.NO_OF_PROBLEMS; i++) {
            File file = new File(Constants.OUTPUT_DIR + "/proiect" + i + ".txt");
            Scanner scanner = new Scanner(file);

            while (scanner.hasNext()) {
                String participant = scanner.next();
                Integer nota = scanner.nextInt();
                if(nota == -1)
                {
                    blackList.add(participant);
                    if(list.search(participant) != null)
                    {
                        list.remove(participant);
                    }
                }

                if(!blackList.contains(participant))
                {
                    LinkedListE element = new LinkedListE(participant, nota);
                    list.addOrUpdate(element);
                }
            }
        }

        LinkedList sortedList = new LinkedList();
        LinkedListE nodeToMove;
        while ((nodeToMove = list.extractHead()) != null) {
            sortedList.insertSorted(nodeToMove);
        }

        try(BufferedWriter writer = new BufferedWriter(new FileWriter("resultsSequential.txt")))
        {
            while(sortedList.getHead()!= null)
            {
                writer.write(sortedList.getHead().participant+" "+sortedList.getHead().nota+"\n");
                sortedList.remove(sortedList.getHead().participant);
            }
        } catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}