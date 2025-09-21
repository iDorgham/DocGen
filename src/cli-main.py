"""
Main CLI entry point for DocGen CLI.
"""

import click
from src.commands.generate import generate_command
from src.commands.project import project_command
from src.commands.validate import validate_command


@click.group()
@click.version_option()
def main():
    """DocGen CLI - Generate project documentation from specifications."""
    pass


# Add command groups
main.add_command(generate_command)
main.add_command(project_command)
main.add_command(validate_command)


if __name__ == '__main__':
    main()