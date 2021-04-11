import cadquery as cq
import math

def mm2m(v):
    return v / 1000.0

def draw_rectangle(x, y, w, h, rot=None):
    obj = (
            cq.Workplane("XY")
                .center(mm2m(x), mm2m(y))
                .moveTo(-mm2m(w / 2.0), mm2m(h / 2.0))
                .line(mm2m(w), 0)
                .line(0, -mm2m(h))
                .line(-mm2m(w), 0)
                .line(0, mm2m(h))
                .close()
            )

    if rot:
        obj = obj.rotate((mm2m(x), mm2m(y), 0), (mm2m(x), mm2m(y), 1), rot)

    return obj

def draw_rounded_rectangle(x, y, w, h, r, rot=None):
    f = mm2m(r)

    if f == 0:
        return draw_rectangle(x, y, w, h)

    tllX = mm2m(-w / 2.0)
    tllY = mm2m(+h / 2.0 - r)
    tltX = mm2m(-w / 2.0 + r)
    tltY = mm2m(+h / 2.0)

    trrX = mm2m(+w / 2.0)
    trrY = mm2m(+h / 2.0 - r)
    trtX = mm2m(+w / 2.0 - r)
    trtY = mm2m(+h / 2.0)

    brrX = mm2m(+w / 2.0)
    brrY = mm2m(-h / 2.0 + r)
    brbX = mm2m(+w / 2.0 - r)
    brbY = mm2m(-h / 2.0)

    bllX = mm2m(-w / 2.0)
    bllY = mm2m(-h / 2.0 + r)
    blbX = mm2m(-w / 2.0 + r)
    blbY = mm2m(-h / 2.0)

    obj = (
        cq.Workplane("XY")
            .center(mm2m(x), mm2m(y))
            .moveTo(tllX, tllY)
            .radiusArc((tltX, tltY), f)
            .lineTo(trtX, trtY)
            .radiusArc((trrX, trrY), f)
            .lineTo(brrX, brrY)
            .radiusArc((brbX, brbY), f)
            .lineTo(blbX, blbY)
            .radiusArc((bllX, bllY), f)
            .close()
    )

    if rot:
        obj = obj.rotate((mm2m(x), mm2m(y), 0), (mm2m(x), mm2m(y), 1), rot)

    return obj

def draw_circle(x, y, r):
    return (
        cq.Workplane("XY")
            .moveTo(mm2m(x), mm2m(y))
            .circle(mm2m(r))
        )

class point:

    def __init__(self, x, y):

        self.__x = x
        self.__y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

class edge:

    def __init__(self, xy_from, xy_to):

        self.__from = xy_from
        self.__to = xy_to
        self.__angle = math.atan2(self.y1 - self.y0, self.x1 - self.x0)

    @property
    def length(self):
        return math.sqrt((self.x1-self.x0)**2 + (self.y1-self.y0)**2)

    @property
    def x0(self):
        return self.__from.x

    @property
    def y0(self):
        return self.__from.y

    @property
    def x1(self):
        return self.__to.x

    @property
    def y1(self):
        return self.__to.y

    @property
    def radians(self):
        return self.__angle

    @property
    def degrees(self):
        return math.degrees(self.radians)

    def __repr__(self):
        return f"<{self.__from}->{self.__to}>"

    def offset(self, distance=0):

        new_from = point(
            self.x0 + math.sin(self.radians)*distance,
            self.y0 - math.cos(self.radians)*distance
        )

        new_to = point(
            self.x1 + math.sin(self.radians)*distance,
            self.y1 - math.cos(self.radians)*distance
        )

        return edge(new_from, new_to)

    def intersection_point(self, other):
        xdiff = (self.x1 - self.x0, other.x1 - other.x0)
        ydiff = (self.y1 - self.y0, other.y1 - other.y0)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           raise Exception('lines do not intersect')

        d = (det((self.x1,self.y1),(self.x0,self.y0)), det((other.x1,other.y1),(other.x0,other.y0)))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        return point(x, y)

    def perpendicular(self, other):
        # Works out the perpendicular intersection point of this line a line drawn from the specified point
        xdiff = self.x1 - self.x0
        ydiff = self.y1 - self.y0
        mag = math.sqrt(xdiff*xdiff + ydiff*ydiff)
        xdiff = xdiff / mag
        ydiff = ydiff / mag
        l = (xdiff * (other.x - self.x0)) + (ydiff * (other.y - self.y0))
        return point((xdiff * l) + self.x0, (ydiff * l) + self.y0)

    def lerp(self, ratio=0.5):
        x = self.x0 + (ratio * (self.x1 - self.x0))
        y = self.y0 + (ratio * (self.y1 - self.y0))
        return point(x, y)

class arc:

    def __init__(self, edge_ab, edge_bc, offset, is_convex):

        self.__edge_ab = edge_ab.offset(offset)
        self.__edge_bc = edge_bc.offset(offset)
        self.__intersection = edge_ab.intersection_point(edge_bc)
        if is_convex:
            self.__centre = self.intersection
        else:
            self.__centre = edge_ab.offset(2*offset).intersection_point(edge_bc.offset(2*offset))

    @property
    def intersection(self):
        return self.__intersection

    @property
    def centre(self):
        return self.__centre

    @property
    def chord_length(self):
        return math.sqrt(math.pow(self.end.x-self.start.x,2)+pow(self.end.y-self.start.y,2))

    @property
    def start(self):
        return self.__edge_ab.perpendicular(self.centre)

    @property
    def end(self):
        return self.__edge_bc.perpendicular(self.centre)
