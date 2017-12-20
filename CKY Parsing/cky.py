from pprint import pprint
from collections import defaultdict

# The productions rules have to be binarized.

grammar_text = """
S -> NP VP
S -> NPS VPS
NP -> Det Noun
NPS -> Det NounS
VP -> Verb NP
VPS -> VerbS NP
PP -> Prep NP
NP -> NP PP
VP -> VP PP
"""
"""
grammar_text = 
S -> NP VP
NP -> Det Noun
VP -> Verb NP
PP -> Prep NP
NP -> NP PP
VP -> VP PP
"""

lexicon = {
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'NounS': set(['dogs', 'cats']),
    'Verb': set(['attacked', 'saw', 'loved', 'hated', 'attacks']),
    'VerbS': set(['attack']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the', 'a']),
}
"""
lexicon = {
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'Verb': set(['attacked', 'saw', 'loved', 'hated']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the', 'a']),
}"""

# Process the grammar rules.  You should not have to change this.
grammar_rules = []
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    left = left.strip()
    children = right.split()
    rule = (left, tuple(children))
    grammar_rules.append(rule)
#possible_parents_for_children = {}
possible_parents_for_children = defaultdict(list)
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)
# Error checking
all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
for par, (leftchild, rightchild) in grammar_rules:
    if leftchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    if rightchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

# print "Grammar rules in tuple form:"
# pprint(grammar_rules)
# print "Rule parents indexed by children:"
# pprint(possible_parents_for_children)


def cky_acceptance(sentence):
    # return True or False depending whether the sentence is parseable by the grammar.
    global grammar_rules, lexicon

    # Set up the cells data structure.
    # It is intended that the cell indexed by (i,j)
    # refers to the span, in python notation, sentence[i:j],
    # which is start-inclusive, end-exclusive, which means it includes tokens
    # at indexes i, i+1, ... j-1.
    # So sentence[3:4] is the 3rd word, and sentence[3:6] is a 3-length phrase,
    # at indexes 3, 4, and 5.
    # Each cell would then contain a list of possible nonterminal symbols for that span.
    # If you want, feel free to use a totally different data structure.
    N = len(sentence)
    #cells = {}
    cells = defaultdict(list)
    tags = {}
    for word in sentence:
        for key, value in lexicon.iteritems():
            if word in value:
                tags[word] = key
    print 'tags',tags
    
    for i in range(0,N):
        cells[(i, i+1)] = [tags[sentence[i]]]
        for j in range(i + 1, N + 1):
            if cells[(i, j)] == 0:
                cells[(i, j)] = [' ']    
    #pprint(cells)
    
    # TODO replace the below with an implementation
    for l in range(2, N + 1):
        for m in range(0, N+1-l):    
            for k in range(m+1, m+l):                               
                if cells[m,k] == []:
                    cells[m,k] = [' ']
                if cells[k, m+l] == []:
                    cells[k, m+l] = [' ']
                len_left = len(cells[m,k])
                len_right = len(cells[k, m+l])
                if len_left == 1 and len_right == 1:
                    cells[(m, m+l)] = list(set(cells[(m, m+l)]).union( set(possible_parents_for_children[cells[m,k][0], cells[k, m+l][0]]) ))
                else:
                    for p in range(len_left):
                        for q in range(len_right):
                            cells[(m, m+l)] = list(set(cells[(m, m+l)]).union( set(possible_parents_for_children[cells[m,k][p], cells[k, m+l][q]]) ))
    print(cells)
    if cells[0,N] == ['S']:
        return True
    else:
        return False
    #pprint(cells)
    #return False


def cky_parse(sentence):
    # Return one of the legal parses for the sentence.
    # If nothing is legal, return None.
    # This will be similar to cky_acceptance(), except with backpointers.
    global grammar_rules, lexicon

    N = len(sentence)
    cells = defaultdict(list)
    cells_word = defaultdict(list)
    tags = {}
    for word in sentence:
        for key, value in lexicon.iteritems():
            if word in value:
                tags[word] = key
    
    backpointers = defaultdict(list)
    
    for i in range(N):        
        cells[(i, i+1)] = [tags[sentence[i]]]
        cells_word[(i, i+1)] = [tags[sentence[i]], sentence[i]]
        for j in range(i + 1, N + 1):
            if cells[(i, j)] == 0:
                cells[(i, j)] = [' '] 
    # TODO replace the below with an implementation
    for l in range(2, N + 1):
        for m in range(0, N+1-l):    
            for k in range(m+1, m+l):  
                flag = False
                if cells[m,k] == []:
                    cells[m,k] = [' ']
                if cells[k, m+l] == []:
                    cells[k, m+l] = [' ']
                len_left = len(cells[m,k])
                len_right = len(cells[k, m+l])
                current_parent = possible_parents_for_children[cells[m,k][0], cells[k, m+l][0]]
                #print 'current_parent',current_parent
                if current_parent != []:
                    flag = True
                if len_left == 1 and len_right == 1:
                    cells[(m, m+l)] = list(set(cells[(m, m+l)]).union( set(possible_parents_for_children[cells[m,k][0], cells[k, m+l][0]]) ))
                else:
                    for p in range(len_left):
                        for q in range(len_right):
                            
                            cells[(m, m+l)] = list(set(cells[(m, m+l)]).union( set(possible_parents_for_children[cells[m,k][p], cells[k, m+l][q]]) ))
    
    
                if flag == True:
                    backpointers[(m, m+l)] = [(m,k),(k,m+l)]
                
    if cells[0,N] != ['S']:
        return None
    else:
        parse = []
        start_key = (0, N) 
        i = 0
        start_value = backpointers[start_key]
        left_key = start_value[0]
        right_key = start_value[1]
        
        
    def print_parse2(root):
            result = [cells[root][0]]
            if root not in backpointers.keys():
                #return [cells[root][0],'the']
                return cells_word[root]
            else:
                res_2 = []
                for x in backpointers[root]:
                    y = print_parse2(x)
                    res_2.append(y)
                        
                result.append(res_2)
                return result
           
            
    return print_parse2(start_key)       
    

## some examples of calling these things...
## you probably want to call only one sentence at a time to help debug more easily.

# print cky_acceptance(['the','cat','attacked','the','food'])
# pprint( cky_parse(['the','cat','attacked','the','food']))
# pprint( cky_acceptance(['the','the']))
# pprint( cky_parse(['the','the']))
# print cky_acceptance(['the','cat','attacked','the','food','with','a','dog'])
# pprint( cky_parse(['the','cat','attacked','the','food','with','a','dog']) )
# pprint( cky_parse(['the','cat','with','a','table','attacked','the','food']) )
#
