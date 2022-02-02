'''
This is just a script for remove characters that is not English alphabet and replace with it ascii.
@author: Baby
@last modify: Nov 3,2021
'''
import argparse
import os.path
import json
import ndjson
import unicodedata


parser = argparse.ArgumentParser()

weird_char = {
            "’" : "'",
            "“" : '"',
            "”" : '"',
            }

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        return parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r',encoding='utf-8')


def normalize(input_file, output_file):
    '''
    Decode each charater to ascii. then normalize characters that is not English alphabet
    with replace character or remove it.
    '''
    out_file = open(output_file, "x")
    file = input_file
    for line in file:
        for character in line:
            
            try:
                character.encode(encoding='utf-8').decode('ascii') 
            except UnicodeDecodeError:
                #convert character to English alphabet.
                c = unicodedata.normalize('NFD', character).encode('ascii', 'ignore').decode("utf-8") 
                if not c.isalpha():
                    if character in weird_char:
                        c = weird_char[character] #replace the weied char with normal char.
                    else:
                        c = ''
                    
                print(f'NOT ENGLISH! = {character} was replaced with {c} ')
                out_file.write(c)
            else:
                character = remove_control_characters(character)
                out_file.write(character)
    
    out_file.close()


def remove_control_characters(s):
    '''
    control characters(eg. '\\t','\\r','\\0', etc.)
    '''
    if s == '\n':
        return '\n'

    if unicodedata.category(s)[0] != 'C':
        return s
    return ''


if __name__ == '__main__':
    
    parser.add_argument('-i','--i', help="place the input file",required=True, metavar="FILE",dest="input_file",type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o','--o', help="place the output file", required=True, metavar="FILE",dest="output_file")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    normalize(input_file, output_file)  
    