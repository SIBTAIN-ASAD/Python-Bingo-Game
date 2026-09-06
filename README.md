# Python Bingo

A console Bingo game for one to five players. Each player receives a 5×5 card
containing 25 distinct items. Cards may share items with other players.

## Play

```sh
python3 bingo.py
```

The entry point downloads its item list from the URL configured in `main()`, so
normal startup requires network access and an available source with at least 25
distinct items. Python's standard library is sufficient; no packages are required.

Choose a winning mode:

- **Full card:** all 25 squares are marked.
- **Single line:** a complete row, column, or diagonal is marked.
- **Four corners:** the four corner squares are marked.

During a game, enter `P` to draw an item or `S` to show all cards. Each item is drawn
at most once. All players who satisfy the selected winning rule on the same draw
are announced as winners.

For an offline game, supply your own item list from Python:

```python
from bingo import Game
Game([str(number) for number in range(1, 76)])
```

## Tests

```sh
python3 -m unittest -v
```

The tests run offline and cover unique cards, insufficient item pools, every
winning line, four-corner wins, exhausted draws, and a complete full-card game.
