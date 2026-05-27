from IPython.core.magic import magics_class, line_magic
from IPython.core.magics.pylab import PylabMagics
from IPython.core.error import UsageError
import matplotlib.pyplot as plt
import re
import shlex
import subprocess
import tempfile
import os

@magics_class
class KittyMatplotlib(PylabMagics):
    @line_magic
    def matplotlib_kitty(self, line):
        """Enable matplotlib with chafa passthrough for Kitty.

        Usage: %matplotlib_kitty [--size COLUMNSxROWS]
        Example: %matplotlib_kitty --size 100x40
        """
        size = None
        tokens = shlex.split(line)
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '--size':
                i += 1
                if i >= len(tokens):
                    raise UsageError('%matplotlib_kitty: --size requires a value like 100x40')
                size = tokens[i]
            elif token.startswith('--size='):
                size = token.split('=', 1)[1]
            else:
                raise UsageError(f'%matplotlib_kitty: unknown argument: {token}')
            i += 1

        if size and not re.fullmatch(r'\d+x\d+', size):
            raise UsageError('%matplotlib_kitty: --size must look like COLUMNSxROWS, e.g. 100x40')

        import matplotlib
        matplotlib.use('Agg')
        
        def kitty_show():
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                fname = f.name
            plt.savefig(fname)
            cmd = ['chafa', '--passthrough', 'tmux', '-f', 'kitty', '--align=center']
            if size:
                cmd.extend(['--size', size])
            cmd.append(fname)
            print('kitty-matplotlib:', shlex.join(cmd[:-1]), '<image>')
            subprocess.run(cmd)
            os.unlink(fname)
        
        plt.show = kitty_show
        size_msg = f" Display size: {size}." if size else ""
        print(f"Kitty matplotlib enabled from {__file__}.{size_msg} Use plt.show() to display.")

def load_ipython_extension(ipython):
    ipython.register_magics(KittyMatplotlib)
