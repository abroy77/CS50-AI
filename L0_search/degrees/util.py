class Node:
    def __init__(self, person, movie, parent):
        self.person = person
        self.parent = parent
        # self.neighbours = neighbours
        self.movie = movie

    def get_path_to_target(self, neighbour=None):

        if neighbour:
            path = [neighbour]
        else:
            path = []
        node = self
        while node.parent:
            path.append((node.movie, node.person))
            node = node.parent
        path.reverse()
        return path


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, person):
        return any(node.person == person for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class GBFS(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = max(self.frontier, key=lambda x: len(x.neighbours))
        self.frontier.remove(node)
        return node