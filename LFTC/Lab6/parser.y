%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

extern int yylex();
extern FILE *yyin;
extern int lineNumber;
void yyerror(char *s);

void generate_asm_header();
void generate_asm_footer();
void generate_asm_read(char *name);
void generate_asm_write(char *name);
void generate_asm_assign(char *name, char *value);
char* generate_asm_expr(char *op, char *left, char *right); 
void generate_int_to_str();
void generate_asm_str_to_int();

int add_symbol(char *name);
char* get_symbol_address(char *name);

#define MAX_SYMBOLS 100
typedef struct {
    char name[50];
    int address;
} Symbol;

Symbol symbol_table[MAX_SYMBOLS];
int symbol_count = 0;
int temp_counter = 0; // Contor pt var temporare

int add_symbol(char *name) {
    for (int i = 0; i < symbol_count; i++) {
        if (strcmp(symbol_table[i].name, name) == 0) {
            return symbol_table[i].address;
        }
    }
    strcpy(symbol_table[symbol_count].name, name);
    symbol_table[symbol_count].address = symbol_count * 4;
    return symbol_count++;
}

char* get_symbol_address(char *name) {
    for (int i = 0; i < symbol_count; i++) {
        if (strcmp(symbol_table[i].name, name) == 0) {
            return symbol_table[i].name;
        }
    }
    printf("Eroare: Variabila %s nu este declarata.\n", name);
    exit(1);
}

void generate_asm_header() {
    printf("section .data\n");
    for (int i = 0; i < symbol_count; i++) {
        printf("%s dd 0\n", symbol_table[i].name);
    }
    // Generam sp pt var temporare (temp0 ... temp99)
    for (int i = 0; i < 100; i++) {
        printf("temp%d dd 0\n", i);
    }
    printf("\n");
    printf("input_buffer db 0,0,0,0,0,0,0,0,0,0,0,0 ; buffer mai mare\n");
    printf("output_buffer db 0,0,0,0,0,0,0,0,0,0,0,0 ;\n");
    printf("\n");
    printf("section .text\n");
    printf("global _start\n");
    printf("\n");
    printf("_start:\n");
}

void generate_asm_footer() {
    printf("    mov eax, 1\n");
    printf("    xor ebx, ebx\n");
    printf("    int 0x80\n");
    generate_int_to_str();
    generate_asm_str_to_int();
}

void generate_asm_read(char *name) {
    printf("    mov eax, 3\n");
    printf("    mov ebx, 0\n");
    printf("    lea ecx, [input_buffer]\n");
    printf("    mov edx, 10\n");
    printf("    int 0x80\n");
    printf("\n");
    printf("    lea esi, [input_buffer]\n");
    printf("    xor eax, eax\n");
    printf("    call clean_and_convert\n");
    printf("    mov [%s], eax\n", name);
    printf("\n");
}

void generate_asm_str_to_int() {
    printf("clean_and_convert:\n");
    printf("    xor eax, eax\n");
    printf("    xor ecx, ecx\n");
    printf("\n");
    printf(".convert_loop:\n");
    printf("    movzx edx, byte [esi + ecx]\n");
    printf("    cmp dl, 0xA\n");
    printf("    je .done_conversion\n");
    printf("    cmp dl, 0xD\n");
    printf("    je .done_conversion\n");
    printf("    test dl, dl\n");
    printf("    je .done_conversion\n");
    printf("    sub dl, '0'\n");
    printf("    imul eax, eax, 10\n");
    printf("    add eax, edx\n");
    printf("    inc ecx\n");
    printf("    jmp .convert_loop\n");
    printf("\n");
    printf(".done_conversion:\n");
    printf("    ret\n");
    printf("\n");
}

void generate_asm_write(char *name) {
   
    if (isdigit(name[0])) printf("    mov eax, %s\n", name);
    else printf("    mov eax, [%s]\n", name);
    
    printf("\n");
    printf("    call int_to_str\n");
    printf("\n");
    printf("    mov byte [output_buffer + 10], 0\n");
    printf("    mov byte [output_buffer + 9], 0xA\n");
    printf("    mov eax, 4\n");
    printf("    mov ebx, 1\n");
    printf("    lea ecx, [output_buffer]\n");
    printf("    mov edx, 11\n");
    printf("    int 0x80\n");
    printf("\n");
}

