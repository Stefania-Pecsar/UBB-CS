package org.example;

import java.util.ArrayList;
import java.util.List;

public class TSHashTable {
    private MyHashTable<TSValue> hashTable;
    private List<TSValue> allValues; // Păstrează toate valorile pentru scriere în fișier

    public TSHashTable(int capacity) {
        this.hashTable = new MyHashTable<>(capacity);
        this.allValues = new ArrayList<>();
    }

    public int insert(TSValue value) {
        // Verifică dacă există deja în hash table
        Pair<Integer, Integer> existing = hashTable.get(value);
        if (existing != null) {
            // Caută în allValues pentru poziția globală
            for (TSValue existingValue : allValues) {
                if (existingValue.equals(value)) {
                    return existingValue.getPosition();
                }
            }
        }

        // Inserează noua valoare
        Pair<Integer, Integer> position = hashTable.insert(value);
        int globalPosition = allValues.size();
        value.setPosition(globalPosition);
        allValues.add(value);
        return globalPosition;
    }

    public List<TSValue> getValues() {
        return allValues;
    }

    public List<TSValue> getIdentifiers() {
        List<TSValue> identifiers = new ArrayList<>();
        for (TSValue value : allValues) {
            if ("ID".equals(value.getAtom())) {
                identifiers.add(value);
            }
        }
        return identifiers;
    }

    public List<TSValue> getConstants() {
        List<TSValue> constants = new ArrayList<>();
        for (TSValue value : allValues) {
            if ("CONST".equals(value.getAtom())) {
                constants.add(value);
            }
        }
        return constants;
    }
}