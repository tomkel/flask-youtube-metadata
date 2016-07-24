from flask import Flask, jsonify, abort
from flask_cors import CORS
import youtube_dl

#        return jsonify(username=g.user.username,
#                   email=g.user.email,
#                   id=g.user.id)

app = Flask(__name__)
CORS(app)


class ErrorLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


@app.errorhandler(400)
def unavailable(error):
    return error.description[0], 400


@app.route('/metadata/<vid>')
def get_info(vid):

    def get_best_audio(formats):
        best = {}
        for f in formats:
            # abr not in some formats with both a+v
            # but we have already filtered those out so no need to worry
            if (not f['acodec'] in best or
                    best[f['acodec']]['abr'] > f['abr']):
                best[f['acodec']] = f
        return list(best.values())

    def has_av(f):
        return f['acodec'] != 'none' and f['vcodec'] != 'none'

    ydl_opts = {'logger': ErrorLogger(), 'no_color': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(
                    'http://www.youtube.com/watch?v={}'.format(vid),
                    download=False)
        except Exception as e:
            return abort(400, e.args)

        audio_only = [f for f in info['formats'] if f['acodec'] != 'none' and
                      f['vcodec'] == 'none']
        audio_only_best = get_best_audio(audio_only)
        return jsonify({'formats': [f for f in info['formats'] if has_av(f)] +
                        audio_only_best,
                       'title': info['title']})
