#!/usr/bin/python3
# Copyright (C) 2013-2018 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class ZeroClearanceLid(Boxes):
    """Either a lid for boxes sitting next to each other or a storage box for sheet like objects. 
    """

    description = """
    This lid can be opened from the top even if there is no space around the boxes.
    Also usable as storage box with an openeing from the side and on the bottom e.g. for cards.

    Set 'play' to 0 if not used as lid, otherwise the box size will be increased by 2x the material 
    thickness to compensate for the box (assuming the box is made from the same material than the lid).

"""

    ui_group = "Box"

    def cb_cutout(self, nr, length, edgetype):
        cutnum = self.cutNumbers[nr%4]
        cutlen = self.CutLengths[nr%4]
        cutheight = self.CutHeights[nr%4] if nr < 4 else self.CutDepths[nr%4]
        cutradius = self.CutRadii[0] if nr < 4 else self.CutRadii[1]
        if cutnum:
            fingers, leftover, finger, space, tmp = self.edges['f'].FingerAndSpacers(length,0,0)
            cutOut = self.edges['f'].calcCutout(fingers,cutnum,cutlen)

            if self.debug:
                print (length, fingers, leftover, finger, space, cutOut)
                with self.saved_context():
                    self.hole(leftover/2, 1-self.burn, 0.25, color=[ 0.0, 1.0, 0.0 ])
                    self.hole(leftover/2, 0, 0.5, color=[ 1.0, 0.0, 0.0 ])
                    self.hole(leftover/2 + finger, 0, 0.5, color=[ 1.0, 0.0, 0.0 ])
                    self.text("1",leftover/2 + finger/2, -3, fontsize=2, color=[ 1.0, 0.0, 0.0 ])
                    for i in range(fingers-1):
                        self.hole(leftover/2 + (i+2)*finger + (i+1) * (space), 0, 0.5, color=[ 1.0, 0.0, 0.0 ])
                        self.text(str(i+2), leftover/2 - finger/2 + (i+2) * finger + (i+1) * (space), -3, fontsize=2, color=[ 1.0, 0.0, 0.0 ])
                    for i in range(2*fingers):
                        self.hole(leftover/2 + math.ceil(i/2) * finger + math.trunc(i/2) * space , 1-self.burn, 0.25, color=[ 0.0, 1.0, 0.0 ])
                        self.text(str(i+1), leftover/2 + math.ceil(i/2) * finger + math.trunc(i/2) * space - 1 , 2, fontsize=2, color=[ 1.0, 0.0, 0.0 ])

            for i in range(len(cutOut)):
                s, l = cutOut[i]
                if edgetype in ['f', 'F']:
                    with self.saved_context():
                        self.ctx.stroke()
                        self.set_source_color(Color.INNER_CUT)
                        self.moveTo( leftover/2 + math.trunc(s / 2) * finger + math.trunc((s - 1) / 2) * space , -self.burn, 90)
                        self.edge(cutheight+2*self.burn-cutradius)
                        self.corner(-90,cutradius)
                        self.edge((math.ceil(l/2)*finger + math.trunc(l/2)*space if s%2 else math.trunc(l/2)*finger + math.ceil(l/2)*space) - 2 * cutradius + 2*self.burn)
                        self.corner(-90,cutradius)
                        self.edge(cutheight+2*self.burn-cutradius)
                        self.ctx.stroke()
                elif edgetype in ['h']:
                    with self.saved_context():
                        self.ctx.stroke()
                        self.set_source_color(Color.INNER_CUT)
                        self.moveTo( leftover/2 + math.trunc(s / 2) * finger + math.trunc((s - 1) / 2) * space , -self.burn, 90)
                        self.edge(-1*(self.thickness+self.edges["f"].settings.edge_width))
                        self.edge((self.thickness+self.edges["f"].settings.edge_width))
                        self.edge(cutheight+2*self.burn-cutradius)
                        self.corner(-90,cutradius)
                        self.edge((math.ceil(l/2)*finger + math.trunc(l/2)*space if s%2 else math.trunc(l/2)*finger + math.ceil(l/2)*space) - 2 * cutradius + 2*self.burn)
                        self.corner(-90,cutradius)
                        self.edge(cutheight+2*self.burn-cutradius)
                        self.edge((self.thickness+self.edges["f"].settings.edge_width))
                        self.ctx.stroke()
                if self.debug:
