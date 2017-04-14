from PIL import Image, ImageFont, ImageDraw
from .models import *
from os import path as op
from os import listdir


class BadgeImageGenerator:
    def __init__(self, config):
        self._config = config

    def generate_badge(self, badge_type, ribbon_color, crew_info=None, photo=None, text=None, number=None):

        # Generate crew badge
        if badge_type is BadgeType.Crew:
            if crew_info and photo:
                return self.generate_crew_badge(ribbon_color, crew_info, photo)

        # Generate blank badge
        if badge_type is BadgeType.Blank:
            if text:
                return self.generate_blank_badge(ribbon_color, text, number)

        # Generate blank badge with 'Invited By'
        if badge_type is BadgeType.Invitation:
            if text:
                return self.generate_blank_badge(ribbon_color, text, number, True)

    def generate_crew_badge(self, ribbon_color, crew_info, photo):
        template = Image.open(self._config['crew_template']).convert("RGBA")
        ribbon_image = self._get_ribbon_image(BadgeType.Crew, ribbon_color)

        template.paste(ribbon_image, ribbon_image)
        if photo is not None:
            photo = photo.resize((394, 525), Image.ANTIALIAS)
            template.paste(photo.resize((394, 525), Image.ANTIALIAS), photo)

        self._transpose_crew_info(template, crew_info)

        return template

    def generate_blank_badge(self, ribbon_color, text, number, invited_by=False):
        template = Image.open(self._config['other_template']).convert("RGBA")
        ribbon_image = self._get_ribbon_image(BadgeType.Blank, ribbon_color)
        invite_font = ImageFont.truetype('resources/fonts/DroidSans-Bold.ttf', 40)
        text_font = ImageFont.truetype('resources/fonts/DroidSans-Bold.ttf', 60)
        template.paste(ribbon_image, ribbon_image)

        text_addition = ImageDraw.Draw(template)

        if not invited_by:
            text_addition.text((self._center_text_coord(template, text_font, text), 500), text, font=text_font)
        else:
            text_addition.text((self._center_text_coord(template, invite_font, 'INVITED BY'), 450), 'INVITED BY',
                               font=invite_font)
            text_addition.text((self._center_text_coord(template, text_font, text), 500), text, font=text_font)

        if number:
            text_addition.text((20, 20), '#' + str(number), font=text_font, fill=0)

        return template

    def _center_text_coord(self, image, font, text):
        base_w, base_h = image.size
        text_w, text_h = font.getsize(text)
        return (base_w - text_w)/2

    def _transpose_crew_info(self, base_image, crew_info):
        font = ImageFont.truetype('resources/fonts/DroidSans.ttf', 26)
        font_bold = ImageFont.truetype('resources/fonts/DroidSans-Bold.ttf', 50)
        text_addition = ImageDraw.Draw(base_image)

        text_addition.text((412, 344), crew_info.id, font=font, fill=0)
        text_addition.text((412, 384), crew_info.name, font=font, fill=0)
        text_addition.text((412, 424), crew_info.nick, font=font, fill=0)
        text_addition.text((412, 464), crew_info.position, font=font, fill=0)
        text_addition.text(
            (self._center_text_coord(base_image, font_bold, crew_info.crew), 554), crew_info.crew, font=font_bold)

    def _get_ribbon_image(self, badge_type, ribbon_color):
        crew_rib, other_rib = self._config['crew_ribbon_folder'], self._config['other_ribbon_folder']
        crew_ribbons = [op.join(crew_rib, f) for f in listdir(crew_rib) if op.isfile(op.join(crew_rib, f))]
        other_ribbons = [op.join(other_rib, f) for f in listdir(other_rib) if op.isfile(op.join(other_rib, f))]

        if badge_type is BadgeType.Crew and ribbon_color:
            for ribbon in crew_ribbons:
                if ribbon_color.lower() in ribbon.lower():
                    return Image.open(ribbon).convert("RGBA")

        if badge_type is BadgeType.Blank:
            for ribbon in other_ribbons:
                if ribbon_color.lower() in ribbon.lower():
                    return Image.open(ribbon).convert("RGBA")

        raise ValueError('Invalid ribbon color')


