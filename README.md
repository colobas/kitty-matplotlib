# kitty-matplotlib

An IPython extension that displays Matplotlib plots directly in Kitty-compatible terminals by rendering figures to PNG and passing them through `chafa`.

## How it works

The extension provides a `%matplotlib_kitty` magic. When enabled, it switches Matplotlib to the non-interactive `Agg` backend and replaces `plt.show()` with a function that:

1. Saves the current Matplotlib figure to a temporary PNG file.
2. Runs `chafa` with Kitty passthrough support to display the image in the terminal.
3. Deletes the temporary file.

## Requirements

Python package dependencies are installed automatically:

- `matplotlib`
- `ipython`

You also need these command-line tools / terminal capabilities installed separately:

- `chafa`
- A terminal supporting Kitty graphics protocol, such as Kitty
- `tmux`, if using the provided `chafa --passthrough tmux` invocation

## Usage

Install the package, then in IPython:

```python
%load_ext kitty_matplotlib
%matplotlib_kitty

import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```