#                    print(s,l)
                    with self.saved_context():
                        self.rectangularHole(leftover/2+finger*math.trunc(s/2) + space*math.trunc((s-1)/2), -self.burn, math.ceil(l/2)*finger + math.trunc(l/2)*space if s%2 else math.trunc(l/2)*finger + math.ceil(l/2)*space , h+2*self.burn, center_x=False, center_y=False, color=[ 1.0, 0.0, 0.0 ])


    def __init__(self) -> None:
        Boxes.__init__(self)

        self.addSettingsArgs(edges.FingerJointSettings, finger=2.0, space=2.0)
        self.frontgroup = self.argparser.add_argument_group(self.__class__.__name__ +  " Front Side Settings")
        self.rightgroup = self.argparser.add_argument_group(self.__class__.__name__ +  " Right Side Settings")
        self.backgroup = self.argparser.add_argument_group(self.__class__.__name__ +  " Back Side Settings")
        self.leftgroup = self.argparser.add_argument_group(self.__class__.__name__ +  " Left Side Settings")

        self.buildArgParser(x=100, y=100, h=50, outside=True)
        self.argparser.add_argument("--top_edge", action="store", type=ArgparseEdgeType("fh"), choices=list("fh"), default="f", help="edge type for top edge")
        self.argparser.add_argument("--play",  action="store", type=float, default=0.15, help="play if used as lid to the box as multiple of the wall thickness")
        self.argparser.add_argument("--CutEdges",  action="store", type=str, choices=['none', 'front', 'front + back', 'front + right', 'all sides'], default="front + back", help="edges to be cut")
        self.argparser.add_argument("--CutRadius_w",  action="store", type=int, default=5, help="wall: radius of cutouts (in mm)")
        self.argparser.add_argument("--CutRadius_t",  action="store", type=int, default=1, help="top:  radius of cutouts (in mm)")


        self.frontgroup.add_argument("--CutNumber_f",  action="store", type=int, default=1,  help="front side: number of cutouts")
        self.frontgroup.add_argument("--CutLength_f",  action="store", type=int, default=3,  help="front side: length of cutouts (in fingers)")
        self.frontgroup.add_argument("--CutHeight_f",  action="store", type=int, default=12, help="front side wall: height of cutouts (in mm)")
        self.frontgroup.add_argument("--CutDepth_f" ,  action="store", type=int, default=2,  help="front side top: depth of cutouts (in mm)")

        self.backgroup.add_argument("--CutNumber_b",  action="store", type=int, default=1,  help="back side: number of cutouts")
        self.backgroup.add_argument("--CutLength_b",  action="store", type=int, default=3,  help="back side: length of cutouts (in fingers)")
        self.backgroup.add_argument("--CutHeight_b",  action="store", type=int, default=12, help="back side wall: height of cutouts (in mm)")
        self.backgroup.add_argument("--CutDepth_b" ,  action="store", type=int, default=2,  help="back side top: depth of cutouts (in mm)")

        self.rightgroup.add_argument("--CutNumber_r",  action="store", type=int, default=1,  help="right side: number of cutouts")
        self.rightgroup.add_argument("--CutLength_r",  action="store", type=int, default=3,  help="right side: length of cutouts (in fingers)")
        self.rightgroup.add_argument("--CutHeight_r",  action="store", type=int, default=12, help="right side wall: height of cutouts (in mm)")
        self.rightgroup.add_argument("--CutDepth_r" ,  action="store", type=int, default=2,  help="right side top: depth of cutouts (in mm)")

        self.leftgroup.add_argument("--CutNumber_l",  action="store", type=int, default=1,  help="left side: number of cutouts")
        self.leftgroup.add_argument("--CutLength_l",  action="store", type=int, default=3,  help="left side: length of cutouts (in fingers)")
        self.leftgroup.add_argument("--CutHeight_l",  action="store", type=int, default=12, help="left side wall: height of cutouts (in mm)")
        self.leftgroup.add_argument("--CutDepth_l" ,  action="store", type=int, default=2,  help="left side top: depth of cutouts (in mm)")

    def render(self):
        # adjust to the variables you want in the local scope
        x, y, height = self.x, self.y, self.h
        t = self.thickness
        p = self.play * t
        
        self.CutLengths = [self.CutLength_f, self.CutLength_b, self.CutLength_r, self.CutLength_l] 
        self.CutHeights = [self.CutHeight_f, self.CutHeight_b, self.CutHeight_r, self.CutHeight_l] 
        self.CutDepths  = [self.CutDepth_f , self.CutDepth_b , self.CutDepth_r , self.CutDepth_l]
        self.CutRadii   = [self.CutRadius_w, self.CutRadius_t]

        match self.CutEdges:
            case 'none':
                self.cutNumbers = [0,0,0,0]
            case 'front':
                self.cutNumbers = [self.CutNumber_f, 0,0,0] 
            case 'front + back':
                self.cutNumbers = [self.CutNumber_f, self.CutNumber_b, 0, 0] 
            case 'front + right':
                self.cutNumbers = [self.CutNumber_f, 0, self.CutNumber_r, 0] 
            case 'all sides':
                self.cutNumbers = [self.CutNumber_f, self.CutNumber_b, self.CutNumber_r, self.CutNumber_l] 
            case  _:
                self.cutNumbers = [0,0,0,0]

        if self.outside:
            x -= 2*t + 2*p
            y -= 2*t + 2*p
            height -= (self.thickness + self.edges["f"].settings.edge_width) if self.top_edge == 'h' else (t)

        for i in range(len(self.CutHeights)):
            if self.CutHeights[i] >= height:
                self.CutHeights[i] = height

        # Adjust h edge with play
        self.edges["f"].settings.setValues(t, False, edge_width=self.edges["f"].settings.edge_width + p)

        if p > 0 :
            d = 2 * (t+p)
        else:
            d = 0
        with self.saved_context():
            self.rectangularWall(x+d, height, self.top_edge + "FeF", move="right", label="front", callback=[lambda: self.cb_cutout(0, x+d, self.top_edge), 0, 0, 0])
            self.rectangularWall(y+d, height, self.top_edge + "fef", move="right", label="right", callback=[lambda: self.cb_cutout(2, y+d, self.top_edge), 0, 0, 0])
            self.rectangularWall(x+d, height, self.top_edge + "FeF", move="right", label="back",  callback=[lambda: self.cb_cutout(1, x+d, self.top_edge), 0, 0, 0])
            self.rectangularWall(y+d, height, self.top_edge + "fef", move="right", label="left",  callback=[lambda: self.cb_cutout(3, y+d, self.top_edge), 0, 0, 0])
        self.rectangularWall(y, height, self.top_edge + "fef", move="up only")

        self.rectangularWall(x+d, y+d, "FFFF" if self.top_edge == "f" else "ffff", bedBolts=None, move="right", label="top", callback=[lambda: self.cb_cutout(4, x+d, "F"), lambda: self.cb_cutout(6, y+d, "F"),lambda: self.cb_cutout(5, x+d, "F"),lambda: self.cb_cutout(7, y+d, "F")])
        
