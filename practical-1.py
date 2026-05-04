# Practical 1: Implement depth first search algorithm and Breadth First Search algorithm and develop a recursive algorithm for searching all the vertices of a tree data structure. 

from collections import deque

GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": [], "E": [], "F": [], "G": []
}

START = "A"

def show_tree():
    print("""
        A
      /   \\
     B     C
    / \\   / \\
   D   E F   G
    """)

def dfs(start):
    stack, visited, order = [start], set(), []
    step = 1

    while stack:
        print(f"\nStep {step}")
        print("Stack:", stack)

        node = stack.pop()
        print("Pop →", node)

        if node not in visited:
            visited.add(node)
            order.append(node)

            print("Traversal:", " → ".join(order))

            for nb in reversed(GRAPH[node]):
                if nb not in visited:
                    stack.append(nb)
                    print("Push →", nb)

        step += 1

    return order

def bfs(start):
    queue, visited, order = deque([start]), {start}, []
    step = 1

    while queue:
        print(f"\nStep {step}")
        print("Queue:", list(queue))

        node = queue.popleft()
        print("Dequeue →", node)

        order.append(node)
        print("Traversal:", " → ".join(order))

        for nb in GRAPH[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                print("Enqueue →", nb)

        step += 1

    return order

def main():
    show_tree()

    while True:
        print("\n1. DFS\n2. BFS\n3. Exit")

        c = input("Choice: ")

        if c == "1":
            print("\nDFS Traversal")
            print("Final:", " → ".join(dfs(START)))

        elif c == "2":
            print("\nBFS Traversal")
            print("Final:", " → ".join(bfs(START)))

        elif c == "3":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()