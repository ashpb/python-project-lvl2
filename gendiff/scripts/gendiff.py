#!/usr/bin/env python3
"""Main program script"""

import argparse

def main():
    """Main"""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str, nargs=1)
    parser.add_argument('second_file', type=str, nargs=1)
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
