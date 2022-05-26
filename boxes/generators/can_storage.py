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
#   MERself.canHightANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
import math

class FrontEdge(edges.BaseEdge):
    char = "a"

    def __call__(self, length, **kw):
        x = math.ceil( ((self.canDiameter * 0.5 + 2 * self.thickness) * math.sin(math.radians(self.angle))) / self.thickness)
        if self.top_edge != "e":
            self.corner(90, self.thickness)
            self.edge(0.5 * self.canDiameter)            
            self.corner(-90, 0.25 * self.canDiameter)
        else:
            self.moveTo(-self.burn, self.canDiameter + self.thickness, -90)
            self.corner(90, 0.25 * self.canDiameter)
            self.edge(self.thickness)

        self.edge(0.5 * self.canDiameter - self.thickness)
        self.corner(-90, 0.25 * self.canDiameter)
        self.edge(0.5 * self.canDiameter)
        self.corner(90, self.thickness)
        self.edge(x * self.thickness )
        self.corner(90, self.thickness)
        self.edge(0.5 * self.canDiameter)
        self.corner(-90, 0.25 * self.canDiameter)
        self.edge(0.5 * self.canDiameter - (1 + x) * self.thickness + self.top_chute_height + self.bottom_chute_height - self.barrier_height)
        self.corner(-90, 0.25 * self.canDiameter)
        self.edge(0.5 * self.canDiameter)
        self.corner(90, self.thickness)
        self.edge(self.barrier_height)
        self.edge(self.thickness)

