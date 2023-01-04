# let's try to make this faster than normal degrees by using better data structures like dataframes
# And let's try to implement A* algorithm of search
import csv
import sys
import pandas as pd


from util_v2 import Node, StackFrontier, QueueFrontier, GBFS, Timer, TimerError

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


# TODO
# try greedy best first by choosing actor with most neighbours
# Result: GBFS doesnt give optimal solution (shortest degree of connection)
# need to try A*


def test_df_speed(directory):
    people = pd.read_csv(f"{directory}/people.csv")
    movies = pd.read_csv(f"{directory}/movies.csv")
    stars = pd.read_csv(f"{directory}/stars.csv")

    people["movies"] = [set() for i in range(len(people.index))]
    people.set_index("id", drop=True, inplace=True)
    movies["stars"] = [set() for i in range(len(movies.index))]
    movies.set_index("id", drop=True, inplace=True)

    for _, row in stars.iterrows():
        try:
            people.loc[row["person_id"]]["movies"].add(row["movie_id"])
            movies.loc[row["movie_id"]]["stars"].add(row["person_id"])
        except KeyError:
            pass

    person_ids = people.id
    person2movies = [
        set(stars[stars.person_id == person_id].movie_id) for person_id in people.id
    ]
    timer = Timer()

    person_id = 102
    neighbours = set()

    timer.start()
    movies_person_in = stars[stars.person_id == 102].movie_id
    [
        [
            neighbours.add((movie, person))
            for person in stars[stars.movie_id == movie].person_id
        ]
        for movie in movies_person_in
    ]
    timer.stop()
    print(len(list(neighbours)))

    return


def test_old_speed(directory):
    load_data(directory)

    timer = Timer()
    person_id = "102"
    timer.start()
    neighbours = neighbors_for_person(person_id)
    print(len(neighbours))
    timer.stop()


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    # people = pd.read_csv(f"{directory}/people.csv")
    # movies = pd.read_csv(f"{directory}/movies.csv")
    # stars = pd.read_csv(f"{directory}/stars.csv")

    # stars[stars.person_id == 102].movie_id

    # # now let's make some connective databases so it's easier to index
    # person_ids = people.id
    # movie_ids = movies.id
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set(),
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set(),
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # source = person_id_for_name(input("Name: "))
    source = person_id_for_name("pierce brosnan")
    if source is None:
        sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    target = person_id_for_name("noah centineo")
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    source_node = Node(
        person=source, movie=None, parent=None, neighbours=neighbors_for_person(source)
    )

    frontier = GBFS()
    frontier.add(source_node)
    success_path = None
    explored_persons = [source_node.person]
    while not frontier.empty():

        node = frontier.remove()
        explored_persons.append(node.person)

        # let's check if a neighbour is the target
        success_neighbour = is_target_neighbour(node.neighbours, target)
        if success_neighbour:
            success_path = node.get_path_to_target(success_neighbour)
            return success_path
        else:
            for neighbour in node.neighbours:
                person = neighbour[1]
                if person in explored_persons:
                    continue
                movie = neighbour[0]
                new_node = Node(person, movie, node, neighbors_for_person(person))
                frontier.add(new_node)

    return None


def is_target_neighbour(neighbours, target):
    """returns a tuple (movie, person) from the neighbours
    list if one of the neighbours has the target.
    Else returns None"""
    neighbours = list(neighbours)
    try:
        index = [x[1] for x in neighbours].index(target)
        neighbour = neighbours[index]

    except ValueError:
        neighbour = None

    return neighbour


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    # main()
    # test_old_speed("../degrees/large")
    test_df_speed("../degrees/large")
