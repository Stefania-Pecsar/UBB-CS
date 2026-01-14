package org.prudconsum;

import org.prudconsum.method.Parallel;
import org.prudconsum.method.ParallelV2;
import org.prudconsum.method.Sequential;
import org.prudconsum.utils.FileManagment;
import org.prudconsum.utils.Generator;

import java.io.FileNotFoundException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Objects;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        //ca si arg tip -> sequential/parallel/parallelV2
        //nrOfReaderThreads si nrOfWriterThreads -> nr threaduri
        String type = args[0];
        int nrOfReaderThreads = Integer.parseInt(args[1]);
        int nrOfWriterThreads = Integer.parseInt(args[2]);

        //generez datele daca nu le am
        if(!Files.exists(Paths.get("src/main/resources/input_data"))) {
            Generator.generate();
        }

        double start = System.nanoTime();
        if(Objects.equals(type, "sequential"))
        {
            Sequential.run();
        }
        else if(Objects.equals(type, "parallel"))
        {
            Parallel.run(nrOfReaderThreads, nrOfWriterThreads);
            FileManagment fileManagment = new FileManagment();
            assert fileManagment.areFilesEqual("resultsSequential.txt","resultsParallel.txt");
            System.out.println("Fisierele sunt identice.");
        }
        else if(Objects.equals(type, "parallelV2"))
        {
            ParallelV2.run(nrOfReaderThreads, nrOfWriterThreads);
            FileManagment fileManagment = new FileManagment();
            assert fileManagment.areFilesEqual("resultsSequential.txt","resultsParallel.txt");
            System.out.println("Fisierele sunt identice.");
        }
        double end = System.nanoTime();
        System.out.println((end-start)/1e6); //mili
    }
}