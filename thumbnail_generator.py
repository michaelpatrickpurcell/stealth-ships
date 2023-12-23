import tikz
import numpy as np
import subprocess
import random
import os
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from itertools import product

from pylatex import Document, TikZ
from pylatex import Package, Command
from pylatex.utils import italic, bold, NoEscape
from pylatex.basic import NewLine

from PIL import Image

tetra_pixels = [
    np.array([[0,0],[1,1]]),
    np.array([[0,1],[0,1]]),
    np.array([[0,1],[1,0]]),
    np.array([[1,0],[0,1]]),
    np.array([[1,0],[1,0]]),
    np.array([[1,1],[0,0]]),
]


glyphs = (
    np.array([
        [1,1,1,1,1, 0, 1,1,1,1,1, 0, 1,0,0,0,1, 0, 1,1,1,1,1, 0, 1,1,1,1,1, 0, 1,1,1,1,1], 
        [1,0,0,0,0, 0, 1,0,0,0,1, 0, 0,1,0,1,0, 0, 1,0,0,0,1, 0, 0,0,1,0,0, 0, 1,0,0,0,1], 
        [1,0,0,0,0, 0, 1,1,1,1,1, 0, 0,0,1,0,0, 0, 1,1,1,1,1, 0, 0,0,1,0,0, 0, 1,0,0,0,1], 
        [1,0,0,0,0, 0, 1,0,0,1,0, 0, 0,0,1,0,0, 0, 1,0,0,0,0, 0, 0,0,1,0,0, 0, 1,0,0,0,1], 
        [1,1,1,1,1, 0, 1,0,0,0,1, 0, 0,0,1,0,0, 0, 1,0,0,0,0, 0, 0,0,1,0,0, 0, 1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0, 1,1,1,1,1, 0, 1,0,0,0, 1,0,0,0,1, 0, 1,1,1,1,1, 0, 1,0,0,0,1, 0,0,0,0],
        [0,0,0,0, 1,0,0,0,0, 0, 1,0,0,0, 0,1,0,1,0, 0, 1,0,0,0,1, 0, 1,0,0,0,1, 0,0,0,0],
        [0,0,0,0, 1,0,1,1,1, 0, 1,0,0,0, 0,0,1,0,0, 0, 1,1,1,1,1, 0, 1,1,1,1,1, 0,0,0,0],
        [0,0,0,0, 1,0,0,0,1, 0, 1,0,0,0, 0,0,1,0,0, 0, 1,0,0,0,0, 0, 1,0,0,0,1, 0,0,0,0],
        [0,0,0,0, 1,1,1,1,1, 0, 1,1,1,1, 0,0,1,0,0, 0, 1,0,0,0,0, 0, 1,0,0,0,1, 0,0,0,0],
    ]),
)

letters='ABCDEFGHIJ'

def generate_pixel_grid(pixel_values, n_rows, n_cols):

    #n_rows = n_cols and both values are even.
    locations = [[0.198 * (np.array([i,j]) - np.array(((n_rows-1)/2, (n_cols-1)/2))) for j in range(n_cols)] for i in range(n_rows-1,-1,-1)] 
    # print(locations)
    # print(len(locations))
    # print(len(locations[0]))
    pic = tikz.Picture()
    # pic.usetikzlibrary('shapes.geometric')

    for i in range(n_rows):
        for j in range(n_cols):
            location = locations[i][j]
            point = '(%fin, %fin)' % (location[1], location[0])
            if pixel_values[i,j] == 0:
                pic.node(r'\phantom{.}', at=point, minimum_width='0.198in', minimum_height='0.198in')
                                                                       
            else:
                fill_color='black'
                pic.node(r'\phantom{.}', at=point, minimum_width='0.198in', minimum_height='0.198in', fill=fill_color)

    # meta_locations = [0.396 * np.array([i,j]) for i in range(-2,3) for j in range(-2,3)]
    # for location in sum(locations,[]):
    #     point = '(%fin, %fin)' % (location[0], location[1])
    #     pic.node(r'\phantom{.}', at=point, minimum_width='0.198in', minimum_height='0.198in', draw='black', thin=True)

    # for location in meta_locations:
    #     point = '(%fin, %fin)' % (location[0], location[1])
    #     pic.node(r'\phantom{.}', at=point, minimum_width='0.396in', minimum_height='0.396in', draw='black', very_thick=True)

    tikzpicture = pic.code()
    return tikzpicture
    # return pic

