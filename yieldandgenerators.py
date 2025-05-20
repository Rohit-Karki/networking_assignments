# Have you ever had to work with a dataset so large that it overwhelmed your machine’s memory?
# Or maybe you have a complex function that needs to maintain an internal state every time it’s called,
# but the function is too small to justify creating its own class. In these cases and more, generators
# and the Python yield statement are here to help.

# Handle Large files
def csv_reader(file_name):
    for row in open(file_name, "r"):
        yield row


csv_gen = csv_reader('./techcrunch.csv')
print(f"{csv_gen}")
row_count = 0

for row in csv_gen:
    row_count += 1

print(f"Row count is {row_count}")
