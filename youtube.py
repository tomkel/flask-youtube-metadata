from flask import Flask, jsonify
import youtube_dl

#        return jsonify(username=g.user.username,
#                   email=g.user.email,
#                   id=g.user.id)

app = Flask(__name__)


@app.route('/')
def get_info():

    def get_best_audio(formats):
        best = {}
        for f in formats:
            # abr not in some formats with both a+v
            if (not f['acodec'] in best or
                    best[f['acodec']]['abr'] > f['abr']):
                best[f['acodec']] = f
        return list(best.values())

    def has_av(f):
        return f['acodec'] != 'none' and f['vcodec'] != 'none'

    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info('http://www.youtube.com/watch?v=BaW_jenozKc',
                                download=False)
        audio_only = [f for f in info['formats'] if f['acodec'] != 'none' and
                      f['vcodec'] == 'none']
        audio_only_best = get_best_audio(audio_only)
        return jsonify([f for f in info['formats'] if has_av(f)] +
                       audio_only_best)
