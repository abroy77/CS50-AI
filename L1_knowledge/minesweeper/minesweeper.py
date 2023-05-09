import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def __repr__(self):
        return f"Sentence({self.cells} , {self.count})"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells:
            return
        self.cells.remove(cell)
        self.count-=1
        return
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell not in self.cells:
            return
        self.cells.remove(cell)
        return

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        if cell in self.mines:
            return
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)


    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        if cell in self.safes:
            return
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def get_surrounding_cells(self, cell, count):
        moves = list(itertools.product([-1,0,1], repeat=2))
        add_move = lambda position,move: tuple(map(lambda i,j:i+j, position, move))
        surrounding_cells = {add_move(cell,move) for move in moves}
        # remove the cell itself
        surrounding_cells.remove(cell)
        # remove cells out of bounds
        surrounding_cells = {x for x in surrounding_cells if (0 <= x[0] < self.height) and (0<= x[1] < self.width)}
        # how many KNOWN mines are in the surrounding cells
        num_known_mines_surrounding = len(surrounding_cells  & self.mines)
        # remove cells that are in self.mines or self.safes
        surrounding_cells = surrounding_cells - self.mines
        
        # remove that number from the count
        updated_count = count-num_known_mines_surrounding
        surrounding_cells = surrounding_cells - self.safes
        if (2,7) in surrounding_cells:
            print('bro')
        
        return surrounding_cells, updated_count


    def subset_inference(self):
        new_sentences = []
        for s1, s2 in itertools.permutations(self.knowledge, 2):
            if s1.cells < s2.cells:
                new_sentence = Sentence(s2.cells-s1.cells, s2.count - s1.count)
                if new_sentence not in self.knowledge and new_sentence:
                    new_sentences.append(new_sentence)
            else:
                continue
        return new_sentences


    def update_knowledge(self):

        while True: # loop for updating sentences based on the inference rule
            new_sentences=[]
                      
            while True: # loop for infering new mines and new safes from existing sentences
                new_safes = set()
                new_mines = set()
                # let's find the new mines and new safes from inference
                for sentence in self.knowledge:
                    new_mines |= sentence.known_mines()
                    new_safes |= sentence.known_safes()
                
                # mark the new safes
                new_safes = new_safes - self.safes
                {self.mark_safe(cell) for cell in new_safes} 

                # mark the new mines
                new_mines = new_mines - self.mines 
                {self.mark_mine(cell) for cell in new_mines}
                    

                # let's delete sentences from knowledge that have no cells in the sentence
                self.knowledge = [sentence for sentence in self.knowledge if sentence.cells]     
                if len(new_mines | new_safes) == 0: break

            
            
            new_sentences.extend(self.subset_inference())
            self.knowledge.extend(new_sentences)
            
            if len(new_sentences) ==0 : break
        
        return


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1: mark cell as move made
        self.moves_made.add(cell)

        # 2: mark the cell as safe
        self.mark_safe(cell)

        # 3: add new sentence to knowledge base
        # we need to get the set of surrounding cells
        surrounding_cells, updated_count = self.get_surrounding_cells(cell, count)
        if len(surrounding_cells) > 0: 
            new_sentence = Sentence(surrounding_cells, updated_count)
            self.knowledge.append(new_sentence)

        # recursively update until there's no new inferences
        self.update_knowledge()
        return



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves = self.safes - self.moves_made
        if len(possible_moves)==0:
            return None
        move = random.sample(possible_moves, 1)
        return move[0]



    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set(itertools.product(range(self.height), range(self.width), repeat = 1))
        possible_moves = all_moves - self.moves_made - self.mines
        if len(possible_moves)==0:
            return None

        move = random.sample(possible_moves, 1)
        return move[0]

