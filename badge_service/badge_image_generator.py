from PIL import Image, ImageFont, ImageDraw
from .models import BadgeType, CrewBadgeInfo
from os import path as op
from os import listdir
from wannabe_service.service import WannabeService


class BadgeImageGenerator:
    def __init__(self, config):
        self._crew_template = config.get('BadgeService', 'crew_template')
        self._other_template = config.get('BadgeService', 'other_template')
        self._crew_ribbons = config.get('BadgeService', 'crew_ribbon_folder')
        self._other_ribbons = config.get('BadgeService', 'other_ribbon_folder')
        self._wannabe_service = WannabeService(config)
        self._output_directory = config.get('BadgeService', 'output_directory')

    def save_crew_badge(self, ribbon_color, id):
        badge = self.generate_crew_badge_with_id(ribbon_color, id)
        if badge:
            badge.save(op.join(self._output_directory, id + '.png'))
            return badge

    def generate_crew_badges(self, ribbon_color, crew_info=None):
        users = self._wannabe_service.get_approved_users()
        badges = []

        for user in users:
            badges.append(self.generate_crew_badge(ribbon_color, CrewBadgeInfo(wannabe_json=user)))
        return badges

    def generate_other_badges(self, ribbon_color, text=None, start=None, stop=None, invited=False):
        if not (start and stop):
            return self._generate_blank_badge(ribbon_color, text, None, invited)
        else:
            results = []
            for value in range(start, stop+1):
                results.append(self._generate_blank_badge(ribbon_color, text, value, invited))
            return results

    def generate_crew_badge_with_id(self, ribbon_color, id):
        wannabe_json = self._wannabe_service.get_crew_info_json(id)
        if wannabe_json:
            crew_info = CrewBadgeInfo(wannabe_json=wannabe_json)
            return self.generate_crew_badge(ribbon_color, crew_info)

    def generate_crew_badge(self, ribbon_color, crew_info):
        template = Image.open(self._crew_template).convert("RGBA")
        ribbon_image = self._get_ribbon_image(BadgeType.Crew, ribbon_color)
        template.paste(ribbon_image, ribbon_image)
        photo = self._wannabe_service.get_crew_picture(crew_info.id)
        photo = photo.resize((394, 525), Image.ANTIALIAS)
        template.paste(photo.resize((394, 525), Image.ANTIALIAS), photo)

        self._transpose_crew_info(template, crew_info)

        return template

    def _generate_blank_badge(self, ribbon_color, text, number, invited_by=False):
        template = Image.open(self._other_template).convert("RGBA")
        ribbon_image = self._get_ribbon_image(BadgeType.Blank, ribbon_color)
        invite_font = ImageFont.truetype('resources/fonts/DroidSans-Bold.ttf', 40)
        text_font = ImageFont.truetype('resources/fonts/DroidSans-Bold.ttf', 60)
        template.paste(ribbon_image, ribbon_image)

        text_addition = ImageDraw.Draw(template)

        if not invited_by:
            text_addition.text((self._center_text(template, text_font, text), 500), text, font=text_font)
        else:
            text_addition.text((self._center_text(template, invite_font, 'INVITED BY'), 450), 'INVITED BY',
                               font=invite_font)
            text_addition.text((self._center_text(template, text_font, text), 500), text, font=text_font)

        if number:
            text_addition.text((20, 20), '#' + str(number), font=text_font, fill=0)

        return template

    def _center_text(self, image, font, text):
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
        text_addition.text((self._center_text(base_image, font_bold, crew_info.crew), 554), crew_info.crew,
                           font=font_bold)

    def _get_ribbon_image(self, badge_type, ribbon_color):
        crew_rib, other_rib = self._crew_ribbons, self._other_ribbons
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
