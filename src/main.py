"""
Entry point for running docgen as a module.

This allows running docgen with: python -m docgen
"""

from .cli import main

if __name__ == "__main__":
    main()
