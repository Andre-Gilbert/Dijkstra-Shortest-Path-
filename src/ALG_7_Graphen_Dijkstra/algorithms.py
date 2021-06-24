"""Contains the different variations of Dijktra's Algorithm.

It supports a lazy and an eager version of dijkstra's shortest path.
Before you run the algorithms, you need to create a graph, and pass
the graph as an argument.

Lazy implementation:
    Rather than updating existing key's value in O(n), the lazy version
    inserts key-value pairs in O(log(n)) even if they already exist in our
    priority queue.

Eager implementation:
    The eager version avoids inserting duplicate key-value pairs.
"""
import heapq
from queue import PriorityQueue

from data_structures import Edge, Graph, Vertex


def dijkstra_lazy(graph: Graph, start: Vertex, destination: Vertex) -> None:
    """Dijktra's shortest path with priority queue.

    Args:
        graph: A graph with edges and vertices.
        start: The start vertex.
        destination: The destination vertex.
    """
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set()
    came_from = {}

    costs = dict.fromkeys(graph.vertices, float('inf'))
    costs[start] = 0

    while not queue.empty():
        current = queue.get()[1]
        visited.add(current)

        for edge in current.adjacent_edges:
            if edge in visited:
                continue

            new_distance = costs[current] + edge.cost

            if new_distance < costs[edge.destination]:
                came_from[edge.destination] = current
                costs[edge.destination] = new_distance
                queue.put((costs[edge.destination], edge.destination))

    reconstruct_path(came_from, destination, costs)


def dijkstra_eager(graph: Graph, start: Vertex, destination: Vertex) -> None:
    """Dijktra's shortest path with heapqueue.

    Args:
        graph: A graph with edges and vertices.
        start: The start vertex.
        destination: The destination vertex.
    """
    heap = [(0, start)]
    heap_vertices = set()
    visited = set()
    came_from = {}

    costs = dict.fromkeys(graph.vertices, float('inf'))
    costs[start] = 0

    while heap:
        idx, current = heapq.heappop(heap)
        visited.add(current)

        if costs[current] < idx:
            continue

        for edge in current.adjacent_edges:
            if edge in visited:
                continue

            new_distance = costs[current] + edge.cost
            current_distance = costs[edge.destination]

            if new_distance < current_distance:
                came_from[edge.destination] = current
                costs[edge.destination] = new_distance

                if edge.destination not in heap_vertices:
                    heap_vertices.add(edge.destination)
                    heapq.heappush(heap, (costs[edge.destination], edge.destination))
                else:
                    # Since the heapq module doesn't support a decrease key method
                    # with O(1) lookup, we iterate over the heap in O(V) as a workaround.
                    """for idx, tup in enumerate(heap):
                        if tup[1] == edge.destination and temp_distance < tup[0]:
                            heap[idx] = (temp_distance, tup[1])

                            if idx > 0 and temp_distance < heap[idx - 1][0]:"""
                    #heapq.heapify(heap)

                    decrease_key(heap, edge, new_distance, current_distance)

    reconstruct_path(came_from, destination, costs)


def decrease_key(heap: list[tuple[int, Vertex]], edge: Edge, new_distance: int, current_distance: int) -> None:
    """Decrease a value of a vertex given a edge.
    
    Args:
        heap: An array of tuples containing the cost and vertex.
        edge: The current edge we're considering.
        new_distance: The new distance from vertex A to vertex B.
        current_distance: The current distance from vertex A to vertex B.
    """
    low, high = 0, len(heap) - 1

    while low <= high:
        mid = (low + high) // 2

        if heap[mid][1] == edge.destination:
            heap[mid] = (new_distance, edge.destination)
            break
        elif heap[mid][0] < current_distance:
            low = mid + 1
        else:
            high = mid - 1

    swim(heap, 0, mid)


def swim(heap: list[tuple[int, Vertex]], start_position: int, position: int) -> None:
    """Restore the heap invariant.
    
    Args:
        heap: An array of tuples containing the cost and vertex.
        start_position: The index of the root.
        position: The index of the updated tuple.
    """
    new_item = heap[position]

    while position > start_position:
        parent_position = (position - 1) >> 1
        parent = heap[parent_position]

        if new_item < parent:
            heap[position] = parent
            position = parent_position
            continue

        break

    heap[position] = new_item


def reconstruct_path(came_from: dict, current: Vertex, costs: dict) -> None:
    """Reconstruct the shortest path.

    Args:
        came_from: A dictionary containing the path to the destination.
        current: The current vertex we're considering.
        costs: A dictionary containing all of the costs.
    """
    print(f'Distance: {costs[current]}')
    path = current.name

    while current in came_from:
        current = came_from[current]
        path = f'{current.name} -> {path}'

    print(f'Shortest Path: {path}')
