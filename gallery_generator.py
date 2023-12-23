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

tetra_pixels = [
    np.array([[0,0],[0,0]]),
    np.array([[1,1],[1,1]]),
]

glyphs = [
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ]),#A
    np.array([
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
    ]),#B
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ]),#C
    np.array([
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
    ]),#D
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ]),#E
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
    ]),#F
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,1,1,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
    ]),#G
    np.array([
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ]),#H
    np.array([
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [1,1,1,1,1],
    ]),#I
    np.array([
        [1,1,1,1,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [1,0,1,0,0],
        [1,1,1,0,0],
    ]),#J
    np.array([
        [1,0,0,1,0],
        [1,0,1,0,0],
        [1,1,0,0,0],
        [1,0,1,0,0],
        [1,0,0,1,0],
    ]),#K 
    np.array([
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
    ]),#L
    np.array([
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ]),#M    
    np.array([
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,1],
        [1,0,0,1,1],
        [1,0,0,0,1],
    ]),#N
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
    ]),#O 
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
    ]),#P
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,1,1],
        [1,1,1,1,1],
    ]),#Q
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,1,0],
        [1,0,0,0,1],
    ]),#R
    np.array([
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,1],
        [0,0,0,0,1],
        [1,1,1,1,1],
    ]),#S
    np.array([
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
    ]),#T
    np.array([
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
    ]),#U
    np.array([
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,0,1,0],
        [0,1,0,1,0],
        [0,0,1,0,0],
    ]),#V
    np.array([
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,1,0,1,1],
    ]),#W
    np.array([
        [1,0,0,0,1],
        [0,1,0,1,0],
        [0,0,1,0,0],
        [0,1,0,1,0],
        [1,0,0,0,1],
    ]),#X
    np.array([
        [1,0,0,0,1],
        [0,1,0,1,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
    ]),#Y
    np.array([
        [1,1,1,1,1],
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,1,0,0,0],
        [1,1,1,1,1],
    ]),#Z
    np.array([
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ]),#0
    np.array([
        [0,1,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
    ]),#1
    np.array([
        [0,1,1,0,0],
        [1,0,0,1,0],
        [0,0,1,0,0],
        [0,1,0,0,0],
        [1,1,1,1,0],
    ]),#2
    np.array([
        [1,1,1,1,0],
        [0,0,0,1,0],
        [0,1,1,1,0],
        [0,0,0,1,0],
        [1,1,1,1,0],
    ]),#3
    np.array([
        [1,0,0,1,0],
        [1,0,0,1,0],
        [1,1,1,1,0],
        [0,0,0,1,0],
        [0,0,0,1,0],
    ]),#4
        np.array([
        [0,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [0,0,0,1,0],
        [1,1,1,1,0],
    ]),#5
    np.array([
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,1,0],
        [1,1,1,1,0],
    ]),#6
    np.array([
        [1,1,1,1,0],
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,1,0,0,0],
        [1,0,0,0,0],
    ]),#7
    np.array([
        [1,1,1,1,0],
        [1,0,0,1,0],
        [0,1,1,0,0],
        [1,0,0,1,0],
        [1,1,1,1,0],
    ]),#8
    np.array([
        [1,1,1,1,0],
        [1,0,0,1,0],
        [1,1,1,1,0],
        [0,0,0,1,0],
        [1,1,1,1,0],
    ]),#9
]

letters='ABCDEFGHIJ'

def generate_pixel_grid(pixel_values, n_rows, n_cols):

    #n_rows = n_cols and both values are even.
    locations = [[0.198 * (np.array([i,j]) - np.array(((n_cols-1)/2, (n_rows-1)/2))) for i in range(n_rows)] for j in range(n_cols-1,-1,-1)]

    pic = tikz.Picture()
    # pic.usetikzlibrary('shapes.geometric')

    for i in range(n_rows):
        for j in range(n_cols):
            location = locations[i][j]
            point = '(%fin, %fin)' % (location[0], location[1])
            if pixel_values[i,j] == 0:
                fill_color='white'
            else:
                fill_color='gray'
            # pic.node(r'\textcolor{lightgray}{%s%i}' % (letters[j],i), at=point, minimum_width='0.198in', minimum_height='0.198in', fill=fill_color)
            pic.node(r'\phantom{.}', at=point, minimum_width='0.198in', minimum_height='0.198in', fill=fill_color)

    meta_locations = [0.396 * np.array([i,j]) for i in range(-2,3) for j in range(-2,3)]
    for location in sum(locations,[]):
        point = '(%fin, %fin)' % (location[0], location[1])
        pic.node(r'\phantom{.}', at=point, minimum_width='0.198in', minimum_height='0.198in', draw='black', thin=True)

    for location in meta_locations:
        point = '(%fin, %fin)' % (location[0], location[1])
        pic.node(r'\phantom{.}', at=point, minimum_width='0.396in', minimum_height='0.396in', draw='black', very_thick=True)

    # for i,loc in enumerate([0.891, 0.693, 0.495, 0.297, 0.099, -0.099, -0.297, -0.495, -0.693, -0.891]):
    #     point = '(-1.099in, %fin)' % loc
    #     pic.node(r'%s' % (i+1), at=point, minimum_width='0.198in', minimum_height='0.198in')
    #     point = '(1.099in, %fin)' % loc
    #     pic.node(r'%s' % (i+1), at=point, minimum_width='0.198in', minimum_height='0.198in')
    #     point = '(%fin, 1.099in)' % loc
    #     pic.node(r'%s' % letters[9-i], at=point, minimum_width='0.198in', minimum_height='0.198in')
    #     point = '(%fin, -1.099in)' % loc
    #     pic.node(r'%s' % letters[9-i], at=point, minimum_width='0.198in', minimum_height='0.198in')

    pic.node(r'\phantom{.}', at='(0,0)', minimum_width='1.99in', minimum_height='1.99in', draw='black', line_width='0.25mm')
    # tikzpicture = pic.code()
    return pic#tikzpicture

