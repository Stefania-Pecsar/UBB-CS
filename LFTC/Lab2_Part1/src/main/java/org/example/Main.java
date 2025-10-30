package org.example;

import org.example.AF.*;

import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    static AutomateFinite finiteAutomata = new AutomateFinite();
    public static void printMenu(){
        System.out.println("Introduceti optiunea: ");
        System.out.println("1. Citeste automatul din fisier!");
        System.out.println("2. Citeste automatul de la tastatura!");
        System.out.println("3. Afiseaza BNF-ul pentru formatul fisierului automatului!");
        System.out.println("4. Verifica daca o secventa este acceptata de automat - AFD!");
        System.out.println("5. Afieaza cel mai lung prefix al unei secvente care este acceptat de automat - AFD!");
        System.out.println("6. Afiseaza multimea starilor automatului!");
        System.out.println("7. Afiseaza multimea simbolurilor alfabetului automatului!");
        System.out.println("8. Afiseaza multimea starilor finale ale automatului!");
        System.out.println("9. Afiseaza multimea tranzitiilor automatului!");
        System.out.println("10. Afiseaza starea initiala a automatului!");
        System.out.println("11. Afiseaza intregul automat!");
        System.out.println("12. Iesire!");


    }
    public static AutomateFinite readAutomataFromConsole(){
        AutomateFinite finiteAutomata = new AutomateFinite();
        Scanner scanner = new Scanner(System.in);
        int numberOfStates, numberOfAlphabetSymbols, numberOfFinalStates, numberOfTransitions;
        while(true) {
            try {
                Stare initialState;
                System.out.println("Introduceti numarul de stari:");

                numberOfStates = Integer.parseInt(scanner.nextLine());
                List<Stare> states = new ArrayList<>();
                for (int i = 0; i < numberOfStates; i++) {
                    System.out.println("Introduceti starea:");
                    states.add(new Stare(scanner.nextLine(), StareType.NORMAL));
                }
                finiteAutomata.setAllStates(states);
                System.out.println("Introduceti numarul de simboluri ale alfabetului:");
                numberOfAlphabetSymbols = Integer.parseInt(scanner.nextLine());
                List<Alfabet> alphabetList = new ArrayList<>();
                for (int i = 0; i < numberOfAlphabetSymbols; i++) {
                    System.out.println("Introduceti simbolul alfabetului:");
                    alphabetList.add(new Alfabet(scanner.nextLine()));
                }
                System.out.println("Introduceti numarul de stari finale:");
                numberOfFinalStates = Integer.parseInt(scanner.nextLine());
                List<Stare> finalStates = new ArrayList<>();
                for (int i = 0; i < numberOfFinalStates; i++) {
                    System.out.println("Introduceti starea finala:");
                    finalStates.add(new Stare(scanner.nextLine(), StareType.FINAL));
                }
                System.out.println("Introduceti starea initiala:");
                initialState = new Stare(scanner.nextLine(), StareType.INITIAL);

                System.out.println("Introduceti numarul de tranzitii:");
                numberOfTransitions = Integer.parseInt(scanner.nextLine());
                List<Tranzitie> transitions = new ArrayList<>();
                for (int i = 0; i < numberOfTransitions; i++) {
                    System.out.println("Introduceti tranzitia:");
                    transitions.add(Tranzitie.stringToTransition(scanner.nextLine()));
                }
                finiteAutomata.setInitialState(initialState);
                finiteAutomata.setFinalStates(finalStates);
                finiteAutomata.setTransitions(transitions);
                finiteAutomata.setAlphabet(alphabetList);
                break;
            } catch (Exception e) {
                System.out.println("Intrare invalida! Doriti sa incercati din nou? (da/nu)");
                String option = scanner.nextLine();
                if(option.equals("nu")) {
                    break;
                }

            }
        }
        return finiteAutomata;
    }
    public static void doAction(String option)
    {

        switch (option){
            case "1":
            {
                // read the automata from file
                Scanner scanner = new Scanner(System.in);
                System.out.println("Introduceti calea catre fisier:");
                String path = scanner.nextLine();
                try {
                    finiteAutomata = FileManager.readAF("src/main/resources/"+path);
                    System.out.println("Automatul a fost citit cu succes!");
                } catch (Exception e) {
                    System.out.println("Eroare la citirea automatului din fisier!");
                    System.out.println("Detalii eroare: " + e.getMessage());
                }
                System.out.println(finiteAutomata);

                break;

            }
            case "2":
            {
                // read the automata from keyboard
                finiteAutomata = readAutomataFromConsole();
                break;
            }
            case "3":
            {
                // show the BNF for the file format of automata
                System.out.println(finiteAutomata.getBNF());
                break;
            }

            case "4":
            {
                // verify if a sequence is accepted by the automata - AFD
                Scanner scanner = new Scanner(System.in);
                System.out.println("Introduceti secventa ");
                String sequence = scanner.nextLine();
                if(finiteAutomata.acceptsSequence(sequence)) {
                    System.out.println("Secventa este acceptata de automat!");
                }
                else {
                    System.out.println("Secventa nu este acceptata de automat!");
                }
                break;
            }
            case "5":
            {
                // show the longest prefix of a sequence that is accepted by the automata-AFD
                Scanner scanner = new Scanner(System.in);
                System.out.println("Introduceti secventa: ");
                String sequence = scanner.nextLine();
                String longestPrefix = finiteAutomata.longestPrefixAccepted(sequence);
                PrintWriter out = new PrintWriter(new OutputStreamWriter(System.out, StandardCharsets.UTF_8), true);
                out.println("Cel mai lung prefix al secventei acceptat de automat este: " + longestPrefix);
                break;
            }
            case "6":
            {
                // show the set of states of the automata
                System.out.println("Multimea starilor automatului este: ");
                for(Stare state: finiteAutomata.getAllStates()) {
                    System.out.println(state);
                }
                break;
            }
            case "7":
            {
                // show the set of alphabet symbols of the automata
                System.out.println("Multimea simbolurilor alfabetului automatului este: ");
                for(Alfabet alphabet: finiteAutomata.getAlphabet()) {
                    System.out.println(alphabet);
                }
                break;
            }
            case "8":
            {
                // show the set of final states of the automata
                System.out.println("Multimea starilor finale ale automatului este: ");
                for(Stare state: finiteAutomata.getFinalStates()) {
                    System.out.println(state);
                }
                break;
            }
            case "9":
            {
                // show the set of transitions of the automata
                System.out.println("Multimea tranzitiilor automatului este: ");
                for(Tranzitie transition: finiteAutomata.getTransitions()) {
                    System.out.println(transition);
                }
                break;
            }
            case "10":
            {
                // show the initial state of the automata
                System.out.println("Starea initiala a automatului este: ");
                System.out.println(finiteAutomata.getInitialState());
                break;
            }
            case "11":
            {
                // show the entire automata
                System.out.println(finiteAutomata);
                break;
            }
            case "12":
            {
                // exit
                break;
            }
            default:
            {
                System.out.println("Invalid option!");
                break;
            }


        }
    }

    public static void main(String[] args) {
        String option= "";
        Scanner scanner = new Scanner(System.in);
        while(true)
        {
            printMenu();

            option = scanner.nextLine();
            if(option.equals("12"))
            {
                break;
            }
            doAction(option);
        }
    }
}
