from flask import Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import reqparse
import os
import torcp
from key import APIKEY

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'torcp':
        return APIKEY
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/torcpapi', methods=['POST'])
@auth.login_required
def loadApiArgs():
    parser = reqparse.RequestParser()
    parser.add_argument(
        'src_path', help='The directory contains TVs and Movies to be copied.')
    parser.add_argument('dst_path',
                        required=True,
                        help='the dest path to create Hard Link.')
    parser.add_argument('keep-ext',
                        help='keep files with these extention(\'srt,ass\').')
    parser.add_argument(
        'tmdb-api-key',
        help=
        'Search API for the tmdb id, and gen dirname as Name (year)\{tmdbid=xxx\}'
    )
    parser.add_argument('tmdb-lang',
                        default='zh-CN',
                        help='specify the TMDb language')
    parser.add_argument('tv',
                        help='specify the src directory is TV.')
    parser.add_argument('movie',
                        help='specify the src directory is Movie.')
    parser.add_argument('dryrun',
                        help='print message instead of real copy.')
    parser.add_argument('single', help='parse and copy one single folder.')
    parser.add_argument('extract-bdmv',
                        help='extract largest file in BDMV dir.')
    parser.add_argument('full-bdmv', help='copy full BDMV dir and iso files.')
    parser.add_argument('origin-name', help='keep origin file name.')
    parser.add_argument('sleep',
                        type=int,
                        help='sleep x seconds after operation.')
    parser.add_argument('move-run', help='WARN: REAL MOVE...with NO REGRET.')
    parser.add_argument('emby-bracket',
                        help='ex: Alone (2020) [tmdbid=509635]')
    parser.add_argument('plex-bracket', help='ex: Alone (2020) {tmdb-509635}')

    ARGS = torcp.ARGSClass()
    API_ARGS = parser.parse_args()
    ARGS.src_path = os.path.expanduser(API_ARGS['src_path'])
    ARGS.dst_path = API_ARGS['dst_path']
    if API_ARGS['keep-ext']:
        ARGS.keep_ext = API_ARGS['keep-ext']
    if API_ARGS['tmdb-api-key']:
        ARGS.tmdb_api_key = API_ARGS['tmdb-api-key']
    if API_ARGS['tmdb-lang']:
        ARGS.tmdb_lang = API_ARGS['tmdb-lang']
    if API_ARGS['tv']:
        ARGS.tv = True
    if API_ARGS['movie']:
        ARGS.movie = True
    if API_ARGS['dryrun']:
        ARGS.dryrun = True
    if API_ARGS['single']:
        ARGS.single = True
    if API_ARGS['extract-bdmv']:
        ARGS.extract_bdmv = True
    if API_ARGS['full-bdmv']:
        ARGS.full_bdmv = True
    if API_ARGS['origin-name']:
        ARGS.origin_name = True
    if API_ARGS['sleep']:
        ARGS.sleep = API_ARGS['sleep']
    if API_ARGS['move-run']:
        ARGS.move_run = True
    if API_ARGS['emby-bracket']:
        ARGS.emby_bracket = True
    if API_ARGS['plex-bracket']:
        ARGS.plex_bracket = True

    if ARGS.single:
        t = torcp.TorCP(ARGS)
        t.torcpMain()
        return {"tmdbid": t.tmdbid, "libpath": t.libpath}
    else:
        return {"unsupport": "currently only support single for api interface"}



if __name__ == '__main__':
    app.run(debug=True)


