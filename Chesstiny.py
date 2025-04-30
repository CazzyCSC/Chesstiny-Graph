import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Load the data
df = pd.read_csv("data-verified.tsv", sep="\t")

# Settings
tile_size = 8
tile_px = 48
board_px = tile_px * tile_size
num_tiles = len(df)
grid_size = int(np.ceil(np.sqrt(num_tiles)))
canvas_px = board_px * grid_size

# Mappings
color_map = {
    'darkGray': 0.2, 'lightRed': 0.6, 'darkRed': 0.4, 'lightGray': 0.8,
    'white': 1.0, 'black': 0.0, 'blue': 0.5, 'pink': 0.7,
    'green': 0.3, 'orange': 0.55, 'yellow': 0.9, 'purple': 0.45,
}

piece_value_map = {
    '': 1.0, 'Pw': 0.9, 'Pb': 0.1, 'Rw': 0.85, 'Rb': 0.15,
    'Nw': 0.8, 'Nb': 0.2, 'Bw': 0.75, 'Bb': 0.25,
    'Qw': 0.7, 'Qb': 0.3, 'Kw': 0.65, 'Kb': 0.35
}

def parse_board_string(board_str):
    return np.array(board_str.split(",")).reshape((8, 8))

# Sort by frequency
df_sorted = df.sort_values(by="frequency").reset_index(drop=True)

# Create the plot
fig, ax = plt.subplots(figsize=(16, 16))
ax.set_xlim(0, canvas_px)
ax.set_ylim(0, canvas_px)
ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor('white')

# Draw each tile
for idx, row in df_sorted.iterrows():
    board = parse_board_string(row["board"])
    fill_val = color_map.get(row["fill"], 1.0)
    row_idx = idx // grid_size
    col_idx = idx % grid_size
    x_offset = col_idx * board_px
    y_offset = canvas_px - (row_idx + 1) * board_px

    for y in range(8):
        for x in range(8):
            piece = board[y, x]
            color_val = str(0.6 * fill_val + 0.4 * piece_value_map.get(piece, 1.0))
            rect = patches.Rectangle(
                (x_offset + x * tile_px, y_offset + y * tile_px),
                tile_px, tile_px,
                facecolor=color_val, edgecolor='black', linewidth=0.5
            )
            ax.add_patch(rect)
            if piece:
                ax.text(
                    x_offset + x * tile_px + tile_px / 2,
                    y_offset + y * tile_px + tile_px / 2,
                    piece,
                    fontsize=5, ha='center', va='center',
                    color='red' if 'w' in piece else 'black'
                )

# Save files
output_png = "destiny2_chess_mosaic.png"
output_pdf = "destiny2_chess_mosaic.pdf"
fig.savefig(output_png, dpi=300, bbox_inches='tight')
fig.savefig(output_pdf, bbox_inches='tight')
plt.close(fig)

print(f"Saved:\n  PNG: {output_png}\n  PDF: {output_pdf}")