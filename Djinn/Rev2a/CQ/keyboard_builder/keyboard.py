import cadquery as cq
import math
from . import primitives

class keyboard:

    def __init__(self, **kwargs):

        d = {
            "locationFiducialSize": 0.25,
            "switchSizeX": 19.05,
            "switchSizeY": 19.05,
            "switchCutX": 14,
            "switchCutY": 14,
            "switchCutFillet": 0.5,
            "outlineOffset": 5,
            "handAngleDegrees": 10,
            "rowCounts": [],
            "columnDeltas": [],
            "extraKeys": [],
            "outlineLocations": [],
            "spacerOffset": 1,
            "extraDrills": [],
            "edgeLEDCounts": [],
            "drillRadius": 1.6,
            "drillPadRadius": 3.5,
            "spacerRadius": 2.25, # size of holes that brass spacers need to pass through
            "lcdX": 7.6, # in keyswitch units
            "lcdY": 2.7, # in keyswitch units
            "lcdWidth": 40.1,
            "lcdHeight": 67.2,
            "lcdDrillWidth": 34.1,
            "lcdDrillHeight": 61.2,
            "lcdDrillRadius": 1.6,
            "lcdDrillPadRadius": 3.5,
            "lcdPinCutoutWidth": 26.2,
            "lcdPinCutoutHeight": 2.9,
            "lcdPinCutoutY": 32.14701,
            "lcdPinCutoutFillet": 1,
            "encoderX": 7.65, # in keyswitch units
            "encoderY": 4, # in keyswitch units
            "encoderCutX": 13,
            "encoderCutY": 13,
            "encoderCutFillet": 0.5,
            "encoderKnobDiameter": 26.2,
            "dpadX": 5.375, # in keyswitch units
            "dpadY": 5.5, # in keyswitch units
            "dpadCutDiameter": 6,
            "dpadHousingWidth": 14,
            "dpadHousingHeight": 14,
            "resetX": 8.625, # in keyswitch units
            "resetY": 3.375, # in keyswitch units
            "resetCutDiameter": 3, # hole for reset button
            "resetHousingWidth": 7,
            "resetHousingHeight": 7,
            "ledSizeX": 8,
            "ledSizeY": 4,
            "ledCutFillet": 1.5,
            "ledOffset": 1.5,
            "usbX": 6.3, # in keyswitch units
            "usbY": -1.037234, # in keyswitch units
            "usbWidth": 9.5,
            "usbHeight": 8,
            "splitX": 7.375, # in keyswitch units
            "splitY": -0.7265, # in keyswitch units
            "splitWidth": 9.5,
            "splitHeight": 8,
        }

        d.update(kwargs)

        self.__switchOrder = d["switchOrder"]
        self.__ledFlip = d["ledFlip"]

        self.__switchSizeX = float(d["switchSizeX"])
        self.__switchSizeY = float(d["switchSizeY"])
        self.__switchCutX = float(d["switchCutX"])
        self.__switchCutY = float(d["switchCutY"])
        self.__switchCutFillet = float(d["switchCutFillet"])

        self.__outlineOffset = float(d["outlineOffset"])
        self.__spacerOffset = float(d["spacerOffset"])
        self.__handAngle = math.radians(float(d["handAngleDegrees"]))

        self.__locationFiducialSize = float(d["locationFiducialSize"])

        self.__rowCounts = d["rowCounts"]
        self.__columnDeltas = d["columnDeltas"]
        self.__extraKeys = d["extraKeys"]
        self.__outlineLocations = d["outlineLocations"]
        self.__spacerLocations = d["spacerLocations"]
        self.__extraDrills = d["extraDrills"]
        self.__edgeLEDCounts = d["edgeLEDCounts"]
        self.__extraLeds = d["extraLeds"]

        self.__drillRadius = float(d["drillRadius"])
        self.__drillPadRadius = float(d["drillPadRadius"])
        self.__spacerRadius = float(d["spacerRadius"])

        self.__lcdX = float(d["lcdX"])
        self.__lcdY = float(d["lcdY"])
        self.__lcdWidth = float(d["lcdWidth"])
        self.__lcdHeight = float(d["lcdHeight"])
        self.__lcdDrillWidth = float(d["lcdDrillWidth"])
        self.__lcdDrillHeight = float(d["lcdDrillHeight"])
        self.__lcdDrillRadius = float(d["lcdDrillRadius"])
        self.__lcdDrillPadRadius = float(d["lcdDrillPadRadius"])
        self.__lcdPinCutoutWidth = float(d["lcdPinCutoutWidth"])
        self.__lcdPinCutoutHeight = float(d["lcdPinCutoutHeight"])
        self.__lcdPinCutoutY = float(d["lcdPinCutoutY"])
        self.__lcdPinCutoutFillet = float(d["lcdPinCutoutFillet"])

        self.__encoderX = float(d["encoderX"])
        self.__encoderY = float(d["encoderY"])
        self.__encoderCutX = float(d["encoderCutX"])
        self.__encoderCutY = float(d["encoderCutY"])
        self.__encoderCutFillet = float(d["encoderCutFillet"])
        self.__encoderKnobDiameter = float(d["encoderKnobDiameter"])

        self.__dpadX = float(d["dpadX"])
        self.__dpadY = float(d["dpadY"])
        self.__dpadCutDiameter = float(d["dpadCutDiameter"])
        self.__dpadHousingWidth = float(d["dpadHousingWidth"])
        self.__dpadHousingHeight = float(d["dpadHousingHeight"])

        self.__resetX = float(d["resetX"])
        self.__resetY = float(d["resetY"])
        self.__resetCutDiameter = float(d["resetCutDiameter"])
        self.__resetHousingWidth = float(d["resetHousingWidth"])
        self.__resetHousingHeight = float(d["resetHousingHeight"])

        self.__ledSizeX = float(d["ledSizeX"])
        self.__ledSizeY = float(d["ledSizeY"])
        self.__ledCutFillet = float(d["ledCutFillet"])
        self.__ledOffset = float(d["ledOffset"])

        self.__usbX = float(d["usbX"])
        self.__usbY = float(d["usbY"])
        self.__usbWidth = float(d["usbWidth"])
        self.__usbHeight = float(d["usbHeight"])

        self.__splitX = float(d["splitX"])
        self.__splitY = float(d["splitY"])
        self.__splitWidth = float(d["splitWidth"])
        self.__splitHeight = float(d["splitHeight"])

        self.__workplane = cq.Workplane("XY")

        self.__post_processing()

    def __post_processing(self):

        self.__generated = {}

        allKeys = []
        allLeds = []

        # Work out the switch locations
        currY = 0
        switchIndex = 0
        for col in range(len(self.__rowCounts)):

            count = self.__rowCounts[col]
            offset = self.__columnDeltas[col]
            currY = currY + offset

            for row in range(count):
                order = self.__switchOrder[switchIndex]
                keyloc = primitives.point(col, currY + row)
                keypos = self.__keyloc_to_xy_mm(keyloc.x, keyloc.y)
                allKeys.append([order, keyloc, keypos]) # component ID, x/y pos (key coords), x/y pos (mm)

                ledFlip = self.__ledFlip[switchIndex]
                allLeds.append([False, order, primitives.point(keypos.x, keypos.y-5.08), ledFlip, 0]) # component ID, x/y pos, flipped, rotation

                switchIndex = switchIndex + 1

        for extra in self.__extraKeys:
            order = self.__switchOrder[switchIndex]
            keypos = self.__keyloc_to_xy_mm(extra.x, extra.y)
            allKeys.append([order, extra, keypos]) # component ID, x/y pos (key coords), x/y pos (mm)

            ledFlip = self.__ledFlip[switchIndex]
            allLeds.append([False, order, primitives.point(keypos.x, keypos.y-5.08), ledFlip, 0]) # edge LED, component ID, x/y pos, flipped, rotation

            switchIndex = switchIndex + 1

        order = 0
        for i in range(0,len(self.__edgeLEDCounts)):
            if self.__edgeLEDCounts[i] > 0:
                this_drill = self.__outlineLocations[i]
                next_drill = self.__outlineLocations[(i+1) % len(self.__outlineLocations)]
                edge = primitives.edge(self.__keyloc_to_xy_mm(this_drill["position"].x, this_drill["position"].y, this_drill["offsetByHandAngle"]), self.__keyloc_to_xy_mm(next_drill["position"].x, next_drill["position"].y, next_drill["offsetByHandAngle"])).offset(self.__ledOffset)
                led_count = self.__edgeLEDCounts[i]
                lerpFactor = 1.0 / (1 + led_count)
                for n in range(0, led_count):
                    pos = edge.lerp((n+1)*lerpFactor)
                    allLeds.append([True, self.__extraLeds[order], pos, True, 180+edge.degrees]) # edge LED, component ID, x/y pos, flipped, rotation
                    order = order + 1

        allDrills = []
        allDrills.extend(self.__outlineLocations)
        allDrills.extend(self.__extraDrills)

        for drill in allDrills:
            drill["location"] = self.__keyloc_to_xy_mm(drill["position"].x, drill["position"].y, drill["offsetByHandAngle"])

        self.__generated = {
            "keys": allKeys,
            "leds": allLeds,
            "drills": allDrills,
            "lcd": {
                "position": primitives.point(self.__lcdX, self.__lcdY),
                "location": self.__keyloc_to_xy_mm(self.__lcdX, self.__lcdY, True)
            },
            "encoder": {
                "position": primitives.point(self.__encoderX, self.__encoderY),
                "location": self.__keyloc_to_xy_mm(self.__encoderX, self.__encoderY)
            },
            "dpad": {
                "position": primitives.point(self.__dpadX, self.__dpadY),
                "location": self.__keyloc_to_xy_mm(self.__dpadX, self.__dpadY)
            },
            "reset": {
                "position": primitives.point(self.__resetX, self.__resetY),
                "location": self.__keyloc_to_xy_mm(self.__resetX, self.__resetY)
            },
            "usb": {
                "position": primitives.point(self.__usbX, self.__usbY),
                "location": self.__keyloc_to_xy_mm(self.__usbX, self.__usbY)
            },
            "split": {
                "position": primitives.point(self.__splitX, self.__splitY),
                "location": self.__keyloc_to_xy_mm(self.__splitX, self.__splitY)
            },
        }

        return

    def __keyloc_to_xy_mm(self, x_key, y_key, offset_by_hand_angle=False):

        if offset_by_hand_angle:

            return primitives.point(
                (x_key * self.__switchSizeX) * math.cos(-self.__handAngle) - (y_key * self.__switchSizeY) * math.sin(-self.__handAngle),
                -(x_key * self.__switchSizeX) * math.sin(-self.__handAngle) - (y_key * self.__switchSizeY) * math.cos(-self.__handAngle)
                 )

        return primitives.point(x_key * self.__switchSizeX, - y_key * self.__switchSizeY) # intentionally inverted Y-coord


    def __keyswitch_cut_at_xy(self, workplane, xy_mm):
        (x_mm, y_mm) = (xy_mm.x, xy_mm.y)
        cutObj = primitives.draw_rounded_rectangle(x_mm, y_mm, self.__switchCutX, self.__switchCutY, self.__switchCutFillet)
        workplane.add(cutObj)

    def __keyswitch_cut_at_keyloc(self, workplane, x_key, y_key):
        return self.__keyswitch_cut_at_xy(workplane, self.__keyloc_to_xy_mm(x_key, y_key))

    def __keyswitch_outline_at_xy(self, workplane, xy_mm):
        (x_mm, y_mm) = (xy_mm.x, xy_mm.y)
        outlineObj = primitives.draw_rectangle(x_mm, y_mm, self.__switchSizeX, self.__switchSizeY)
        workplane.add(outlineObj)

    def __keyswitch_outline_at_keyloc(self, workplane, x_key, y_key):
        return self.__keyswitch_outline_at_xy(workplane, self.__keyloc_to_xy_mm(x_key, y_key))

    def __circle_at_xy(self, workplane, xy_mm, r_mm):
        (x_mm, y_mm) = (xy_mm.x, xy_mm.y)
        outlineObj = primitives.draw_circle(x_mm, y_mm, r_mm)
        workplane.add(outlineObj)

    def __circle_at_keyloc(self, workplane, x_key, y_key, r_mm, offset_by_hand_angle=False):
        return self.__circle_at_xy(workplane, self.__keyloc_to_xy_mm(x_key, y_key, offset_by_hand_angle), r_mm)

    def __render_keys(self, workplane, d):
        if bool(d["locations"]):
            print("Key locations:")

        for key in self.__generated["keys"]:
            keyloc = key[1]
            keypos = key[2]
            if bool(d["keyswitchCuts"]):
                self.__keyswitch_cut_at_keyloc(workplane, keyloc.x, keyloc.y)

            if bool(d["keyswitchOutlines"]):
                self.__keyswitch_outline_at_keyloc(workplane, keyloc.x, keyloc.y)

            if bool(d["locations"]):
                self.__circle_at_keyloc(workplane, keyloc.x, keyloc.y, self.__locationFiducialSize)
                print(f"    ({keypos.x:8.3f}, {keypos.y:8.3f})")

    def __render_drills(self, workplane, d):

        if bool(d["drills"]) or bool(d["drillPads"]) or bool(d["spacer"]):

            if bool(d["locations"]):
                print("Drill locations:")

            for drill in self.__generated["drills"]:
                if drill["isDrill"]:

                    if bool(d["drills"]):
                        self.__circle_at_keyloc(workplane, drill["position"].x, drill["position"].y, self.__drillRadius, drill["offsetByHandAngle"])
                    if bool(d["drillPads"]):
                        self.__circle_at_keyloc(workplane, drill["position"].x, drill["position"].y, self.__drillPadRadius, drill["offsetByHandAngle"])
                    if bool(d["spacer"]):
                        self.__circle_at_keyloc(workplane, drill["position"].x, drill["position"].y, self.__spacerRadius, drill["offsetByHandAngle"])

                    if bool(d["locations"]):
                        self.__circle_at_keyloc(workplane, drill["position"].x, drill["position"].y, self.__locationFiducialSize, drill["offsetByHandAngle"])

                        xy_mm = self.__keyloc_to_xy_mm(drill["position"].x, drill["position"].y, drill["offsetByHandAngle"])
                        (x_mm, y_mm) = (xy_mm.x, xy_mm.y)
                        print(f"    ({x_mm:8.3f}, {y_mm:8.3f})")

    def __render_outline(self, workplane, d, outlineArray, offset):

        outline = cq.Workplane("XY")
        arcs = []

        for i in range(0, len(outlineArray)):
            last_drill = outlineArray[(i-1) % len(outlineArray)]
            this_drill = outlineArray[i]
            next_drill = outlineArray[(i+1) % len(outlineArray)]

            edge_ab = primitives.edge(self.__keyloc_to_xy_mm(last_drill["position"].x, last_drill["position"].y, last_drill["offsetByHandAngle"]), self.__keyloc_to_xy_mm(this_drill["position"].x, this_drill["position"].y, this_drill["offsetByHandAngle"]))
            edge_bc = primitives.edge(self.__keyloc_to_xy_mm(this_drill["position"].x, this_drill["position"].y, this_drill["offsetByHandAngle"]), self.__keyloc_to_xy_mm(next_drill["position"].x, next_drill["position"].y, next_drill["offsetByHandAngle"]))

            # Work out the offset from the centre, if overridden
            this_offset = this_drill["radius"] if "radius" in this_drill else offset

            # Flip convex/concave if we're generating an internal contour
            convex = this_drill["convex"] if this_offset > 0 else not this_drill["convex"]

            this_arc = primitives.arc(edge_ab, edge_bc, this_offset, convex)
            if this_arc.chord_length > 1e-9:
                arcs.append(this_arc)

        last_arc = arcs[-1]
        outline = outline.moveTo(primitives.mm2m(last_arc.end.x), primitives.mm2m(last_arc.end.y))
        for this_arc in arcs:
            outline = outline.lineTo(primitives.mm2m(this_arc.start.x), primitives.mm2m(this_arc.start.y))
            outline = outline.tangentArcPoint(cq.Vector(primitives.mm2m(this_arc.end.x), primitives.mm2m(this_arc.end.y)), relative=False)

            if bool(d["locations"]):
                self.__circle_at_xy(workplane, this_arc.centre, self.__locationFiducialSize)

        workplane.add(outline.wire().combine())

    def __render_lcd(self, workplane, d):

        pos = self.__keyloc_to_xy_mm(self.__lcdX, self.__lcdY, True)

        if bool(d["locations"]) and (bool(d["lcdOutline"]) or bool(d["lcdDrills"]) or bool(d["lcdDrillPads"])):
            print("LCD location:")

        lcd = cq.Workplane("XY")

        if bool(d["lcdOutline"]):
            outline = cq.Workplane("XY").add(
                primitives.draw_rectangle(0, 0, self.__lcdWidth, self.__lcdHeight))
            lcd.add(outline.wire())

        if bool(d["lcdDrills"]):
            drills = cq.Workplane("XY")
            self.__circle_at_xy(drills, primitives.point(-self.__lcdDrillWidth/2.0, -self.__lcdDrillHeight/2.0), self.__lcdDrillRadius)
            self.__circle_at_xy(drills, primitives.point(+self.__lcdDrillWidth/2.0, -self.__lcdDrillHeight/2.0), self.__lcdDrillRadius)
            self.__circle_at_xy(drills, primitives.point(-self.__lcdDrillWidth/2.0, +self.__lcdDrillHeight/2.0), self.__lcdDrillRadius)
            self.__circle_at_xy(drills, primitives.point(+self.__lcdDrillWidth/2.0, +self.__lcdDrillHeight/2.0), self.__lcdDrillRadius)
            lcd.add(drills.combine())

        if bool(d["lcdPlateCuts"]) or bool(d["lcdSpacerCuts"]):
            drills = cq.Workplane("XY")

            # Top left drill doesn't participate in the spacers
            if bool(d["lcdPlateCuts"]):
                self.__circle_at_xy(drills, primitives.point(-self.__lcdDrillWidth/2.0, +self.__lcdDrillHeight/2.0), self.__spacerRadius)
            self.__circle_at_xy(drills, primitives.point(+self.__lcdDrillWidth/2.0, +self.__lcdDrillHeight/2.0), self.__spacerRadius)
            self.__circle_at_xy(drills, primitives.point(-self.__lcdDrillWidth/2.0, -self.__lcdDrillHeight/2.0), self.__spacerRadius)
            self.__circle_at_xy(drills, primitives.point(+self.__lcdDrillWidth/2.0, -self.__lcdDrillHeight/2.0), self.__spacerRadius)
            lcd.add(drills.combine())
            pinCut = cq.Workplane("XY").add(
                primitives.draw_rounded_rectangle(0, -self.__lcdPinCutoutY, self.__lcdPinCutoutWidth, self.__lcdPinCutoutHeight, self.__lcdPinCutoutFillet))
            lcd.add(pinCut.wire())

        if bool(d["lcdDrillPads"]):
            pads = cq.Workplane("XY")
            self.__circle_at_xy(pads, primitives.point(-self.__lcdDrillWidth/2.0, -self.__lcdDrillHeight/2.0), self.__lcdDrillPadRadius)
            self.__circle_at_xy(pads, primitives.point(+self.__lcdDrillWidth/2.0, -self.__lcdDrillHeight/2.0), self.__lcdDrillPadRadius)
            self.__circle_at_xy(pads, primitives.point(-self.__lcdDrillWidth/2.0, +self.__lcdDrillHeight/2.0), self.__lcdDrillPadRadius)
            self.__circle_at_xy(pads, primitives.point(+self.__lcdDrillWidth/2.0, +self.__lcdDrillHeight/2.0), self.__lcdDrillPadRadius)
            lcd.add(pads.combine())

        workplane.add(
            lcd.rotate((0,0,0), (0,0,1), math.degrees(self.__handAngle))
               .translate((primitives.mm2m(pos.x), primitives.mm2m(pos.y))))

        if bool(d["locations"]):
            self.__circle_at_keyloc(workplane, self.__lcdX, self.__lcdY, self.__locationFiducialSize, True)
            (x_mm, y_mm) = (pos.x, pos.y)
            print(f"    ({x_mm:8.3f}, {y_mm:8.3f})")

    def __render_encoder(self, workplane, d):

        pos = self.__keyloc_to_xy_mm(self.__encoderX, self.__encoderY)

        if bool(d["locations"]):
            print("Encoder location:")

        if bool(d["encoderCut"]):
            workplane.add(
                primitives.draw_rounded_rectangle(pos.x, pos.y, self.__encoderCutX, self.__encoderCutY, self.__encoderCutFillet)
            )

        if bool(d["encoderKnob"]):
            self.__circle_at_xy(workplane, pos, self.__encoderKnobDiameter/2.0)

        if bool(d["locations"]):
            self.__circle_at_xy(workplane, pos, self.__locationFiducialSize)
            (x_mm, y_mm) = (pos.x, pos.y)
            print(f"    ({x_mm:8.3f}, {y_mm:8.3f})")

    def __render_dpad(self, workplane, d):

        pos = self.__keyloc_to_xy_mm(self.__dpadX, self.__dpadY)

        if bool(d["dpadCut"]) or bool(d["dpadHousing"]):

            if bool(d["dpadCut"]):
                self.__circle_at_xy(workplane, pos, self.__dpadCutDiameter/2.0)

            if bool(d["dpadHousing"]):
                workplane.add(
                    primitives.draw_rectangle(pos.x, pos.y, self.__dpadHousingWidth, self.__dpadHousingHeight)
                )

            if bool(d["locations"]):
                self.__circle_at_xy(workplane, pos, self.__locationFiducialSize)
                (x_mm, y_mm) = (pos.x, pos.y)
                print("D-pad location:")
                print(f"    ({x_mm:8.3f}, {y_mm:8.3f})")

    def __render_reset(self, workplane, d):

        pos = self.__keyloc_to_xy_mm(self.__resetX, self.__resetY)

        if bool(d["resetCut"]) or bool(d["resetHousing"]):

            if bool(d["resetCut"]):
                self.__circle_at_xy(workplane, pos, self.__resetCutDiameter/2.0)

            if bool(d["resetHousing"]):
                workplane.add(
                    primitives.draw_rectangle(pos.x, pos.y, self.__resetHousingWidth, self.__resetHousingHeight)
                )

            if bool(d["locations"]):
                self.__circle_at_xy(workplane, pos, self.__locationFiducialSize)
                (x_mm, y_mm) = (pos.x, pos.y)
                print("Reset location:")
                print(f"    ({x_mm:8.3f}, {y_mm:8.3f})")

    def __render_connector_cutouts(self, workplane, d):

        if bool(d["usbCut"]):
            usbpos = self.__generated["usb"]["location"]
            workplane.add(
                primitives.draw_rectangle(usbpos.x, usbpos.y, self.__usbWidth, self.__usbHeight, math.degrees(self.__handAngle))
            )
            workplane.add(
                primitives.draw_rectangle(usbpos.x, usbpos.y, self.__usbWidth+2.4, self.__usbHeight+4.8, math.degrees(self.__handAngle))
            )

        if bool(d["splitCut"]):
            splitpos = self.__generated["split"]["location"]
            workplane.add(
                primitives.draw_rectangle(splitpos.x, splitpos.y, self.__splitWidth, self.__splitHeight, math.degrees(self.__handAngle)-45)
            )
            workplane.add(
                primitives.draw_rectangle(splitpos.x, splitpos.y, self.__splitWidth+2.4, self.__splitHeight+4.8, math.degrees(self.__handAngle)-45)
            )

    def __render_leds(self, workplane, d):

        if bool(d["edgeLedCuts"]) or bool(d["keyLedCuts"]):

            if bool(d["locations"]):
                print("LED locations:")

            for led in self.__generated["leds"]:
                edgeLed = led[0]
                pos = led[2]
                degrees = led[4]

                if bool(d["edgeLedCuts"]) and edgeLed is True:
                    workplane.add(primitives.draw_rounded_rectangle(pos.x, pos.y, self.__ledSizeX, self.__ledSizeY, self.__ledCutFillet, degrees))

                if bool(d["keyLedCuts"]) and edgeLed is False:
                    workplane.add(primitives.draw_rounded_rectangle(pos.x, pos.y, self.__ledSizeX, self.__ledSizeY, self.__ledCutFillet, degrees))

                if bool(d["locations"]):
                    self.__circle_at_xy(workplane, pos, self.__locationFiducialSize)
                    print(f"    ({pos.x:8.3f}, {pos.y:8.3f}) @ {degrees:8.1f} degrees")

    def __render_kicad_script(self, d):

        if bool(d['kicadScript']):
            with open("kicad-placement.py", "w") as f:
                f.write(f'''\
from pcbnew import *
pcb = GetBoard()
''')

                for key in self.__generated["keys"]:
                    order = key[0]
                    keypos = key[2]
                    f.write(f'''
switch = pcb.FindModule("SW{order}")
if switch is not None:
    switch.SetPosition(wxPointMM({keypos.x:.3f},{-keypos.y:.3f}))
diode = pcb.FindModule("D{order}")
if diode is not None:
    diode.SetPosition(wxPointMM({(keypos.x-7.62):.3f},{-(keypos.y-(2.54*1.2)):.3f}))
    diode.SetOrientationDegrees(270)
''')

                for led in self.__generated["leds"]:
                    edgeLed = led[0]
                    order = led[1]
                    ledpos = led[2]
                    ledFlip = led[3]
                    rotation = led[4]
                    f.write(f'''
led = pcb.FindModule("LED{order}")
if led is not None:
    # Reset positioning
    if led.IsFlipped() is True:
        led.Flip(wxPointMM(0,0))
    led.SetOrientationDegrees(0)
    led.SetPosition(wxPointMM(0,0))

    # Apply flip if required
    if led.IsFlipped() is not {ledFlip}:
        led.Flip(wxPointMM(0,0))

    if {edgeLed} is True:
        # Fixup silkscreen
        for item in led.GraphicalItems():
            if isinstance(item, TEXTE_MODULE) and item.GetText() != "HOLE":
                item.SetPosition(wxPointMM({-3.9:.3f},{2:.3f}))
        # Fixup rotation
        led.SetOrientationDegrees({rotation:.3f})
    else:
        # Fixup rotation
        led.SetOrientationDegrees({180 if ledFlip else 0})
        # Fixup silkscreen
        for item in led.GraphicalItems():
            if isinstance(item, TEXTE_MODULE) and item.GetText() != "HOLE":
                item.SetPosition(wxPointMM({-3.9:.3f},{-2:.3f}))

    # Fixup positioning
    led.SetPosition(wxPointMM({ledpos.x:.3f},{-ledpos.y:.3f}))
''')

                order = 1
                for idx in range(0,len(self.__generated["drills"])):
                    drill = self.__generated["drills"][idx]
                    if drill["isDrill"]:
                        drillloc = drill["location"]
                        f.write(f'''
drill = pcb.FindModule("DRILL{order}")
if drill is not None:
    drill.SetPosition(wxPointMM({drillloc.x:.3f},{-drillloc.y:.3f}))
''')
                        order = order + 1

                lcdpos = self.__generated["lcd"]["location"]
                encpos = self.__generated["encoder"]["location"]
                hatpos = self.__generated["dpad"]["location"]
                rstpos = self.__generated["reset"]["location"]
                usbpos = self.__generated["usb"]["location"]
                splitpos = self.__generated["split"]["location"]
                f.write(f'''
lcd = pcb.FindModule("LCD1")
if lcd is not None:
    lcd.SetPosition(wxPointMM({lcdpos.x:.3f},{-lcdpos.y:.3f}))
    lcd.SetOrientationDegrees({math.degrees(self.__handAngle):.3f})

encoder = pcb.FindModule("ENC1")
if encoder is not None:
    encoder.SetPosition(wxPointMM({encpos.x:.3f},{-encpos.y:.3f}))

hat = pcb.FindModule("HAT1")
if hat is not None:
    hat.SetPosition(wxPointMM({hatpos.x:.3f},{-hatpos.y:.3f}))

reset = pcb.FindModule("RESET1")
if reset is not None:
    reset.SetPosition(wxPointMM({rstpos.x:.3f},{-rstpos.y:.3f}))

usb = pcb.FindModule("USB1")
if usb is not None:
    usb.SetPosition(wxPointMM({usbpos.x:.3f},{-usbpos.y:.3f}))
    usb.SetOrientationDegrees({180+math.degrees(self.__handAngle):.3f})

split = pcb.FindModule("SPLIT1")
if split is not None:
    split.SetPosition(wxPointMM({splitpos.x:.3f},{-splitpos.y:.3f}))
    split.SetOrientationDegrees({180-45+math.degrees(self.__handAngle):.3f})

Refresh()
''')

    def render(self, **kwargs):

        d = {
            "locations": False,
            "keyswitchCuts": False,
            "keyswitchOutlines": False,
            "drills": False,
            "drillPads": False,
            "outline": False,
            "spacer": False,
            "esdOutline": False,
            "lcdOutline": False,
            "lcdDrills": False,
            "lcdPlateCuts": False,
            "lcdSpacerCuts": False,
            "lcdDrillPads": False,
            "encoderCut": False,
            "encoderKnob": False,
            "dpadCut": False,
            "dpadHousing": False,
            "resetCut": False,
            "resetHousing": False,
            "edgeLedCuts": False,
            "keyLedCuts": False,
            "usbCut": False,
            "splitCut": False,
            "kicadScript": False,
        }

        d.update(kwargs)

        workplane = cq.Workplane("XY")
        self.__render_keys(workplane, d)
        self.__render_drills(workplane, d)
        if bool(d["outline"]):
            self.__render_outline(workplane, d, self.__outlineLocations, self.__outlineOffset)
        if bool(d["spacer"]):
            self.__render_outline(workplane, d, self.__spacerLocations, self.__spacerOffset)
        self.__render_lcd(workplane, d)
        self.__render_encoder(workplane, d)
        self.__render_dpad(workplane, d)
        self.__render_reset(workplane, d)
        self.__render_connector_cutouts(workplane, d)
        self.__render_leds(workplane, d)
        self.__render_kicad_script(d)
        return workplane.combine()