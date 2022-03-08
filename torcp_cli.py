#  Usage:
#   python3 torcp.py -h
#
#  Example: hard link to a seperate dir
#    python3 torcp.py /home/ccf2012/Downloads/  -d=/home/ccf2012/emby/
#
#
import argparse
import torcp
import os


def loadArgs():
    parser = argparse.ArgumentParser(
        description=
        'torcp: a script hardlink media files and directories in Emby-happy naming and structs.'
    )
    parser.add_argument(
        'MEDIA_DIR',
        help='The directory contains TVs and Movies to be copied.')
    parser.add_argument('-d',
                        '--hd_path',
                        required=True,
                        help='the dest path to create Hard Link.')
    parser.add_argument('-e',
                        '--keep-ext',
                        help='keep files with these extention(\'srt,ass\').')
    parser.add_argument(
        '--tmdb-api-key',
        help=
        'Search API for the tmdb id, and gen dirname as Name (year)\{tmdbid=xxx\}'
    )
    parser.add_argument('--tmdb-lang',
                        default='zh-CN',
                        help='specify the TMDb language')
    parser.add_argument('--tv',
                        action='store_true',
                        help='specify the src directory is TV.')
    parser.add_argument('--movie',
                        action='store_true',
                        help='specify the src directory is Movie.')
    parser.add_argument('--dryrun',
                        action='store_true',
                        help='print message instead of real copy.')
    parser.add_argument('--single',
                        '-s',
                        action='store_true',
                        help='parse and copy one single folder.')
    parser.add_argument('--extract-bdmv',
                        action='store_true',
                        help='extract largest file in BDMV dir.')
    parser.add_argument('--full-bdmv',
                        action='store_true',
                        help='copy full BDMV dir and iso files.')
    parser.add_argument('--origin-name',
                        action='store_true',
                        help='keep origin file name.')
    parser.add_argument('--sleep',
                        type=int,
                        help='sleep x seconds after operation.')
    parser.add_argument('--move-run',
                        action='store_true',
                        help='WARN: REAL MOVE...with NO REGRET.')
    parser.add_argument('--emby-bracket',
                        action='store_true',
                        help='ex: Alone (2020) [tmdbid=509635]')
    parser.add_argument('--plex-bracket',
                        action='store_true',
                        help='ex: Alone (2020) {tmdb-509635}')

    ARGS = torcp.ARGSClass()
    API_ARGS = parser.parse_args()
    ARGS.src_path = os.path.expanduser(API_ARGS.MEDIA_DIR)
    ARGS.dst_path = os.path.expanduser(API_ARGS.hd_path)
    if API_ARGS.keep_ext:
        ARGS.keep_ext = API_ARGS.keep_ext
    if API_ARGS.tmdb_api_key:
        ARGS.tmdb_api_key = API_ARGS.tmdb_api_key
    if API_ARGS.tmdb_lang:
        ARGS.tmdb_lang = API_ARGS.tmdb_lang
    if API_ARGS.tv:
        ARGS.tv = True
    if API_ARGS.movie:
        ARGS.movie = True
    if API_ARGS.dryrun:
        ARGS.dryrun = True
    if API_ARGS.single:
        ARGS.single = True
    if API_ARGS.extract_bdmv:
        ARGS.extract_bdmv = True
    if API_ARGS.full_bdmv:
        ARGS.full_bdmv = True
    if API_ARGS.origin_name:
        ARGS.origin_name = True
    if API_ARGS.sleep:
        ARGS.sleep = API_ARGS.sleep
    if API_ARGS.move_run:
        ARGS.move_run = True
    if API_ARGS.emby_bracket:
        ARGS.emby_bracket = True
    if API_ARGS.plex_bracket:
        ARGS.plex_bracket = True

    return ARGS


def main():
    ARGS = loadArgs()
    t = torcp.TorCP(ARGS)
    t.torcpMain()


if __name__ == '__main__':
    main()
