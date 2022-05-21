# Copyright (C) 2013-2014 Florian Festi
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
from boxes.edges import Settings

class _ChestLid(Boxes):

    def getR(self, x, angle=0):
        t = self.thickness
        d = x - 2*math.sin(math.radians(angle)) * (3*t)

        r = d / 2.0 / math.cos(math.radians(angle))
        return r

    def side(self, x, angle=0, move="", label=""):
        if "a" not in self.edges:
            s = edges.FingerJointSettings(self.thickness, True,
                                          finger=1.0, space=1.0)
            s.edgeObjects(self, "aA.")

        t = self.thickness
        r = self.getR(x, angle)
        if self.move(x+2*t, 0.5*x+3*t, move, True, label=label):
            return

        self.moveTo(t, 0)
        self.edge(x)
        self.corner(90+angle)
        self.edges["a"](3*t)
        self.corner(180-2*angle, r)
        self.edges["a"](3*t)
        self.corner(90+angle)

        self.move(x+2*t, 0.5*x+3*t, move, False, label=label)

    def top(self, x, y, angle=0, move=None, label=""):
        if "a" not in self.edges:
            s = edges.FingerJointSettings(self.thickness, True,
                                          finger=1.0, space=1.0)
            s.edgeObjects(self, "aA.")

        t = self.thickness
        l = math.radians(180-2*angle) * self.getR(x, angle)

        tw = l + 6*t
        th = y+2*t

        if self.move(tw, th, move, True, label=label):
            return

        self.edges["A"](3*t)
        self.edges["X"](l, y+2*t)
        self.edges["A"](3*t)
        self.corner(90)
        self.edge(y+2*t)
        self.corner(90)
        self.edges["A"](3*t)
        self.edge(l)
        self.edges["A"](3*t)
        self.corner(90)
        self.edge(y+2*t)
        self.corner(90)

        self.move(tw, th, move, label=label)
        
    def cutHandleHole(self, x, y, ext):
        ht = self.edgesettings.get('LidWithHandle')['HandleThickness']
        hl = self.edgesettings.get('LidWithHandle')['HandleLength']
        ad = self.edgesettings.get('LidWithHandle')['AlignmentDiameter']
        self.moveTo((self.thickness / 4 + 0.5 * self.burn), (self.thickness / 4 + 1.5 * self.burn))
        if ext == 0:
            x += 2 * self.thickness 
            y += 2 * self.thickness 
        self.rectangularHole(x / 2, y / 2, self.thickness * ht, hl + ext * 2 * self.thickness, r=0, center_x=True, center_y=True)
#        self.hole((2 - ext) * self.thickness + ad / 2, (2 - ext) * self.thickness + ad / 2, ad / 2) # two holes are enough for alingment
        self.hole(x - (2 - ext) * self.thickness - ad / 2, (2 - ext) * self.thickness + ad / 2, ad / 2)
        self.hole((2 - ext) * self.thickness + ad / 2, y - (2 - ext) * self.thickness - ad / 2, ad / 2)
        self.moveTo(-1 * (self.thickness / 4 + 0.5 * self.burn), -1 * (self.thickness / 4 + 1.5 * self.burn))

    def drawAddOnLid(self, x, y, style):
        hl = self.edgesettings.get('LidWithHandle')['HandleLength']
        ht = self.edgesettings.get('LidWithHandle')['HandleThickness']
        hh = self.edgesettings.get('LidWithHandle')['HandleHeight']
        hr = self.edgesettings.get('LidWithHandle')['HandleRadius']
        ad = self.edgesettings.get('LidWithHandle')['AlignmentDiameter']
        if ad > self.thickness:
            raise ValueError("LidWithHandle: maximum alingment diameter is material thickness")
        
        if style == "flat":
            self.rectangularWall(x, y, "eeee", move="right", label="lid bottom")
            self.rectangularWall(x, y, "EEEE", move="up", label="lid top")
        elif style == "flat with handle":
            self.rectangularWall(x, y, "eeee", callback=[self.cutHandleHole(x, y, 1), ], move="right", label="lid bottom")
            self.rectangularWall(x, y, "EEEE", callback=[self.cutHandleHole(x, y, 0),], move="up", label="lid top")
            for i in range(ht):
                if self.move(hl + 2 * self.thickness, hh + 2 * self.thickness, "right", True, label="Lid Handle " + str(i)):
                    return
                self.edge(hl + 2 * self.thickness)
                self.corner(90)
                self.edge(self.thickness)
                self.corner(90)
                self.edge(self.thickness)
                self.corner(-90)
                self.edge(hh + self.thickness - hr)
                self.corner(90, hr)
                self.edge(hl - 2 * hr)
                self.corner(90, hr)
                self.edge(hh + self.thickness - hr)
                self.corner(-90)
                self.edge(self.thickness)
                self.corner(90)
                self.edge(self.thickness)
                self.corner(90)
                self.moveTo(-self.burn, 0)
                self.hole(self.thickness + ad * 2 , self.thickness, ad / 2)
                self.hole(hl + self.thickness - ad * 2 , self.thickness, ad / 2)                                
                self.move(hl + 2 * self.thickness, hh + 2 * self.thickness, "right", False, label="Lid Handle " + str(i))
        elif style == "chest":
            self.side(x, move="right", label="lid right")
            self.side(x, move="up", label="lid left")
            self.side(x, move="left only", label="invisible")
            self.top(x, y, move="up", label="lid top")
        else:
            return False
        return True

