# Add up and print the sum of the all of the minimum elements of each inner array:

minnie_mouse = [[8, 4], [90, -1, 3], [9, 62], [-7, -1, -56, -6], [201], [76, 18]]
# The expected output is given by:
# 4 + -1 + 9 + -56 + 201 + 18 = 175

inc = 0

for batch in minnie_mouse:
    inc += min(batch)

print(inc)