void generate_int_to_str() {
    printf("\n");
    printf("int_to_str:\n");
    printf("    push ebx\n");
    printf("    push ecx\n");
    printf("    push edx\n");
    printf("    mov ecx, output_buffer +9\n");
    printf("    mov byte [ecx], 0\n");
    printf("    mov ebx, 10\n");
    printf("\n");
    printf(".loop:\n");
    printf("    dec ecx\n");
    printf("    xor edx, edx\n");
    printf("    div ebx\n");
    printf("    add dl, '0'\n");
    printf("    mov [ecx], dl\n");
    printf("    test eax, eax\n");
    printf("    jnz .loop\n");
    printf("\n");
    printf("    pop edx\n");
    printf("    pop ecx\n");
    printf("    pop ebx\n");
    printf("    ret\n");
    printf("\n");
}

void generate_asm_assign(char *name, char *value) {

    if (isdigit(value[0])) {
        printf("    mov dword [%s], %s\n", name, value);
    } else {
        printf("    mov eax, [%s]\n", value);
        printf("    mov dword [%s], eax\n", name);
    }
}

char* generate_asm_expr(char *op, char *left, char *right) {
    // Folosim un buffer static pentru numele temporarului
    static char temp_name[20];
    sprintf(temp_name, "temp%d", temp_counter++);
    
    if (isdigit(left[0])) {
        printf("    mov eax, %s\n", left);
    } else {
        printf("    mov eax, [%s]\n", left);
    }

    if (strcmp(op, "+") == 0) {
        if (isdigit(right[0])) printf("    add eax, %s\n", right);
        else printf("    add eax, [%s]\n", right);
    } else if (strcmp(op, "-") == 0) {
        if (isdigit(right[0])) printf("    sub eax, %s\n", right);
        else printf("    sub eax, [%s]\n", right);
    } else if (strcmp(op, "*") == 0) {
        if (isdigit(right[0])) printf("    imul eax, %s\n", right);
        else printf("    imul eax, [%s]\n", right);
    }
    
    // Salvam in variabila temporara noua
    printf("    mov dword [%s], eax\n", temp_name);
    
    return strdup(temp_name);
}
%}

%union {
    int ival;
    char *sval;
}

%token <ival> DECIMAL
%token <sval> ID
%token INT CIN COUT ASSIGN PLUS MINUS MUL SEMICOLON OUT IN COMMA

%start program

%type <sval> instructiune expresie termen factor lista_variabile declarare

%%

program: lista_instructiuni { generate_asm_footer(); };

lista_instructiuni: instructiune
                  | instructiune lista_instructiuni;

instructiune: declarare { generate_asm_header(); }
             | atribuire { $$ = NULL; }
             | intrare { $$ = NULL; }
             | iesire { $$ = NULL; };

declarare: INT lista_variabile SEMICOLON { $$ = NULL; };

lista_variabile: ID { add_symbol($1); }
               | lista_variabile COMMA ID { add_symbol($3); };

atribuire: ID ASSIGN expresie SEMICOLON { 
    generate_asm_assign($1, $3); 
};

/*  rez return de generate_asm_expr ($$) */
expresie: termen { $$ = $1; }
        | expresie PLUS termen { 
            $$ = generate_asm_expr("+", $1, $3); 
          }
        | expresie MINUS termen { 
            $$ = generate_asm_expr("-", $1, $3); 
          }
        ;

termen: factor { $$ = $1; }
      | termen MUL factor { 
          $$ = generate_asm_expr("*", $1, $3); 
        }
      ;

factor: ID { $$ = get_symbol_address($1); }
      | DECIMAL { 
            char buffer[20];
            snprintf(buffer, sizeof(buffer), "%d", $1);
            $$ = strdup(buffer);
        }
      ;

intrare: CIN IN ID SEMICOLON { generate_asm_read($3); };

iesire: COUT OUT ID SEMICOLON { generate_asm_write($3); };

%%

int main(int argc, char *argv[]) {
    ++argv, --argc;
    if (argc > 0) {
        yyin = fopen(argv[0], "r");
        if (!yyin) {
            printf("Eroare: Nu pot deschide fisierul %s\n", argv[0]);
            return 1;
        }
    } else {
        yyin = stdin;
    }

    yyparse();

    fprintf(stderr, "%s", "Fisierul este corect sintactic!\n");
    return 0;
}

void yyerror(char *s) {
    extern char* yytext;
    fprintf(stderr, "Eroare sintactica pentru simbolul %s la linia: %d.\n", yytext, lineNumber);
    exit(1);
}