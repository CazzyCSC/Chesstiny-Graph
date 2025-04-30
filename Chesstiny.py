import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# === Load the TSV ===
df = pd.read_csv("data-verified.tsv", sep="\t")
print(f"✅ Loaded {len(df)} boards.")

# === Settings ===
tile_size = 8
tile_px = 24  # keep smaller to fit more boards
board_px = tile_px * tile_size
df_sorted = df.sort_values(by="frequency").reset_index(drop=True)

# === Grid layout ===
grid_width = 20
grid_height = int(np.ceil(len(df_sorted) / grid_width))
canvas_width = grid_width * board_px
canvas_height = grid_height * board_px

# === Fill colors ===
fill_rgb_map = {
    'darkGray': (0.3, 0.3, 0.3), 'lightRed': (0.9, 0.3, 0.3), 'darkRed': (0.6, 0.1, 0.1),
    'lightGray': (0.8, 0.8, 0.8), 'white': (1.0, 1.0, 1.0), 'black': (0.0, 0.0, 0.0),
    'blue': (0.3, 0.3, 0.8), 'pink': (1.0, 0.7, 0.8), 'green': (0.3, 0.8, 0.3),
    'orange': (0.95, 0.6, 0.2), 'yellow': (1.0, 1.0, 0.6), 'purple': (0.6, 0.4, 0.8)
}

# === Corrected Unicode mapping (outlined = black) ===
unicode_pieces = {
    'Pw': '♟', 'Pb': '♙',
    'Rw': '♜', 'Rb': '♖',
    'Nw': '♞', 'Nb': '♘',
    'Bw': '♝', 'Bb': '♗',
    'Qw': '♛', 'Qb': '♕',
    'Kw': '♚', 'Kb': '♔'
}

def parse_board_string(board_str):
    cells = board_str.split(",")
    return np.array(cells).reshape((8, 8)) if len(cells) == 64 else None

# === Setup canvas ===
fig, ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100), dpi=100)
ax.set_xlim(0, canvas_width)
ax.set_ylim(0, canvas_height)
ax.set_facecolor("white")
ax.axis("off")

# === Draw boards ===
for idx, row in df_sorted.iterrows():
    board = parse_board_string(row["board"])
    if board is None:
        print(f"⚠️ Skipping malformed board at row {idx}")
        continue

    fill_name = str(row.get("fill", "white"))
    fill_color = fill_rgb_map.get(fill_name, (1.0, 1.0, 1.0))
    if fill_name not in fill_rgb_map:
        print(f"⚠️ Unknown fill '{fill_name}' at row {idx}, defaulting to white")

    row_idx = idx // grid_width
    col_idx = idx % grid_width
    x0 = col_idx * board_px
    y0 = canvas_height - (row_idx + 1) * board_px

    for y in range(8):
        for x in range(8):
            piece = board[y, x]
            rect = patches.Rectangle(
                (x0 + x * tile_px, y0 + y * tile_px),
                tile_px, tile_px,
                facecolor=fill_color,
                edgecolor='black', linewidth=0.5
            )
            ax.add_patch(rect)

            if piece:
                symbol = unicode_pieces.get(piece, '?')
                brightness = 0.299 * fill_color[0] + 0.587 * fill_color[1] + 0.114 * fill_color[2]
                text_color = 'white' if brightness < 0.5 else 'black'
                ax.text(
                    x0 + x * tile_px + tile_px / 2,
                    y0 + y * tile_px + tile_px / 2,
                    symbol,
                    fontsize=tile_px * 0.6,
                    ha='center', va='center',
                    color=text_color
                )

# === Save the result ===
fig.savefig("destiny2_chess_mosaic_colored.png", dpi=100, bbox_inches='tight')
fig.savefig("destiny2_chess_mosaic_colored.pdf", bbox_inches='tight')
print("✅ Saved final output to PNG and PDF.")
