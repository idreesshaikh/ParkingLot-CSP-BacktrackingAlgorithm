from functools import lru_cache
from itertools import product
from abc import ABC, abstractmethod


class Constraint(ABC):

    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        pass


class CSP:
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for var in self.variables:
            self.constraints[var] = []
            if var not in self.domains:
                raise LookupError(f"Every Var needs a Domain. {var}")

    def add_constraint(self, constraint):
        for var in constraint.variables:
            if var not in self.variables:
                raise LookupError(f"Variable in Constraint not in CSP. {var}")
            else:
                self.constraints[var].append(constraint)

    def consistent(self, var, assignment):
        for constraint in self.constraints[var]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment={}):
        if len(assignment) == len(self.variables):
            return assignment
        unassigned = [v for v in self.variables if v not in assignment]
        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None


class ParkingLot_Places:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        try:
            switch = {0: self.row, 1: self.column}
            result = switch[self.i]
            self.i += 1
            return result
        except KeyError:
            raise StopIteration


class ParkingLot:
    def __init__(self, LENGTH, WIDTH):
        L = int(LENGTH)
        W = int(WIDTH)
        self.grid = [[0 for _ in range(W)] for __ in range(L)]
        self.grid_length_size = L
        self.grid_width_size = W

    @lru_cache(maxsize=None)
    def generate_domain(self, PARKING_LENGTH, PARKING_WIDTH, recurse=True):
        domain = []
        LENGTH = self.grid_length_size
        WIDTH = self.grid_width_size

        for row in range(LENGTH):
            for column in range(WIDTH):
                columns = range(column, column + PARKING_WIDTH)
                rows = range(row, row + PARKING_LENGTH)

                if column + PARKING_WIDTH <= WIDTH:
                    #  Left to right
                    if row + PARKING_LENGTH <= LENGTH:
                        # Top to bottom
                        domain.append(
                            [
                                ParkingLot_Places(r, c)
                                for r, c in product(rows, columns)
                            ]
                        )
        if recurse:
            # Rotate boxes 90degrees
            return domain + self.generate_domain(
                PARKING_WIDTH, PARKING_LENGTH, recurse=False
            )
        return domain


class ParkingLotConstraint(Constraint):
    def __init__(self, places):
        super().__init__(places)
        self.place = places

    def satisfied(self, assignment):

        all_places = []
        for locations in assignment.values():
            for location in locations:
                all_places.append((location.row, location.column))
        return len(set(all_places)) == len(all_places)


def print_parkinglot(solution, LENGTH, WIDTH):
    PARK = [[0 for _ in range(int(WIDTH))] for __ in range(int(LENGTH))]
    number = 1
    for box, PARK_locations in solution.items():
        for P in PARK_locations:
            PARK[P.row][P.column] = number
        number = number + 1
    for row in PARK:
        print('\t'.join(str(n) for n in row))


def main():
    LL, WW = input().split()
    LENGTH = int(LL)
    No_Of_Vehicles = int(input().rstrip())
    nOv = int(No_Of_Vehicles)
    WIDTH = int(WW)
    PL = ParkingLot(LENGTH, WIDTH)
    boxes = []
    count = 1
    for i in range(0, nOv):
        count = str(count)
        READ = input().replace("\t", "")
        READ = READ+count
        boxes.append(READ)
        count = int(count)
        count += 1
    tuple(boxes)
    locations = {}
    for box in boxes:
        locations[box] = PL.generate_domain(int(box[0]),int(box[1]))
    csp = CSP(boxes, locations)
    csp.add_constraint(ParkingLotConstraint(boxes))
    solution = csp.backtracking_search()
    print_parkinglot(solution, LENGTH, WIDTH)


if __name__ == "__main__":
    main()