def generate_gallery_grid():
    locations = product(1.6*np.arange(0,-4,-1), 1.2*np.arange(9))
    
    pic = tikz.Picture()
    
    for i,location in enumerate(locations):
        point = '(%fin,%fin)' % (location[1], location[0])
        pic.node(r'\includegraphics[scale=0.075]{Images/glyph_image_%i}' % i, at=point)

    gallery_grid = pic.code()
    return gallery_grid    
            


def generate_latex_doc(gallery_grid):
    geometry_options = {'top': '1.25cm', 'bottom': '1.0cm', 'left': '1cm', 'right':'1cm', 'marginparwidth': '6.0cm', 'marginparsep': '0pt'}
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

    doc.append(NoEscape(r'\begin{center}\setmainfont[Scale=2.5]{Century Gothic}\Huge \textbf{Cryptoglyph Gallery}\end{center}'))

    doc.append(Command(NoEscape(r'setmainfont[Scale=0.75]{Century Gothic}')))
    doc.append(Command(NoEscape(r'raggedright')))

    doc.append(Command(r'vfill'))

    doc.append(Command(NoEscape(r'begin{center}')))
    doc.append(NoEscape(r'\scalebox{1.0}{'))
    doc.append(NoEscape(gallery_grid))
    doc.append(NoEscape(r'}'))
    doc.append(Command(NoEscape(r'end{center}')))

    doc.append(Command(r'vfill'))
    # doc.append(NoEscape(r'{\tiny\phantom{a}}'))

    return doc


def save_tikzpicture(tikzpicture, filename):
    tikzpicture.write_image(filename, dpi=600)

def save_latex_doc(latex_doc, filename):
    latex_doc.generate_tex(filename)#, compiler='xelatex')


if __name__ == '__main__':
    # TODO: Get a random glyph from a list of candidates
    n_rows=len(glyphs[0])*2
    n_cols=len(glyphs[0][0])*2

    # pixel_values_list = [np.zeros((n_rows,n_cols), dtype=int) - 1 for i in range(len(glyphs))]
    # for glyph, pixel_values in zip(glyphs, pixel_values_list):
    #     for i in range(n_rows//2):
    #         for j in range(n_cols//2):
    #             if glyph[i,j] == 0:
    #                 pixel_values[2*i:2*i+2,2*j:2*j+2] = tetra_pixels[0]
    #             else:
    #                 pixel_values[2*i:2*i+2,2*j:2*j+2] = tetra_pixels[1]

    # tikzpictures = []
    # for i,pixel_values in enumerate(pixel_values_list):
    #     glyph_image = generate_pixel_grid(pixel_values, n_rows=n_rows, n_cols=n_cols)
    #     tikzpictures.append(glyph_image)
    #     save_tikzpicture(tikzpicture=glyph_image, filename='Images/glyph_image_%i.png' %i)

    gallery_grid = generate_gallery_grid()
    latex_doc = generate_latex_doc(gallery_grid)

    save_latex_doc(latex_doc, 'PnPFiles/cryptoglyph_gallery')


    subprocess.call(["xelatex", "PnPFiles/cryptoglyph_gallery.tex", "--output-directory=PnPFiles"])
    subprocess.call(["xelatex", "PnPFiles/cryptoglyph_gallery.tex", "--output-directory=PnPFiles"])
    os.remove("PnPFiles/cryptoglyph_gallery.tex")
    os.remove("PnPFiles/cryptoglyph_gallery.aux")
    os.remove("PnPFiles/cryptoglyph_gallery.log")
