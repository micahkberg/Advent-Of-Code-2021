from load import openfile

today = "Day13"
lines = openfile(today+".txt")

init_points = []
init_folds = []
pointing = True
for line in lines:
    if pointing:
        if line:
            init_points.append(list(map(int, line.split(","))))
        else:
            pointing = False
    else:
        init_folds.append(line)


class paper:
    def __init__(self, points, folds):
        self.points = points
        self.folds_list = folds
        for fold in self.folds_list:
            self.fold(fold)

    def __repr__(self):
        out = ""
        for j in range(10):
            out_line = ""
            for i in range(60):
                if [i,j] in self.points:
                    out_line += "#"
                else:
                    out_line += "."
            out += out_line + "\n"

        return out

    def fold(self, next_fold):
        direction = next_fold.split(" ")[2][0]
        position = int(next_fold.split(" ")[2][2:])
        new_points = []
        old_points = []
        for point in self.points:
            new_coord = None
            if direction == "x" and point[0]>position:
                new_coord = [position-abs(point[0]-position),point[1]]
                old_points.append(point)
            elif direction == "y" and point[1]>position:
                new_coord = [point[0],position-abs(point[1]-position)]
                old_points.append(point)
            if new_coord and new_coord not in self.points:
                new_points.append(new_coord)
        for point in new_points:
            self.points.append(point)
        for point in old_points:
            self.points.remove(point)


new_page = paper(init_points, init_folds)
print(new_page)