def generate_latex_doc(tikzpicture, scale, seqno, seed):
    geometry_options = {'top': '1.25cm', 'bottom': '1.0cm', 'left': '7cm', 'right':'7cm', 'marginparwidth': '6.0cm', 'marginparsep': '0pt'}
    doc = Document(documentclass = 'scrartcl',
                document_options = ["paper=a4","parskip=half", "landscape"],
                fontenc=None,
                inputenc=None,
                lmodern=False,
                textcomp=False,
                page_numbers=False,
                geometry_options=geometry_options)

    doc.packages.append(Package('tikz'))
    doc.packages.append(Package('fontspec'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('booktabs'))
    doc.packages.append(Package('marginnote'))
    doc.packages.append(Package('stealthships'))

    doc.preamble.append(Command('setkomafont', NoEscape(r'section}{\setmainfont{Century Gothic}\LARGE\bfseries')))
    doc.preamble.append(Command('RedeclareSectionCommand', 'section', ([r'runin=false', NoEscape(r'afterskip=0.0\baselineskip'), NoEscape(r'beforeskip=1.0\baselineskip')])))
    doc.change_length("\columnsep", "10mm")

    doc.append(NoEscape(r'\begin{center}\setmainfont[Scale=2.5]{Century Gothic}\Huge \textbf{Cryptoglyph}\end{center}'))
    doc.append(Command(NoEscape(r'setmainfont[Scale=0.75]{Century Gothic}')))
    doc.append(Command(NoEscape(r'raggedright')))

    doc.append(Command(r'vspace{0.0cm}'))
    doc.append(Command(r'vspace{-0.5cm}'))

    doc.append(Command(NoEscape(r'begin{center}')))
    doc.append(NoEscape(r'\scalebox{%f}{' % scale))
    doc.append(NoEscape(tikzpicture))
    doc.append(NoEscape(r'}'))
    doc.append(Command(NoEscape(r'end{center}')))

    doc.append(Command(NoEscape(r'setmainfont{TeX Gyre Schola}')))
    doc.append(Command(NoEscape(r'raggedright')))

    f = open('rules_text.tex')
    rules_text = f.read()
    f.close()
    doc.append(NoEscape(rules_text))

    doc.append(Command(NoEscape(r'vfill')))
    doc.append(Command(NoEscape(r'begin{center}')))
    doc.append(NoEscape(r'{\LARGE Designed by Michael Purcell}'))
    doc.append(NoEscape(r'\normalmarginpar\marginnote{\raggedright\textbf{Random Seed}: %i\\\textbf{Sequence Number}: %i / 6}[-\baselineskip]' % (seed, seqno)))
    doc.append(NoEscape(r'\reversemarginpar\marginnote{\raggedright\textbf{Contact}: ttkttkt@gmail.com}'))
    doc.append(Command(NoEscape(r'end{center}')))

    return doc


def save_tikzpicture(bit_array, filename):
    print('hit it, %s' % filename)
    # tikzpicture.write_image(filename, dpi=600)

    maskArr = bit_array.astype(np.uint8) * 255
    maskImg =  Image.fromarray(maskArr, mode='L')
    maskImg.save(filename)

    # f = open(filename, 'w')
    # f.write(r'\documentclass{standalone}')
    # f.write(r'\usepackage{tikz}')
    # f.write(r'\begin{document}')
    # f.write(tikzpicture)
    # f.write(r'\end{document}')   
    # f.close()

def save_latex_doc(latex_doc, filename):
    latex_doc.generate_tex(filename)#, compiler='xelatex')


if __name__ == '__main__':
    seed = None
    # seed = 983291822
    # print(seed)
    if seed is None:
        seed = np.random.randint(2**31)
    np.random.seed(seed)

    # TODO: Get a random glyph from a list of candidates
    glyph = glyphs[0]

    exp_factor = 1
    n_rows=len(glyph)*exp_factor
    n_cols=len(glyph[0])*exp_factor
    expanded_image = np.zeros((n_rows, n_cols), dtype=int)
    for i in range(n_rows//exp_factor):
        for j in range(n_cols//exp_factor):
            if glyph[i,j] == 0:
                expanded_image[exp_factor*i:exp_factor*(i+1),exp_factor*j:exp_factor*(j+1)] = np.zeros((exp_factor,exp_factor), dtype=int)
            else:
                expanded_image[exp_factor*i:exp_factor*(i+1),exp_factor*j:exp_factor*(j+1)] = np.ones((exp_factor,exp_factor), dtype=int)


    # test_thumbnail = generate_pixel_grid(expanded_image, n_rows=n_rows, n_cols=n_cols)
    # save_tikzpicture(bit_array=expanded_image, filename='thumbnail_high_contrast.png')

    n_rows=len(expanded_image)*2
    n_cols=len(expanded_image[0])*2

    initial_tetra_pixel_indices = np.random.randint(0,6,n_rows//2 * n_cols//2)

    tetra_pixel_indices = np.arange(6)
    pixel_values_list = [np.zeros((n_rows,n_cols), dtype=int) - 1 for i in range(6)]
    for i in range(n_rows//2):
        for j in range(n_cols//2):
            np.random.shuffle(tetra_pixel_indices)
            if expanded_image[i,j] == 0:
                for k,pixel_values in enumerate(pixel_values_list):
                    pixel_values[2*i:2*i+2,2*j:2*j+2] = tetra_pixels[tetra_pixel_indices[0]]
            else:
                for k,pixel_values in enumerate(pixel_values_list):
                    pixel_values[2*i:2*i+2,2*j:2*j+2] = tetra_pixels[tetra_pixel_indices[k]]

    print(pixel_values_list[0][2:4,2:4])
    print(pixel_values_list[1][2:4,2:4])
    print(pixel_values_list[2][2:4,2:4])
    print(pixel_values_list[3][2:4,2:4])
    print(pixel_values_list[4][2:4,2:4])
    print(pixel_values_list[5][2:4,2:4])


    for i, pixel_values in enumerate(pixel_values_list[:6]):
        print(type(pixel_values))
        save_tikzpicture(bit_array=pixel_values, filename='flourish_secret_share_%i.png' %i)