class LidWithHandleSettings(Settings):

    """Settings for Flat Lid with Handle
Values:
* absolute_params

 * AlignmentDiameter : 2.0 : diameter of alingment pin holes (in mm, 0 for None) 
 * HandleLength : 30.0 : length of the handle (in mm)
 * HandleHeight : 15.0 : height of the handle (in mm)
 * HandleRadius :  5.0 : radius of the handle (in mm)

* relative (in multiples of thickness)

 * HandleThickness : 2 : thickness of handle (in multiples of material thickness)
"""

    absolute_params = {
        "HandleLength" : 30.0,
        "HandleHeight" : 15.0,
        "HandleRadius" : 5.0,
        "AlignmentDiameter" : 2.0,
        }

    relative_params = {
        "HandleThickness" : 2,
        }

class _TopEdge(Boxes):

    def addTopEdgeSettings(self, fingerjoint={}, stackable={}, hinge={},
                           cabinethinge={}, lid={}, click={},
                           roundedtriangle={}):
        self.addSettingsArgs(edges.FingerJointSettings, **fingerjoint)
        self.addSettingsArgs(edges.StackableSettings, **stackable)
        self.addSettingsArgs(edges.HingeSettings, **hinge)
        self.addSettingsArgs(edges.CabinetHingeSettings, **cabinethinge)
        self.addSettingsArgs(edges.LidSettings, **lid)
        self.addSettingsArgs(edges.ClickSettings, **click)
        self.addSettingsArgs(edges.RoundedTriangleEdgeSettings, **roundedtriangle)

    def topEdges(self, top_edge):
        t1 = t2 = t3 = t4 = self.edges.get(top_edge, self.edges["e"])

        if t1.char == "i":
            t2 = t4 = "e"
            t3 = "j"
        elif t1.char == "k":
            t2 = t4 = "e"
        elif t1.char == "L":
            t1 = "M"
            t2 = "e"
            t3 = "N"
        elif t1.char == "v":
            t2 = t3 = t4 = "e"
        elif t1.char == "t":
            t1 = t3 = "e"
        return [t1, t2, t3, t4]

    def drawLid(self, x, y, top_edge, bedBolts=[None, None]):
        d2, d3 = bedBolts
        if top_edge == "c":
            self.rectangularWall(x, y, "CCCC", bedBolts=[d2, d3, d2, d3], move="up", label="top")
        elif top_edge == "f":
            self.rectangularWall(x, y, "FFFF", move="up", label="top")
        elif top_edge in "FhŠ":
            self.rectangularWall(x, y, "ffff", move="up", label="top")
        elif top_edge == "L":
            self.rectangularWall(x, y, "nlmE", move="up", label="lid top")
        elif top_edge == "i":
            self.rectangularWall(x, y, "IEJe", move="up", label="lid top")
        elif top_edge == "k":
            outset =  self.edges["k"].settings.outset
            self.edges["k"].settings.setValues(self.thickness, outset=True)
            lx = x/2.0-0.1*self.thickness
            self.edges['k'].settings.setValues(self.thickness, grip_length=5)
            self.rectangularWall(lx, y, "IeJe", move="right", label="lid top left")
            self.rectangularWall(lx, y, "IeJe", move="up", label="lid top right")
            self.rectangularWall(lx, y, "IeJe", move="left only", label="invisible")
            self.edges["k"].settings.setValues(self.thickness, outset=outset)
        elif top_edge == "S":
            self.rectangularWall(x, y, "ffff", move="up", label="lid top")
            self.rectangularWall(x, 0, "sFeF", move="up", label="lid top left")
            self.rectangularWall(x, 0, "sFeF", move="up", label="lid top right")
            self.rectangularWall(y, 0, "sfef", move="up", label="lid top front")
            self.rectangularWall(y, 0, "sfef", move="up", label="lid top back")
        elif top_edge == "v":
            self.rectangularWall(x, y, "VEEE", move="up", label="lid top")
            self.edges["v"].parts(move="up")
        else:
            return False
        return True

