def hill_climbing(a, start):
    while True:
        current = a[start]

        left = a[start - 1] if start > 0 else -1
        right = a[start + 1] if start + 1 < len(a) else -1

        if left > current and left >= right:
            start -= 1
        elif right > current:
            start += 1
        else:
            return start, current


a = list(map(int, input("Enter values: ").split(",")))

start = int(input("Enter the starting position: "))

pos, value = hill_climbing(a, start)

print("Peak position:", pos)
print("Peak value:", value)