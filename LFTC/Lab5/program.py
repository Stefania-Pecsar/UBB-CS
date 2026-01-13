class LL1Parser:
    """Parser LL(1) pentru ambele parti ale temei"""
    
    def __init__(self):
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = ""
        self.productions = {}
        self.first = {}
        self.follow = {}
        self.table = {}
        self.stack = []
        self.derivation = []
    
    # ==================== PARTEA 1 ====================
    
    def read_grammar_from_file(self, filename):
        """Citeste gramatica din fisierul dat"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            if len(lines) < 3:
                print("EROARE: Fisierul trebuie sa contina cel putin 3 linii!")
                return False
            
            self.non_terminals = set(lines[0].split())
            
            self.terminals = set(lines[1].split())
            
            self.start_symbol = lines[2].strip()
            if self.start_symbol not in self.non_terminals:
                print(f"EROARE: Simbolul de start '{self.start_symbol}' nu este neterminal!")
                return False
            
            self.productions = {nt: [] for nt in self.non_terminals}
            
            for line in lines[3:]:
                if '->' not in line:
                    continue
                    
                left, right = line.split('->', 1)
                left = left.strip()
                right = right.strip()
                
                if left not in self.non_terminals:
                    print(f"EROARE: Neterminal necunoscut '{left}' in productie!")
                    return False
                
                alternatives = [alt.strip() for alt in right.split('|')]
                
                for alt in alternatives:
                    alt = alt.replace('epsilon', 'ε')
                    alt = alt.replace('Îµ', 'ε')
                    
                    if alt == 'ε':
                        symbols = ['ε']
                    else:
                        symbols = alt.split()
                    
                    for sym in symbols:
                        if sym != 'ε' and sym not in self.non_terminals and sym not in self.terminals:
                            print(f"EROARE: Simbol necunoscut '{sym}' in productie!")
                            return False
                    
                    self.productions[left].append(symbols)
            
            print(f"Gramatica citita cu succes din {filename}")
            return True
            
        except FileNotFoundError:
            print(f"EROARE: Fisierul '{filename}' nu a fost gasit!")
            return False
        except Exception as e:
            print(f"EROARE la citirea gramaticii: {e}")
            return False
    
    
    def compute_first_sets(self):
        """Calculeaza multimile FIRST """
        self.first = {}
        
        for t in self.terminals:
            self.first[t] = {t}
        
        for nt in self.non_terminals:
            self.first[nt] = set()
        
        self.first['ε'] = {'ε'}
        
        changed = True
        while changed:
            changed = False
            
            for nt in self.non_terminals:
                for production in self.productions[nt]:
                    first_of_prod = self._first_of_sequence(production)
                    
                    old_size = len(self.first[nt])
                    self.first[nt].update(first_of_prod)
                    
                    if len(self.first[nt]) > old_size:
                        changed = True
        
        return True
    
    def _first_of_sequence(self, sequence):
        """Calculeaza FIRST pentru o secventa de simboluri"""
        result = set()
        all_contain_epsilon = True
        
        for symbol in sequence:
            if symbol == 'ε':
                result.add('ε')
                break
            
            if symbol in self.first:
                result.update(self.first[symbol] - {'ε'})
            
            if 'ε' not in self.first.get(symbol, set()):
                all_contain_epsilon = False
                break
        
        if all_contain_epsilon:
            result.add('ε')
        
        return result
    
    def compute_follow_sets(self):
        """Calculeaza multimile FOLLOW"""
        self.follow = {nt: set() for nt in self.non_terminals}
        self.follow[self.start_symbol].add('$')
        
        changed = True
        while changed:
            changed = False
            
            for nt in self.non_terminals:
                for production in self.productions[nt]:
                    follow_temp = self.follow[nt].copy()
                    
                    for i in range(len(production)-1, -1, -1):
                        symbol = production[i]
                        
                        if symbol in self.non_terminals:
                            old_size = len(self.follow[symbol])
                            self.follow[symbol].update(follow_temp)
                            
                            if len(self.follow[symbol]) > old_size:
                                changed = True
                            
                            if 'ε' in self.first.get(symbol, set()):
                                follow_temp.update(self.first.get(symbol, set()) - {'ε'})
                            else:
                                follow_temp = self.first.get(symbol, set()).copy()
                        else:
                            follow_temp = self.first.get(symbol, set()).copy()
        
        return True
    
    # ==================== CONSTRUIRE TABELA LL(1) ====================
    
    def build_ll1_table(self):
        """Construieste tabela de parsare LL(1)"""
        self.table = {nt: {} for nt in self.non_terminals}
        
        for nt in self.non_terminals:
            for production in self.productions[nt]:
                first_of_prod = self._first_of_sequence(production)
                
                for terminal in first_of_prod:
                    if terminal != 'ε' and terminal in self.terminals:
                        if terminal in self.table[nt]:
                            print(f"CONFLICT LL(1): [{nt}, {terminal}] are multiple productii!")
                            print(f"  Existenta: {self.table[nt][terminal]}")
                            print(f"  Noua: {production}")
                            return False
                        self.table[nt][terminal] = production
                
                if 'ε' in first_of_prod:
                    for terminal in self.follow[nt]:
                        if terminal in self.table[nt]:
                            print(f"CONFLICT LL(1): [{nt}, {terminal}] are multiple productii!")
                            print(f"  Existenta: {self.table[nt][terminal]}")
                            print(f"  Noua: {production}")
                            return False
                        self.table[nt][terminal] = production
        
        return True
    
    # ==================== PARSARE INPUT ====================
    
    def parse_input_string(self, input_string):
        """Parseaza o secventa de intrare folosind tabela LL(1)"""
        # Initializare
        self.stack = ['$', self.start_symbol]
        input_tokens = input_string.strip().split() + ['$']
        self.derivation = []
        
        print(f"\nPARSARE: '{input_string}'")
        print(f"Stiva initiala: {self.stack}")
        print(f"Input initial: {input_tokens}")
        
        step = 1
        while self.stack:
            top = self.stack.pop()
            current_token = input_tokens[0]
            
            print(f"\n--- Pas {step} ---")
            print(f"Stiva: {self.stack} (top: '{top}')")
            print(f"Input: {input_tokens}")
            
            if top == '$' and current_token == '$':
                print("Parsare finalizata cu succes!")
                return True
            
            elif top == current_token:
                print(f"Match terminal: consumam '{current_token}'")
                input_tokens.pop(0)
            
            elif top in self.non_terminals:
                if current_token in self.table[top]:
                    production = self.table[top][current_token]
                    print(f"Expandare: {top} -> {' '.join(production)}")
                    
                    self.derivation.append(f"{top} -> {' '.join(production)}")
                    
                    for symbol in reversed(production):
                        if symbol != 'ε':
                            self.stack.append(symbol)
                else:
                    print(f"EROARE: Nu exista productie pentru [{top}, {current_token}]")
                    return False
            
            else:
                print(f"EROARE: '{top}' nu se potriveste cu '{current_token}'")
                return False
            
            step += 1
        
        return False
    
    # ==================== PARTEA 2 ====================
    
    def init_minilanguage_grammar(self):
        """Initializeaza gramatica pentru minilimbaj"""
    
        self.non_terminals = {
            'PROG', 'DECLS', 'DECL', 'TYPE', 'VARLIST', 'VARLISTP',
            'STMTS', 'STMT', 'ASSIGN', 'IF', 'WHILE', 'EXPR', 
            'EXPRP', 'TERM', 'TERMP', 'FACTOR'
        }
        
        self.terminals = {
            'int', 'real', 'id', 'num', ';', ',', '=', 
            'if', 'then', 'else', 'while', 'do',
            '+', '-', '*', '/', '(', ')', '$'
        }
        
        self.start_symbol = 'PROG'
        
        self.productions = {
            'PROG': [['DECLS', 'STMTS']],
            'DECLS': [['DECL', ';', 'DECLS'], ['ε']],
            'DECL': [['TYPE', 'VARLIST']],
            'TYPE': [['int'], ['real']],
            'VARLIST': [['id', 'VARLISTP']],
            'VARLISTP': [[',', 'id', 'VARLISTP'], ['ε']],
            'STMTS': [['STMT', ';', 'STMTS'], ['ε']],
            'STMT': [['ASSIGN'], ['IF'], ['WHILE']],
            'ASSIGN': [['id', '=', 'EXPR']],
            'IF': [['if', 'EXPR', 'then', 'STMTS', 'else', 'STMTS']],
            'WHILE': [['while', 'EXPR', 'do', 'STMTS']],
            'EXPR': [['TERM', 'EXPRP']],
            'EXPRP': [['+', 'TERM', 'EXPRP'], ['-', 'TERM', 'EXPRP'], ['ε']],
            'TERM': [['FACTOR', 'TERMP']],
            'TERMP': [['*', 'FACTOR', 'TERMP'], ['/', 'FACTOR', 'TERMP'], ['ε']],
            'FACTOR': [['id'], ['num'], ['(', 'EXPR', ')']]
        }
        
        print("Gramatica minilimbajului initializata")
    
    def load_fip_from_file(self, filename):
        tokens = []
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if '(' in line and ')' in line:
                        line = line.strip('()')
                        parts = line.split(',')
                        if len(parts) >= 2:
                            code = parts[0].strip()
                            value = parts[1].strip().strip('"')
                            
                            if code == 'ID':
                                tokens.append('id')
                            elif code == 'CONST':
                                tokens.append('num')
                            elif code in ['INT', 'REAL']:
                                tokens.append(value.lower())
                            else:
                                tokens.append(value)
                    else:
                        tokens.append(line)
            
            print(f"Incarcat {len(tokens)} token-uri din {filename}")
            return tokens
            
        except FileNotFoundError:
            print(f"Fisierul {filename} nu a fost gasit. Folosesc exemplu default.")
            return ['int', 'id', ';', 'id', '=', 'num', ';']
    
    
    def print_grammar_info(self):
        """Afiseaza informatii despre gramatica"""
        print("\n" + "="*60)
        print("INFORMATII GRAMATICA")
        print("="*60)
        
        print(f"\nNeterminale ({len(self.non_terminals)}):")
        print("  " + ", ".join(sorted(self.non_terminals)))
        
        print(f"\nTerminale ({len(self.terminals)}):")
        print("  " + ", ".join(sorted(self.terminals)))
        
        print(f"\nSimbol de start: {self.start_symbol}")
        
        print("\nProductii:")
        for nt in sorted(self.non_terminals):
            if nt in self.productions:
                for prod in self.productions[nt]:
                    print(f"  {nt} -> {' '.join(prod)}")
    
    def print_first_follow(self):
        """Afiseaza multimile FIRST si FOLLOW"""
        print("\n" + "="*60)
        print("MULTIMI FIRST SI FOLLOW")
        print("="*60)
        
        print("\nFIRST:")
        for nt in sorted(self.non_terminals):
            if nt in self.first:
                print(f"  FIRST({nt}) = {{{', '.join(sorted(self.first[nt]))}}}")
        
        print("\nFOLLOW:")
        for nt in sorted(self.non_terminals):
            if nt in self.follow:
                print(f"  FOLLOW({nt}) = {{{', '.join(sorted(self.follow[nt]))}}}")
    
    def print_ll1_table(self):
        """Afiseaza tabela LL(1)"""
        print("\n" + "="*60)
        print("TABELA LL(1) - EXTRAS")
        print("="*60)
        
        for nt in sorted(self.non_terminals)[:3]: 
            if nt in self.table and self.table[nt]:
                print(f"\n{nt}:")
                for terminal in sorted(self.table[nt].keys())[:5]:  
                    prod = self.table[nt][terminal]
                    print(f"  [{terminal}] -> {' '.join(prod)}")

def partea1_gramatica_custom():
    """Partea 1: Analiza sintactica pentru gramatica din fisier"""
    print("\n" + "="*70)
    print("PARTEA 1: ANALIZA SINTACTICA LL(1) PENTRU GRAMATICA DIN FISIER")
    print("="*70)
    
    parser = LL1Parser()
    
    grammar_file = input("\nIntrodu numele fisierului cu gramatica (ex: gramatica.txt): ").strip()
    if not grammar_file:
        grammar_file = "gramatica.txt"
    
    if not parser.read_grammar_from_file(grammar_file):
        print("Nu pot continua fara o gramatica valida.")
        return
    
    parser.print_grammar_info()
    
    print("\nCalculare multimi FIRST (non-recursiv)...")
    parser.compute_first_sets()
    
    print("Calculare multimi FOLLOW (non-recursiv)...")
    parser.compute_follow_sets()
    
    parser.print_first_follow()
    
    print("\nConstruire tabela LL(1)...")
    if parser.build_ll1_table():
        print("Gramatica este LL(1)! Tabela construita cu succes.")
        parser.print_ll1_table()
    else:
        print("Gramatica NU este LL(1)! Exista conflicte in tabela.")
        print("Consultati indrumatorul pentru transformarea gramaticii.")
        return
    
    print("\n" + "-"*70)
    input_seq = input("Introdu secventa de intrare (ex: 'a b' ): ").strip()
    
    if not input_seq:
        print("Secventa vida. Folosesc exemplu default: 'a b'")
        input_seq = "a b"
    
    success = parser.parse_input_string(input_seq)
    
    if success:
        print("\n" + "="*70)
        print("SECVENTA ACCEPTATA!")
        print("="*70)
        
        print("\nDerivarea completa:")
        for i, step in enumerate(parser.derivation, 1):
            print(f"  {i:2d}. {step}")
        
        print(f"\nSecventa '{input_seq}' este acceptata de gramatica!")
    else:
        print("\n" + "="*70)
        print("SECVENTA RESPINSA!")
        print("="*70)
        print(f"\nSecventa '{input_seq}' NU este acceptata de gramatica!")

def partea2_minilimbaj():
    """Partea 2: Analiza sintactica pentru program minilimbaj"""
    print("\n" + "="*70)
    print("PARTEA 2: ANALIZA SINTACTICA LL(1) PENTRU MINILIMBAJ")
    print("="*70)
    
    parser = LL1Parser()
    
    parser.init_minilanguage_grammar()
    parser.print_grammar_info()
    
    print("\nCalculare multimi FIRST (non-recursiv)...")
    parser.compute_first_sets()
    
    print("Calculare multimi FOLLOW (non-recursiv)...")
    parser.compute_follow_sets()
    
    parser.print_first_follow()
    
    print("\nConstruire tabela LL(1)...")
    if parser.build_ll1_table():
        print("Gramatica minilimbajului este LL(1)!")
        parser.print_ll1_table()
    else:
        print("Gramatica NU este LL(1)! Exista conflicte.")
        print("Consultati indrumatorul pentru transformarea gramaticii.")
        return
    
    print("\n" + "-"*70)
    fip_file = input("Introdu numele fisierului FIP (enter pentru exemplu): ").strip()
    
    if fip_file:
        tokens = parser.load_fip_from_file(fip_file)
    else:
        print("Folosesc exemplu default.")
        tokens = parser.load_fip_from_file("fip.txt") 
        
    input_for_parser = ' '.join(tokens)
    print(f"\nToken-uri pentru parsare: {input_for_parser}")
    
    success = parser.parse_input_string(input_for_parser)
    
    if success:
        print("\n" + "="*70)
        print("PROGRAM CORECT SINTACTIC!")
        print("="*70)
        
        print("\nAnaliza sintactica completa:")
        for i, step in enumerate(parser.derivation, 1):
            print(f"  {i:2d}. {step}")
        
        print(f"\nProgramul este corect sintactic!")
    else:
        print("\n" + "="*70)
        print("EROARE SINTACTICA IN PROGRAM!")
        print("="*70)
        print(f"\nProgramul contine erori sintactice!")

def main():
    """Functia principala cu meniu"""
    print("\n" + "="*70)
    print("TEMA 5: ANALIZA SINTACTICA LL(1)")
    print("Implementare non-recursiva pentru FIRST si FOLLOW")
    print("="*70)
    
    while True:
        print("\nMENIU PRINCIPAL")
        print("1. Partea 1: Analiza sintactica pentru gramatica din fisier")
        print("2. Partea 2: Analiza sintactica pentru program minilimbaj")
        print("0. Iesire")
        
        try:
            optiune = input("\nAlege o optiune (1, 2 sau 0): ").strip()
            
            if optiune == "1":
                partea1_gramatica_custom()
            elif optiune == "2":
                partea2_minilimbaj()
            elif optiune == "0":
                print("\nLa revedere!")
                break
            else:
                print("Optiune invalida! Incearca din nou.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupt. Iesire...")
            break
        except Exception as e:
            print(f"\nEroare neasteptata: {e}")

if __name__ == "__main__":
    main()