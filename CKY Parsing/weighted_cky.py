from pprint import pprint
from collections import defaultdict 
import string

grammar_rules = []
#lexicon = {}
probabilities = {}
#possible_parents_for_children = {}
possible_parents_for_children = defaultdict(list)
#lexicon_keys = ['Noun', 'Pronoun', 'Proper-Noun', 'Verb', 'Aux', 'Prep', 'Det']

lexicon = {
    'Noun': set(),
    'Pronoun': set(),
    'Proper-Noun': set(),
    'Verb': set(),
    'Aux': set(),
    'Prep': set(),
    'Det': set(),
    'NP': set(),
    'Nominal': set(),
    'VP': set()
    }

def populate_grammar_rules():
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO Fill in your implementation for processing the grammar rules.
    
    pcfg_grammar = open("pcfg_grammar_modified", "r")
    lines = pcfg_grammar.readlines()
    for line in lines:
        if not line.strip(): continue
        left, right = line.split("->")
        left = left.strip()
        len_right = len(right.split(' '))
        #if left not in lexicon.keys():
        if len_right == 3:
            _, probability = right.split('\t')
            children = _.split()
            rule = (left, tuple(children))
            grammar_rules.append(rule)
            probabilities[(left, tuple(children))] = probability.strip()
        else:
            _, probability = right.split('\t')
            lexicon[left].add(_.strip())
            probabilities[(left, _.strip())] = probability.strip()
            
    #possible_parents_for_children = {}
    possible_parents_for_children = defaultdict(list)
    #for parent, (leftchild, rightchild) in grammar_rules:
    for parent, children in grammar_rules:
        if len(children) == 2:
            leftchild = children[0]
            rightchild = children[1]
            if (leftchild, rightchild) not in possible_parents_for_children:
                possible_parents_for_children[leftchild, rightchild] = []
        #else:
        #    leftchild = children[0]
        #    if (leftchild,) not in possible_parents_for_children:
        #        possible_parents_for_children[leftchild,] = []
        possible_parents_for_children[leftchild, rightchild].append(parent)
    
    # Error checking
    all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
    #print 'all_parents',all_parents
    #for par, (leftchild, rightchild) in grammar_rules:
    
    for par, children in grammar_rules:
        if len(children) == 2:
            leftchild = children[0]
            rightchild = children[1]
            if leftchild not in all_parents:
                assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
            if rightchild not in all_parents:
                assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild
        #else:
        #    leftchild = children[0]
        #    if leftchild not in all_parents:
        #        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    #pass
    #print "Grammar rules in tuple form:"
    #pprint(grammar_rules)
    #print "Rule parents indexed by children:"
    #pprint(possible_parents_for_children)
    #print "probabilities"
    #pprint(probabilities)
    #print "Lexicon"
    #pprint(lexicon)


def pcky_parse(sentence):
    # Return the most probable legal parse for the sentence
    # If nothing is legal, return None.
    # This will be similar to cky_parse(), except with probabilities.
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO complete the implementation
    
    N = len(sentence)
    cells = defaultdict(float)
    cells_word = defaultdict(list)
    tags = defaultdict(list)
    for word in sentence:
        for key, value in lexicon.iteritems():            
            if word in value:
                tags[word].append(key)
                
    
    #print 'tags',tags
    backpointers = defaultdict(list)
    
    for i in range(N): 
        for X in tags[sentence[i]]:
            cells[(i, i+1, X)] = probabilities[(X, sentence[i])]
            cells_word[(i, i+1, X)] = sentence[i]
            
        
    print 'cells before updating via cky'
    pprint(cells)
    parseStr = lambda x: x.isalpha() and x or x.isdigit() and \
                             int(x) or x.isalnum() and x or \
                             len(set(string.punctuation).intersection(x)) == 1 and \
                             x.count('.') == 1 and float(x) or x
    # TODO replace the below with an implementation
    for l in range(2, N + 1):
        for m in range(0, N+1-l): 
            end = m + l
            for k in range(m+1, m+l):
                max_score = 0.0
                for grammar_rule in grammar_rules:                    
                    score = parseStr(probabilities[grammar_rule]) * float(cells[(m, k, grammar_rule[1][0])]) * float(cells[(k,m+l, grammar_rule[1][1])])
                    if score > cells[m, end, grammar_rule[0]]:
                        cells[m, m+l, grammar_rule[0]] = score
                        backpointers[(m, m+l, grammar_rule[0])] = [(m,k, grammar_rule[1][0]),(k,m+l,grammar_rule[1][1])]
                        
    print 'backpointers'
    pprint(backpointers)
    #print 'cells'
    #pprint(cells) 
    cells_keys = cells.keys()
    parse_accepted = False
    for tuple in cells_keys:
        cell_0 = tuple[0]
        cell_1 = tuple[1]
        cell_nonterminal = tuple[2]
        if cell_0 == 0 and cell_1 == N-1 and cell_nonterminal == 'S':
            parse_accepted = True
            break
    if parse_accepted == True:
        parse = []
        start_key = (0, N, 'S') 
        i = 0
        start_value = backpointers[start_key]
        left_key = start_value[0]
        right_key = start_value[1]
        
    
        def print_parse2(root):
            #result = [cells[root]]
            #print 'root', root
            dataindex = cells.keys()[cells.values().index(cells[root])]
            #print 'main dataindex', dataindex
            #result = [dataindex[2], cells[dataindex]]
            result = [root[2], cells[root]]
            
            if root not in backpointers.keys():
                #print 'yayyyyyyyyyy'
                dataindex = cells.keys()[cells.values().index(cells[root])]
                #print 'dataindex', dataindex
                #print [dataindex[2], cells_word[dataindex], cells[dataindex]]                
                #return [dataindex[2], cells_word[dataindex], cells[dataindex]]                
                return [root[2], cells_word[root], cells[root]]                
            else:
                res_2 = []
                for x in backpointers[root]:
                    y = print_parse2(x)
                    res_2.append(y)
                        
                result.append(res_2)
                return result
           
           
        return print_parse2(start_key) 
    else:
        return "REJECT"   
    #return None

