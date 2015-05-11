#!/usr/bin/env python

# Indicar Landsat Geoprocessing Tools
#
#
# Author: Hex Gis
# Contributor: willemarcel
#
# License: GPLv3

from __future__ import print_function
import argparse
import textwrap
import sys

from .process import Process


DESCRIPTION = """indicar-tools is the software made by the Indicar Project
to process Landsat 8 imagery.

    Commands:
        Process: creates RGB, NDVI and a raster change detection file containing
        the losses in the vegetation of the imagery in comparison with the NDVI
        of the same scene generated 16 days ago.
        $ indicar process path

        If you want the change detection as a vector file instead of a raster,
        use the --polygonize parameter:
        $ indicar process path --polygonize

    Options:
        RGB: creates only a RGB image, using the bands 6, 5 and 4. This composition
        gives emphasys to the areas without vegetation.
        $ indicar process --rgb path

        NDVI: creates only a NDVI image. Where there are clouds or cirrus,
        the pixel value will be 0.
        $ indicar process --ndvi path

        Set Directory: by default, indicar-tools will save the processed images
        in a folder named 'landsat' on your home dir, but you can set an
        alternative directory using the --dir parameter.
        $ indicar process path --dir directory_path
"""


def args_options():
    parser = argparse.ArgumentParser(prog='indicar',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description=textwrap.dedent(DESCRIPTION))
    subparsers = parser.add_subparsers(help='Process Utility',
                                       dest='subs')
    parser_process = subparsers.add_parser('process',
                                           help='Process Landsat 8 imagery')
    parser_process.add_argument('path',
                                help="""Path to the compressed LC8 file or to
                                a folder containing the uncompressed files.""")
    parser_process.add_argument('--rgb', action='store_true',
                                help='Create only a RGB from the imagery')
    parser_process.add_argument('--ndvi', action='store_true',
                                help='Create only a NDVI from the imagery')
    parser_process.add_argument('--polygonize', action='store_true',
                                help="""When calculating change_detection,
                                polygonize the result generating a geojson file,
                                instead of a TIF image.""")
    parser_process.add_argument('--dir',
                                help='Directory where the processed images will be stored')

    return parser


def main(args):
    """Main function - launches the program"""
    if args:
        if args.subs == 'process':
            if args.dir:
                p = Process(args.path, args.dir)
            else:
                p = Process(args.path)
            if args.rgb:
                p.make_rgb()
            elif args.ndvi:
                p.make_ndvi()
            else:
                p.full(args.polygonize)


def exit(message, code=0):
    print(message)
    sys.exit(code)


def __main__():

    global parser
    parser = args_options()
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    __main__()
