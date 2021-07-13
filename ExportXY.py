#!/usr/bin/env python3
#
# curve xy co-ordinate export
# Authors:
# Jean Moreno <jean.moreno.fr@gmail.com>
# John Cliff <john.cliff@gmail.com>
# Neon22 <https://github.com/Neon22?tab=repositories>
# Jens N. Lallensack <jens.lallensack@gmail.com>
#
# Copyright (C) 2011 Jean Moreno
# Copyright (C) 2011 John Cliff 
# Copyright (C) 2011 Neon22
# Copyright (C) 2019 Jens N. Lallensack
#
# Released under GNU GPL v3, see https://www.gnu.org/licenses/gpl-3.0.en.html for details.
#
import inkex
import sys
import yaml
import copy
from inkex import paths
from inkex import transforms

height = 0.053

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class TemplateEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
    def effect(self):
        idx=0
        output_all = {}
        for id, node in self.selected.items():
            output_nodes = []
            if node.tag == inkex.addNS('path','svg'):
                #output_all += ""
                #output_nodes += ""
                node.apply_transform()
                d = node.get('d')
                p = paths.CubicSuperPath(d)
                for subpath in p:
                    for csp in subpath:
                        new_pt={}
                        new_pt['position'] = [-csp[1][0]/1000.0, csp[1][1]/1000.0, height]
                        new_pt['orientation'] = [0,90,0]
                        output_nodes.append(new_pt)

                z_in = copy.deepcopy(output_nodes[0])
                z_in['position'][2] = height+0.02
                z_out = copy.deepcopy(output_nodes[-1])
                z_out['position'][2] = height+0.02
                output_nodes.insert(0,z_in)
                output_nodes.append(z_out)
                output_all['path'+str(idx)]  = output_nodes
                idx+=1
        

        with open('inkscape_path_out.yaml', 'w+') as f:
            yaml.dump(output_all, f, default_flow_style=None)
                #f.write(new_pt)

            sys.stderr.write(str(output_nodes))
TemplateEffect().run()
sys.exit(0) #helps to keep the selection
