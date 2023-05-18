import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # structure of self.domains: {Variable: words}
        for var in self.domains.keys():
            # looping through a copy because we're editing the original as we go
            for word in self.domains[var].copy():
                # check length consistency
                if len(word) != var.length:
                    self.domains[var].remove(word)
        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised=False
        # look for overlap between x and y
        overlap = self.crossword.overlaps[x, y] # overlap has indices of overlap in x and y
        if overlap is None:
            # no revision needed. x is arc consistent with y
            return revised
        
        # if there is overlap, we need to check for consistency
        # loop through x domain
        for x_word in self.domains[x].copy(): # copy because we may edit the domain
            x_overlap = x_word[overlap[0]] # letter of x that must overlap with y
            # loop through y domain
            consistent = False
            for y_word in self.domains[y]:
                y_overlap = y_word[overlap[1]]
                if x_overlap == y_overlap:
                    consistent = True
                    break
            if not consistent:
                revised = True
                self.domains[x].remove(x_word)
        
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # make a list of all arcs
            arcs = []
            for var in self.crossword.variables:
                for neighbor in self.crossword.neighbors(var):
                    arcs.append((var, neighbor))

        # now let's enforce arc consistency
        while len(arcs) > 0:
            
            x,y = arcs.pop(0)
            if self.revise(x, y):
                # this means we have had to make a change to the domain of arc[0]
                if len(self.domains[x]) == 0:
                    # this means we have an empty domain
                    return False # no possible solution as the domain of arc[0] is empty
                # we need to re-add to the que, the arcs that have arc[0] as a neighbor
                for neighbor in self.crossword.neighbors(x)-{y}:
                        arcs.append((neighbor, x))
        return True # no empty domains. consistency enforced


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        unassigned_vars = self.crossword.variables - set(assignment.keys())
        return True if len(unassigned_vars) == 0 else False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check for duplicate values
        words = assignment.values()
        if len(words) != len(set(words)):
            return False
        # check for length consistency
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
        # check for overlap consistency
        for var1, word1 in assignment.items():
            if word1 is None:
                continue
            for var2, word2 in assignment.items():
                if word2 is None:
                    continue
                if var1 == var2:
                    continue
                overlap = self.crossword.overlaps[var1, var2]
                if overlap is not None:
                    if word1[overlap[0]] != word2[overlap[1]]:
                        return False
        
        return True # no inconsistencies 
                        
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # get neighbours
        neighbors = self.crossword.neighbors(var)
        # get the unassigned neighbours
        neighbours = neighbors - set(assignment.keys())
        x_domain = self.domains[var].copy() #  copy because we may edit the domain
        num_constraints = dict()
        for word in x_domain:
            num_constraints[word] = 0
            for neighbor in neighbours:

                overlap = self.crossword.overlaps[var, neighbor]
                if overlap is not None:
                    for neighbor_word in self.domains[neighbor]:
                        if word[overlap[0]] != neighbor_word[overlap[1]]:
                            num_constraints[word] += 1
        # sort by num constraints
        x_domain = sorted(x_domain, key=lambda x: num_constraints[x])
        return x_domain


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = list(self.crossword.variables - set(assignment.keys()))
        var = min(unassigned_vars, key=lambda x: len(self.domains[x]))
        return var


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # this is a recursive function of sorts
        # base case
        if self.assignment_complete(assignment):
            return assignment
        # recursive case
        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var)

        return assignment


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
