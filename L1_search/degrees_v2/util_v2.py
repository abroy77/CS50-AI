import time
import copy
from bisect import bisect_left


class Node:
    def __init__(self, person, movie, parent, neighbours, cost=None):
        self.person = person
        self.parent = parent
        self.neighbours = neighbours
        self.connectivity = 1 / len(neighbours)
        self.movie = movie
        if cost is None:
            self.cost = self.parent.cost + 1
        else:
            self.cost = cost
        self.total_cost = self.cost + self.connectivity

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
        return

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


class AStar(QueueFrontier):
    def __init__(self):
        self.frontier = []
        self.frontier_cost = []
        return

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop(0)
            self.frontier = self.frontier[1:]

            self.frontier_cost.remove(node.total_cost)
            return node

    # def remove(self):
    #     if self.empty():
    #         raise Exception("empty frontier")

    #     node = min(self.frontier, key=lambda x: x.cost + x.connectivity)
    #     self.frontier.remove(node)
    #     return node

    def add(self, node):

        index = bisect_left(self.frontier_cost, node.total_cost)
        self.frontier.insert(index, node)
        self.frontier_cost.insert(index, node.total_cost)

        # insort_left(self.frontier, node, key=lambda x: x.cost + x.connectivity)
        return


import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.6f} seconds")
