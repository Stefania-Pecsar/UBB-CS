#!/bin/bash


rm -f parser lex.yy.c parser.tab.c parser.tab.h program program.o program2 program2.o program_test program_test.o
bison -d parser.y
flex flex.l
gcc lex.yy.c parser.tab.c -o parser -lfl

echo "=========================================="
echo "--- Rulare code.txt ---"
./parser < code.txt > program.asm
nasm -f elf32 program.asm -o program.o
ld -m elf_i386 program.o -o program
./program
echo "" 

# 3. Rulare test2.txt
echo "=========================================="
echo "--- Rulare test2.txt ---"
./parser < test2.txt > program2.asm
nasm -f elf32 program2.asm -o program2.o
ld -m elf_i386 program2.o -o program2
./program2
echo ""

# 4. Rulare test.txt
echo "=========================================="
echo "--- Rulare test.txt ---"
./parser < test.txt > program_test.asm
nasm -f elf32 program_test.asm -o program_test.o
ld -m elf_i386 program_test.o -o program_test
./program_test
echo ""
echo "=========================================="