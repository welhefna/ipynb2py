""".IPYNB to .PY

Simple python script to convert jupyter notebook, .ipynb
to python script file. .py

Note:
	None.
	
Example:

	python -m ipynb2py

#TODO :
	*update based on research requirement.
	
"""

import argparse
import os
import subprocess


def convert(input_path, output_path):
    subprocess.call(['jupyter', 'nbconvert', '--to', 'script',input_path, '--output', output_path])


def cleanup(path):

    skip_lines_startwith = ('Image(filename=',
                            '# In[',
                            '# <hr>',
                            'from IPython.display import Image',
                            'get_ipython()',
                            '# <br>'
                            )

    code_expressions = []
    imports = set()
    
    with open(path, 'r') as f:
        
        next(f) #skip first line
        next(f) #skip second line
        
        for line in f:
            line = line.rstrip(' ')
            if line.startswith(skip_lines_startwith):
                continue
            if line.startswith('import ') or ('from ' in line and 'import ' in line):
                if 'from __future__ import print_function' in line:
                    if line != imports[0]:
                        imports.insert(0, line)
                else:
                    if line.strip() not in imports:
                        imports.append(line)
                        imports.add(line.strip())
            else:
                code_expressions.append(line)

    clean_script = ['# coding: utf-8\n\n\n'] + imports + code_expressions

    with open(path, 'w') as f:
        for line in clean_script:
            f.write(line)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('--input', '-i', required=True, help='Jupyter notebook file path')
    parser.add_argument('--output', '-o', required=True, help='Python script file path')
    args = parser.parse_args()
    convert(input_path=args.input, output_path=os.path.splitext(args.output)[0]) #use jupyter to export the python script file.
    cleanup(args.output) #clean the exported script