from flask import Flask, request
from werkzeug.exceptions import BadRequest, NotFound
from badge_service.badge_image_generator import BadgeImageGenerator
from badge_service import settings


app = Flask(__name__)


@app.route('/badges/crew', methods=['GET'])
def crew_badges():
    generator = BadgeImageGenerator(settings.get_config())
    crew = request.args.get('crew')
    id = request.args.get('id')
    ribbon_color = request.args.get('ribbonColor')
    if id and crew:
        raise BadRequest('Parameters crew and id are mutually exclusive')
    if crew:
        raise NotImplemented()
    if id:
        badge  = generator.save_crew_badge(ribbon_color, id)
    if badge:
        return 'Badge saved'
    else:
        raise NotFound


@app.route('/badges/other', methods=['GET'])
def other_badges():
    raise NotImplemented
    generator = BadgeImageGenerator(settings.get_config())

    invited_by = request.args.get('badgeType')
    start = request.args.get('start')
    stop = request.args.get('stop')
    ribbon_color = request.args.get('ribbonColor')
    text = request.args.get('text')

    if (start and not stop) or (not start and stop):
        raise BadRequest('Both parameters start and stop must be used')

    return 'Flask Dockerized'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
