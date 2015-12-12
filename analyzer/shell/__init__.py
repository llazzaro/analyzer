from subprocess import call

import platform

try:
    from analyzer import __version__ as ANALYZER_VERSION
except ImportError:
    ANALYZER_VERSION = ''

banner = '+-----------------------------------------------------------+\n'
banner += ' Analyzer '
banner += ANALYZER_VERSION
banner += ' [interactive shell] - http://llazzaro.github.io/analyzer\n'
banner += '+-----------------------------------------------------------+\n'
banner += '\n'
banner += 'Commands: \n'
banner += '\t"exit()" or press "Ctrl+ D" to exit the shell\n'
banner += '\t"clear()" to clear the shell screen\n'
banner += '\t"tutorial()" to begin the Analyzer interactive tutorial\n'
banner += '\t"example()" gives a list of examples you can run\n'
banner += '\t"chat()" will launch a web browser for the help\n'
banner += '\t"walkthrough()" will launch a web browser with a walkthrough\n'
banner += '\n'
banner += 'Usage:\n'
banner += '\tdot complete works to show library\n'
banner += '\tfor example: Image().save("/tmp/test.jpg") will dot complete\n'
banner += '\tjust by touching TAB after typing Image().\n'
banner += '\n'
banner += 'Documentation:\n'
banner += '\thelp(Stock), ?Stock, Stock?, or Stock()? all do the same\n'
banner += '\t"docs()" will launch webbrowser showing documentation'
banner += '\n'
exit_msg = '\n... [Exiting the Analyzer interactive shell] ...\n'


def setup_ipython():
    try:
        from traitlets.config.configurable import Config
        from IPython.frontend.terminal.embed import InteractiveShellEmbed

        cfg = Config()
        cfg.PromptManager.in_template = "Analyzer:\\$$> "
        cfg.PromptManager.out_template = "Analyzer:\\$$: "
        # ~ cfg.InteractiveShellEmbed.prompt_in1 = "Analyzer:\\#> "
        # ~ cfg.InteractiveShellEmbed.prompt_out="Analyzer:\\#: "
        scvShell = InteractiveShellEmbed(config=cfg, banner1=banner,
                                         exit_msg=exit_msg)
        # scvShell.define_magic("tutorial", magic_tutorial)
        # scvShell.define_magic("clear", magic_clear)
        # scvShell.define_magic("example", magic_examples)
        # scvShell.define_magic("forums", magic_forums)
        # scvShell.define_magic("walkthrough", magic_walkthrough)
        # scvShell.define_magic("docs", magic_docs)
    except ImportError:
        try:
            from IPython.Shell import IPShellEmbed

            argsv = ['-pi1', 'Analyzer:\\#>', '-pi2', '   .\\D.:', '-po',
                     'Analyzer:\\#>', '-nosep']
            scvShell = IPShellEmbed(argsv)
            scvShell.set_banner(banner)
            scvShell.set_exit_msg(exit_msg)
            # scvShell.IP.api.expose_magic("tutorial", magic_tutorial)
            # scvShell.IP.api.expose_magic("clear", magic_clear)
            # scvShell.IP.api.expose_magic("example", magic_examples)
            # scvShell.IP.api.expose_magic("forums", magic_forums)
            # scvShell.IP.api.expose_magic("walkthrough", magic_walkthrough)
            # scvShell.IP.api.expose_magic("docs", magic_docs)
        except ImportError:
            raise

    return scvShell()


def setup_bpython():
    import bpython
    # example = make_magic(magic_examples)
    # clear = make_magic(magic_clear)
    # docs = make_magic(magic_docs)
    # tutorial = make_magic(magic_tutorial)
    # walkthrough = make_magic(magic_walkthrough)
    # forums = make_magic(magic_forums)
    temp = locals().copy()
    temp.update(globals())
    return bpython.embed(locals_=temp, banner=banner)


def setup_plain():
    import code

    return code.interact(banner=banner, local=globals())


def run_shell(shell=None):
    shells = ['setup_ipython', 'setup_bpython', 'setup_plain']
    available_shells = [shell] if shell else shells

    for shell in available_shells:
        try:
            return globals()[shell]()
        except ImportError:
            pass
    raise ImportError


def shell_clear():
    if platform.system() == "Windows":
        return
    call("clear")
