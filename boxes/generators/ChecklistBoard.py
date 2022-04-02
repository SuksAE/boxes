#!/usr/bin/env python3
# Copyright (C) 2013-2016 Florian Festi
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
import math

class ChecklistBoard(Boxes): # Change class name!
    """Creates a board where Quizcards can be inserted"""

    ui_group = "Unstable" # see ./__init__.py for names

    def __init__(self):
        Boxes.__init__(self)

        # Uncomment the settings for the edge types you use
        # use keyword args to set default values
        self.addSettingsArgs(edges.FingerJointSettings, finger=1.0,space=1.0)
        # self.addSettingsArgs(edges.StackableSettings)
        # self.addSettingsArgs(edges.HingeSettings)
        # self.addSettingsArgs(edges.LidSettings)
        # self.addSettingsArgs(edges.ClickSettings)
        # self.addSettingsArgs(edges.FlexSettings)
        self.addSettingsArgs(edges.GroovedSettings)

        # remove cli params you do not need
        # self.buildArgParser(x=100, sx="3*50", y=100, sy="3*50", h=100, hi=0)
        # Add non default cli params if needed (see argparse std lib)
        self.argparser.add_argument("--CardHight",  action="store", type=float, default=20.0, help="Hight of the cards in mm (vertical size)")
        self.argparser.add_argument("--CardWidth",  action="store", type=float, default=40.0, help="Width of the cards in mm (horizontal size)")
        self.argparser.add_argument("--CardNum",  action="store", type=int, default=5, help="Number of cards")
        self.argparser.add_argument("--Checkmark",  action="store", type=boolarg, default=True, help="Add checkmark box to the left of each card slot")
        self.argparser.add_argument("--AnswerCard",  action="store", type=boolarg, default=False, help="Add card slot for answer card to the left of each card slot")
        self.argparser.add_argument("--AnswerHeight",  action="store", type=float, default=20.0, help="Height of the answer cards in mm (vertical size)")
        self.argparser.add_argument("--AnswerWidth",  action="store", type=float, default=20.0, help="Width of the answer cards in mm (horizontal size)")
        self.argparser.add_argument("--Clamping",  action="store", type=float, default=0.5, help="Height of the clamping bump in mm")
        self.argparser.add_argument("--CornerRadius",  action="store", type=float, default=2, help="Corner radius in mm")
        self.argparser.add_argument("--AlignmentPins",  action="store", type=float, default=2, help="Diameter of the alignment pins in mm")
        self.argparser.add_argument("--GrooveAngle",  action="store", type=float, default=120, help="Angle of the groove arc cuts")

    def DebugTurtle(self):
        self.hole(0,0,0.5)
        self.moveTo(0,0,-90)
        self.edge(1.5)
        self.moveTo(0,0,120)
        self.edge(3)
        self.moveTo(0,0,150)
        self.edge(1)
        self.moveTo(0,0,180)
        self.edge(1)
        self.moveTo(0,0,150)
        self.edge(3)
        self.moveTo(0,0,120)
        self.edge(1.5)
        self.moveTo(0,0,90)

    def clamping_arc(self, width, height=0.5, inv=-1.0):
        angle = math.degrees(math.asin(4*height/width))
        side_length = width / math.sin(math.radians(angle)) / 2
        self.corner(inv * -angle)
        self.corner(inv * angle, side_length)
        self.corner(inv * angle, side_length)
        self.corner(inv * -angle)

    def roundWall(self, x, y, r, edges="eeee", callback=None,
                     holesRadius=None):
        """Wall with rounded corner

        For the callbacks the sides are counted depending on wallpieces

        :param x: width
        :param y: height
        :param r: radius of the corners
        :param edges:  (Default value = "eeee") bottom, right, top, left
        :param callback:  (Default value = None)
        :param holesRadius:  (Default value = None) set to get alignment holes

        """
        
        t = self.thickness
        if len(edges) != 4:
            raise ValueError("four edges required")
        edges = [self.edges.get(e, e) for e in edges]
        edges += edges  # append for wrapping around
        overallwidth = x + edges[-1].spacing() + edges[1].spacing()
        overallheight = y + edges[0].spacing() + edges[2].spacing()
        
        lx = x - 2*r
        ly = y - 2*r

#        self.moveTo(edges[3].spacing(), edges[3].margin())
        self.moveTo(r, 0)
        
        for nr, l in enumerate((lx, ly, lx, ly)):
            self.cc(callback, nr, y=edges[nr].startwidth() + self.burn)
            self.step(edges[nr].endwidth())
            edges[nr](l)
            self.step(-edges[nr].startwidth())
            self.corner(90, r)

#        self.ctx.restore()
#        self.ctx.save()

        
#        self.moveTo(-edges[0].spacing(), -edges[0].margin())
        self.moveTo(-r, 0)
        

        if holesRadius is not None:
            if (r - holesRadius) < holesRadius/2:
                r += holesRadius *1.5
            self.moveTo(r , r )
            self.hole(0, 0, r=holesRadius)
#            self.hole(x - 2 * r, 0, r=holesRadius)
            self.hole(0, y - 2 * r, r=holesRadius)
            self.hole(x - 2 * r, y - 2 * r, r=holesRadius)
            self.moveTo(-r , -r )
        
    def render(self):
        # adjust to the variables you want in the local scope
#        x, y, h = self.x, self.y, self.h
        t = self.thickness

        totalwidth = self.CardWidth + t + t + self.AnswerWidth;
        extraLength = max(self.CornerRadius, self.thickness + self.AlignmentPins) # length of the header and footer
        cardLength = (self.CardHight + t) * self.CardNum - t # length of the card section
        totalheight = extraLength + cardLength + extraLength
 
        # Create new Edges here if needed E.g.:
        s = edges.GroovedSettings(
        self.thickness, 
        style=edges.GroovedSettings.PARAM_ARC, 
        arc_angle=self.GrooveAngle, 
        width = self.CardHight / cardLength,
        gap = t / cardLength,
        margin = 0)
        
        p = edges.GroovedEdgeBase(self, s)
# used edge chars:
# C, c, D, d, E, e, F, f, g, h, I, i, j, J, K, k, L, l, M, m, N, n, O, o, P, p, Q, q, R, S, s, š, T, t, U, u, V, v, X, Z, z
        p.char = "a"
        self.addPart(p)




        # render your parts here

        self.move(x=totalwidth, y=totalheight, where ="up", before=True, label="Front")
        self.roundWall(totalwidth, totalheight, 0, edges='eaea', holesRadius=self.AlignmentPins/2)
        self.DebugTurtle()
        self.move(x=totalwidth, y=totalheight, where ="up", before=False, label="Front")
  
 
        self.move(x=totalwidth, y=totalheight, where ="up", before=True, label="Back")
        self.roundWall(totalwidth, totalheight, self.CornerRadius, edges='eeee', holesRadius=self.AlignmentPins/2)
        self.move(x=totalwidth, y=totalheight, where ="up", before=False, label="Back")
        
#        self.clamping_arc(100,self.Clamping)
#        self.roundedPlate(totalwidth, totalheight, self.Corners, edge='e', extend_corners=False)
        
        #self.trapezoidWall(100, 100, 100, ["z", "z", "z", "z"], move="right")