class CanStorage(Boxes): # self.canHightange class name!
    """Storage box for round containers"""

    ui_group = "Misc"
    
    angle = 3.0 # slope angle of the chutes in degree
    
    def __init__(self):
        Boxes.__init__(self)

        self.addSettingsArgs(edges.FingerJointSettings, finger=2.0, space=2.0, surroundingspaces=0.0)

        self.argparser.add_argument(
            "--top_edge", action="store",
            type=ArgparseEdgeType("efhŠ"), choices=list("efhŠ"),
            default="Š", help="edge type for top edge")
        self.argparser.add_argument(
            "--bottom_edge", action="store",
            type=ArgparseEdgeType("eEš"), choices=list("eEš"),
            default="š", help="edge type for bottom edge")

        # Add non default cli params if needed (see argparse std lib)
        self.argparser.add_argument(
            "--canDiameter",  action="store", type=float, default=67,
            help="outer diameter of the cans to be stored (in mm)")
        self.argparser.add_argument(
            "--canHight",  action="store", type=float, default=115,
            help="hight of the cans to be stored (in mm)")
        self.argparser.add_argument(
            "--canNum",  action="store", type=int, default=12,
            help="number of cans to be stored")
            
    def cb(self, nr):
        if nr == 0:
            # for debugging only
            if self.mydebug:
                # draw orientation points
                self.hole(0, 0, 1)
                self.hole(0, self.thickness, 1)
                self.hole(0, self.thickness + self.canDiameter, 1)
                self.hole(0, self.thickness + self.canDiameter + self.bottom_chute_height, 1)
                self.hole(0, self.thickness + self.canDiameter + self.bottom_chute_height + self.top_chute_height + self.thickness, 1)
                self.hole(0, self.thickness + self.canDiameter + self.bottom_chute_height + self.top_chute_height + self.thickness + self.canDiameter, 1)
                self.hole(0, self.thickness + self.canDiameter + self.bottom_chute_height + self.top_chute_height + self.thickness + self.canDiameter + 1.0 * self.thickness, 1)
                with self.saved_context():
                    # draw cans, bottom row
                    self.moveTo(0, self.thickness, self.angle)
                    self.rectangularHole(0, 0, math.ceil(self.canNum / 2) * self.canDiameter, self.canDiameter, center_x=False, center_y=False, color=Color.ANNOTATIONS)
                    for i in range(math.ceil(self.canNum / 2)):
                        self.hole((0.5 + i) * self.canDiameter, self.canDiameter / 2, self.canDiameter / 2, color=Color.ANNOTATIONS)
                with self.saved_context():
                    # draw cans, top row
                    self.moveTo(0, self.thickness + self.canDiameter + self.bottom_chute_height + self.top_chute_height + 0.5 * self.thickness, -self.angle)
                    self.rectangularHole(0, 0.5 * self.thickness, math.ceil(self.canNum / 2) * self.canDiameter, self.canDiameter, center_x=False, center_y=False, color=Color.ANNOTATIONS)
                    for i in range(math.ceil(self.canNum / 2)):
                        self.hole((0.5 + i) * self.canDiameter, self.canDiameter / 2 + 0.5 * self.thickness, self.canDiameter / 2, color=Color.ANNOTATIONS)
                with self.saved_context():
                    # draw barrier
                    self.moveTo(0.5 * self.thickness, 1.1 * self.thickness + self.burn, 90)
                    self.rectangularHole(0, 0, self.barrier_height, self.thickness, center_x=False, center_y=True, color=Color.ANNOTATIONS)

            # bottom chute
            with self.saved_context():
                self.moveTo(0, 0.5 * self.thickness, self.angle)
                self.fingerHolesAt(0, 0, self.depth / math.cos(math.radians(self.angle)), 0)
            # top chute
            with self.saved_context():
                self.moveTo(0, self.thickness + self.canDiameter + self.bottom_chute_height + self.top_chute_height + 0.5 * self.thickness, -self.angle)
                self.fingerHolesAt(0, 0, self.top_chute_depth, 0)
            # front barrier
            with self.saved_context():
                self.moveTo(0.5 * self.thickness, 1.1 * self.thickness + self.burn, 90)
                self.fingerHolesAt(0, 0, self.barrier_height, 0)
        
    def render(self):
        self.mydebug = False # set to True to enable debugging

        self.addPart(FrontEdge(self, self))
        
        if self.canDiameter < 8 * self.thickness:
            self.edges["f"].settings.setValues(self.thickness, True, finger=1.0)
            self.edges["f"].settings.setValues(self.thickness, True, space=1.0)
        self.edges["f"].settings.setValues(self.thickness, True, surroundingspaces=0.0)
        
        if self.canDiameter < 4 * self.thickness:
            raise ValueError("Can diameter has to be at least 4 times the meterial thickness!")

        if self.canNum < 4:
            raise ValueError("4 cans is the minimum!")

        
        self.depth = self.canDiameter * (math.ceil(self.canNum / 2) + 0.1) + self.thickness
        self.top_chute_height = max(self.depth * math.sin(math.radians(self.angle)), 0.1 * self.canDiameter)
        self.top_chute_depth = (self.depth - 1.1 * self.canDiameter) / math.cos(math.radians(self.angle))
        self.bottom_chute_height = max((self.depth - 1.1 * self.canDiameter) * math.sin(math.radians(self.angle)), 0.1 * self.canDiameter)
        self.bottom_chute_depth = self.depth / math.cos(math.radians(self.angle))
        self.barrier_height = 0.25 * self.canDiameter
        
        if (self.top_chute_depth + self.bottom_chute_height - self.thickness) < (self.barrier_height + self.canDiameter * 0.1):
            self.bottom_chute_height = self.barrier_height + self.canDiameter * 0.1 + self.thickness - self.top_chute_depth
        
        self.height = self.thickness + self.canDiameter + self.bottom_chute_height + self.top_chute_height + 0.5 * self.thickness + self.canDiameter + 1.5 * self.thickness # measurements from bottom to top
        self.width = 0.01 * self.canHight + self.canHight + 0.01 * self.canHight
        edgs = self.bottom_edge + "h" + self.top_edge + "a"
        
        # render your parts here
        self.rectangularWall(self.depth, self.height, edges=edgs, callback=self.cb, move="up", label="right")
        self.rectangularWall(self.depth, self.height, edges=edgs, callback=self.cb, move="up mirror", label="left")
        
        self.rectangularWall(self.bottom_chute_depth, self.width, "fefe", move="up", label="bottom chute")
        self.rectangularWall(self.top_chute_depth, self.width, "fefe", move="up", label="top chute")

        self.rectangularWall(self.barrier_height, self.width, "fefe", move="right", label="barrier")
        self.rectangularWall(self.height, self.width, "fefe", move="up", label="back")
        self.rectangularWall(self.barrier_height, self.width, "fefe", move="left only", label="invisible")
        
        if self.top_edge != "e":
            self.rectangularWall(self.depth, self.width, "fefe", move="up", label="top")
