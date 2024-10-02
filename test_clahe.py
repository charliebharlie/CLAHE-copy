from clahe import main

img_path = "uploads/star.png"
# Adjust the number of tiles here
num_horizontal_tiles = int(input("Enter the number of horizontal tiles: "))
num_vertical_tiles = int(input("Enter the number of vertical tiles: "))
padding_size = int(input("Enter the boundary size: "))
main.run_algorithms(img_path, num_horizontal_tiles, num_vertical_tiles, padding_size)
