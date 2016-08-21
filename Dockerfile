FROM lucidfrontier45/python-uwsgi:3
MAINTAINER Tommy Kelly <docker@tkel.ly>

ENV sourceDir /flask-youtube-metadata

RUN pip3 install virtualenv

RUN git clone https://github.com/tomkel/flask-youtube-metadata.git $sourceDir

WORKDIR $sourceDir

RUN virtualenv yt-env \
        && . yt-env/bin/activate \
        && pip install uwsgi \
        && pip install -r requirements.txt

ENTRYPOINT ["uwsgi" "--socket" ":5000" "--module" "youtube:app" \
        "--virtualenv" "yt-env" "--master" "--die-on-term" "--vacuum" \
        "--manage-script-name" "--stats" ":1717"]
CMD ["--processes" "4" "--threads" "2"]

EXPOSE 5000 1717
