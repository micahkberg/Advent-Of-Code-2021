from load import openfile

today = "Day19"
lines = openfile(today+".txt")


# had to heavily copy some other folks functions in order to flail thru this

def distance(c1,c2):
    return sum([abs(c1[i] - c2[i]) for i in range(3)])


#class Scanner:
#    def __init__(self, name):
#        self.name = name
#        self.rel_coords = []
#        self.v_s = {}
#        self.n_hash_map = {}
#
#    def __repr__(self):
#        return f"Scanner {self.name} coords:\n{self.rel_coords[0]}\n{self.rel_coords[1]}\n{self.rel_coords[2]}\n..."
#
#    def add_coord(self, crd_string):
#        self.rel_coords.append(tuple(map(int, crd_string.split(","))))
#
#    def calc_relative_vectors(self):
#        for i in range(len(self.rel_coords)-1):
#            for j in range(i+1,len(self.rel_coords)):
#                p1 = self.rel_coords[i]
#                p2 = self.rel_coords[j]
#                self.v_s[(i, j)] = (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])

#    def calc_triangle_hashes(self):
#
#        for coord in self.rel_coords:
#            dists = {}
#            for other in self.rel_coords:
#                if other != coord:
#                    dists[distance(coord, other)] = other
#            d1, d2 = sorted(dists)[:2]
#            n1 = dists[d1]
#            n2 = dists[d2]
#            tri_hash = (d1+d2) * (distance(n1,n2))
#            self.n_hash_map[tri_hash] = (coord, n1, n2)

def calc_triangle_hashes(coords):
    hash_list = {}
    for coord in coords:
        dists = {}
        for other in coords:
            if other != coord:
                dists[distance(coord, other)] = other
        d1, d2 = sorted(dists)[:2]
        n1 = dists[d1]
        n2 = dists[d2]
        tri_hash = (d1+d2) * (distance(n1,n2))
        hash_list[tri_hash] = (coord, n1, n2)
    return hash_list


def find_matching_neighbors(base_map, scan_scan_maps):
    for field_hash in base_map.keys():
        for scanner, scanMap in scan_scan_maps:
            for scan_hash in scanMap.keys():
                if field_hash == scan_hash:
                    field_neighbor = base_map[scan_hash]
                    scan_neighbor = scanMap[scan_hash]
                    print("match found")
                    return (scanner, field_neighbor, scan_neighbor)
    print("no match found")


def orientation_calc(field_neighbor, match_neighbor):
    linear_transform = [None]*3
    facing = [None]*3
    rot_transform = [None]*3

    for pos in range(3):
        if linear_transform[pos]:
            continue
        for rotation in range(3):
            for flip in [-1,1]:
                offsets = set()
                for index in range(3):
                    offsets.add(field_neighbor[index][pos]-match_neighbor[index][rotation]*flip)
                if len(offsets) == 1:
                    linear_transform[pos] = offsets.pop()
                    facing[pos] = flip
                    rot_transform[pos] = rotation

    return (linear_transform, facing, rot_transform)


def reorient_coords(orientation, coords):
    lin_transform, flip_transform, rot_transform = orientation
    return [tuple([coord[rot_transform[index]] * flip_transform[index] + lin_transform[index] for index in range(3)])
            for coord in coords]

def calc_max_dist(coords):
    mx = 0
    for c1 in coords:
        for c2 in coords:
            if c1 != c2:
                dist = 0
                for i in range(3):
                    dist+=abs(c1[i]-c2[i])
                mx = dist if dist>mx else mx
    return mx

def assemble_base_field():
    # assemble our scanners
    scanners = []
    new_scanner = None
    for line in lines:
        if "scanner" in line:
            if new_scanner:
                scanners.append(new_scanner)
            new_scanner = []
        elif line:
            new_scanner.append(tuple(map(int, line.split(","))))
    scanners.append(new_scanner)

    base_field = set(scanners.pop(0))

    scanner_hash_maps = []
    for scanner in scanners:
        scanner_hash_maps.append((scanner, calc_triangle_hashes(scanner)))

    scanner_coords = []

    while len(scanner_hash_maps)>0:
        print(len(scanner_hash_maps))
        base_field_hashes = calc_triangle_hashes(base_field)
        matching_neighbors = find_matching_neighbors(base_field_hashes, scanner_hash_maps)
        scanner, field_neighbor, scan_neighbor = matching_neighbors
        for i in range(len(scanner_hash_maps)):
            if scanner_hash_maps[i][0] == scanner:
                scanner_hash_maps.pop(i)
                break
        orientation = orientation_calc(field_neighbor, scan_neighbor)
        scanner_coords.append(orientation[0])
        base_field.update(reorient_coords(orientation, scanner))
        print(f"current beacon count: {len(base_field)}")
    beacon_count = len(base_field)
    print(f"number of beacons {beacon_count}")
    max_dist = calc_max_dist(scanner_coords)
    print(f"max distance in ocean {max_dist}")


assemble_base_field()




