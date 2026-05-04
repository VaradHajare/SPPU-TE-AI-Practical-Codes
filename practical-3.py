# Practical 3: Implement Greedy search algorithm for Selection Sort 

def selection_sort_trace(arr):
    n = len(arr)

    for i in range(n):
        min_idx = i
        print(f"\nPass {i + 1}:")
        print(f"Starting with index {i}, current array: {arr}")

        for j in range(i + 1, n):
            print(f"Comparing arr[{j}] = {arr[j]} with current min = {arr[min_idx]}")
            if arr[j] < arr[min_idx]:
                min_idx = j
                print(f"--> New minimum found: {arr[min_idx]} at index {min_idx}")

        if min_idx != i:
            print(f"Swapping {arr[i]} and {arr[min_idx]}")
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        else:
            print("No swap needed")

        print(f"Array after pass {i + 1}: {arr}")

    return arr

try:
    user_input = input("Enter elements separated by space: ")
    arr = list(map(int, user_input.strip().split()))

    if not arr:
        print("Array is empty.")
    else:
        selection_sort_trace(arr)
        print("\nFinal Sorted Array:", arr)

except ValueError:
    print("Invalid input. Please enter integers only.")