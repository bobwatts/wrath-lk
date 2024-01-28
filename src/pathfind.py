from collections import deque
import heapq
import json


def find_nearest_player(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            # print(node, end=" ")
            visited.add(node.name)
            json_file_path = "./data/herodata.json"
            with open(json_file_path, "r") as file:
                heroes = json.load(file)
            for x in heroes:
                if heroes[x]["symbol"] in node.contents:
                    return node.name
            temp = []
            for neighbor in node.neighbors:
                if neighbor not in visited:
                    for l in graph:
                        if l.name == neighbor:
                            temp.append(l)
                            break
            queue.extend(temp)


def find_all_players(graph):
    h = []
    for l in graph:
        json_file_path = "./data/herodata.json"
        with open(json_file_path, "r") as file:
            heroes = json.load(file)
        for x in heroes:
            if heroes[x]["symbol"] in l.contents:
                h.append(l.name)
    return h


def dijkstra(graph, start, end):
    # print(str(start.name) + " to " + str(end.name))
    distances = {node.name: float("infinity") for node in graph}
    predecessors = {node.name: None for node in graph}
    distances[start.name] = 0

    priority_queue = [(0, start.name)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for g in graph:
            if g.name == current_node:
                t = g
        for neighbor in t.neighbors:
            distance = current_distance + 1

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current_node = end.name
    while current_node is not None:
        path.insert(0, current_node)
        # print(current_node)
        if predecessors[current_node] != None:
            current_node = predecessors[current_node]
        else:
            break
    return path, distances[end.name]


def find_all_locations_in_radius(current_location_ind, locations, radius):
    visited = set()
    result = []

    queue = deque([(locations[current_location_ind].name, 0)])
    visited.add(locations[current_location_ind].name)

    while queue:
        current_node_name, current_distance = queue.popleft()
        result.append(current_node_name)

        for l in range(len(locations)):
            if locations[l].name == current_node_name:
                current_node = locations[l]

        for neighbor in current_node.neighbors:
            if neighbor not in visited and current_distance + 1 <= radius:
                visited.add(neighbor)
                queue.append((neighbor, current_distance + 1))

    result.pop(0)
    return result
