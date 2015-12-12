import logging
from analyzer import init_logging
from analyzer.shell import shell_clear, run_shell


def main():
    init_logging(None, level='debug')
    shell_clear()
    run_shell()
