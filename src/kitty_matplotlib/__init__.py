from IPython.core.magic import magics_class, line_magic
from IPython.core.magics.pylab import PylabMagics
import matplotlib.pyplot as plt
import subprocess
import tempfile
import os

@magics_class
class KittyMatplotlib(PylabMagics):
    @line_magic
    def matplotlib_kitty(self, line):
        """Enable matplotlib with chafa passthrough for Kitty"""
        import matplotlib
        matplotlib.use('Agg')
        
        original_show = plt.show
        
        def kitty_show():
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                fname = f.name
            plt.savefig(fname)
            subprocess.run(['chafa', '--passthrough', 'tmux', '-f', 'kitty', '--align=center', fname])
            os.unlink(fname)
        
        plt.show = kitty_show
        print("Kitty matplotlib enabled. Use plt.show() to display.")

def load_ipython_extension(ipython):
    ipython.register_magics(KittyMatplotlib)
