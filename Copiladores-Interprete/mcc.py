#mcc.py
'''
usage: mcc.py [-h] [-d] [-o OUT] [-l] [-D] [-p] [-I] [--sym] [-S] [-R] input

Compiler for MiniC programs

positional arguments:
  input              MiniC program file to compile

optional arguments:
  -h, --help         show this help message and exit
  -d, --debug        Generate assembly with extra information (for debugging purposes)
  -o OUT, --out OUT  File name to store generated executable
  -l, --lex          Store output of lexer
  -D, --dot          Generate AST graph as DOT format
  -p, --png          Generate AST graph as png format
  -I, --ir           Dump the generated Intermediate representation
  --sym              Dump the symbol table
  -S, --asm          Store the generated assembly file
  -R, --exec         Execute the generated program
'''
from contextlib import redirect_stdout
from rich import print
from mclex import print_lexer
from mcparser import gen_ast
from mcontext import Context
import argparse
import subprocess
import os
import sys

def parse_args():
    cli = argparse.ArgumentParser(
        prog='mcc.py',
        description='Compiler for MiniC++ programs'
    )

    cli.add_argument(
        '-v', '--version',
        action='version',
        version='0.1'
    )

    fgroup = cli.add_argument_group('Formatting options')
    output_group = cli.add_argument_group('Output options')

    fgroup.add_argument(
        'input',
        type=str,
        nargs='?',
        help='MiniC++ program file to compile'
    )

    output_group.add_argument(
        '-l', '--lex',
        action='store_true',
        default=False,
        help='Store output of lexer'
    )

    output_group.add_argument(
        '-d', '--dot',
        action='store_true',
        default=False,
        help='Generate AST graph as DOT format'
    )

    output_group.add_argument(
        '-p', '--png',
        action='store_true',
        help='Generate AST graph as png format'
    )

    output_group.add_argument(
        '--sym',
        action='store_true',
        help='Dump the symbol table'
    )

    return cli.parse_args()

if __name__ == '__main__':
    args = parse_args()
    context = Context()

    if args.input:
        fname = args.input

        # Permitir archivos .c, .cpp y .mcc
        if not (fname.endswith('.c') or fname.endswith('.cpp') or fname.endswith('.mcc')):
            print(f'[bold red]Error:[/bold red] Invalid input file: {fname}')
            exit(1)

        try:
            with open(fname, encoding='utf-8') as file:
                source = file.read()
            print(f'[bold green]Successfully loaded file:[/bold green] {fname}')

            if args.lex:
                flex = fname.split('.')[0] + '.lex'
                print(f'Generating lexer output: {flex}')
                with open(flex, 'w', encoding='utf-8') as f:
                    with redirect_stdout(f):
                        print_lexer(source)

            elif args.dot or args.png:
                ast, dot = gen_ast(source)
                base = fname.split('.')[0]

                if args.dot:
                    fdot = base + '.dot'
                    print(f'Generating AST: {fdot}')
                    with open(fdot, 'w') as f:
                        with redirect_stdout(f):
                            print(dot)

                if args.png:
                    fdot = base + '.dot'
                    png_file = base + '.png'
                    print(f'Generating PNG: {png_file}')
                    try:
                        subprocess.run(['dot', '-Tpng', fdot, '-o', png_file], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f'[bold red]Error:[/bold red] Failed to generate PNG: {str(e)}')

            else:
                context.parse(source)
                context.run()

        except FileNotFoundError:
            print(f'[bold red]Error:[/bold red] File not found: {fname}')
        except Exception as e:
            print(f'[bold red]Error:[/bold red] {str(e)}')

    else:
        while True:
            try:
                source = input('minic $ ')
                if source.strip().lower() in {'exit', 'quit'}:
                    break
                # Tokeniza e imprime los tokens ingresados en la consola
                print_lexer(source)
            except EOFError:
                break
            except Exception as e:
                print(f'[bold red]Error:[/bold red] {str(e)}')
