import re
import sys
import commands

mutant_desc = sys.argv[1]
source_code = sys.argv[2]
dest = sys.argv[3]


source_lines = open(source_code).readlines()
mutants = open(mutant_desc).readlines()
line_mutants = {}


def make_copy(src_list, ith, replace_str):
    newlist  = []
    for i, elem in enumerate(src_list):
        if i != ith:
            newlist.append(elem)
        else:
            newlist.append(replace_str)

    return newlist


for l in mutants:
    line_num_str = l.split()[0].replace(':', '')
    mutation  = re.findall('^\d+: (.*)', l)[0] + '\n'
    line_num = int(line_num_str)
    
    if line_num not in line_mutants:
        line_mutants[line_num] = []
    line_mutants[line_num].append((l,mutation))

# print line_mutants

mutant_id = 0

mfn = open('{0}-mutation-info.txt'.format(source_code), 'w')
for i, line in enumerate(source_lines):
    source_line = i + 1
    if source_line  in line_mutants:
        for mdetail, m in line_mutants[source_line]:
            print mdetail
            new_source = make_copy(source_lines, i, m)
            with open(dest, 'w') as fn:
                content = ''.join(new_source)
                fn.write(content)
                fn.flush()
                fn.close()
            status, out = commands.getstatusoutput('make clean; make build')
        
            print out
         
            if status == 0:
                mutant_id += 1
                mutation_file_name = '{0}.mut{1}'.format(source_code, mutant_id) 
                print commands.getstatusoutput(('cp grep.exe {0}').format(mutation_file_name))
                mfn.write('{0}:grep.c: {1}\n'.format(mutation_file_name, mdetail))

