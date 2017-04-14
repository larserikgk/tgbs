from PIL import Image, ImageFont, ImageDraw, ImageOps
from .models import *


class BadgeImageGenerator:

    def generate_badge(self, badge_type, ribbon_color, crew_info, photo=None, text=None):
        # Generate crew badge
        if badge_type is BadgeType.Crew:
            if crew_info is not None and photo is not None:
                return self.generate_crew_badge(ribbon_color, crew_info, photo)
        if badge_type is BadgeType.Blank:
            if text is not None:
                return self.generate_blank_badge(ribbon_color, text)

    def generate_crew_badge(self, ribbon_color, crew_info, photo):
        template = Image.open('resources/crewtemplates/layer_background.png').convert("RGBA")
        ribbon_image = self._get_ribbon_image(BadgeType.Crew, ribbon_color)

        template.paste(ribbon_image, ribbon_image)
        if photo is not None:
            photo = photo.resize((394, 525), Image.ANTIALIAS)
            template.paste(photo.resize((394, 525), Image.ANTIALIAS), photo)

        self._transpose_crew_info(template, crew_info)

        return template

    def generate_blank_badge(self, ribbon_color, text):
        template = Image.open('resources/templates/blankbadge_template.png').convert("RGBA")
        ribbon_image = self._get_ribbon_image(BadgeType.Blank, ribbon_color)
        font = ImageFont.truetype('resources/fonts/DroidSans-Bold.ttf', 60)
        template.paste(ribbon_image, ribbon_image)

        text_addition = ImageDraw.Draw(template)
        text_addition.text((412, 500), text, font=font)

        return template

    def _transpose_crew_info(self, base_image, crew_info):
        font = ImageFont.truetype('resources/fonts/DroidSans.ttf', 26)
        font_bold = ImageFont.truetype('resources/fonts/DroidSans-Bold.ttf', 50)
        text_addition = ImageDraw.Draw(base_image)
        text_addition.text((412, 344), crew_info.id, font=font, fill=0)
        text_addition.text((412, 384), crew_info.name, font=font, fill=0)
        text_addition.text((412, 424), crew_info.nick, font=font, fill=0)
        text_addition.text((412, 464), crew_info.position, font=font, fill=0)
        text_addition.text((360, 554), crew_info.crew, font=font_bold)

    def _get_ribbon_image(self, badge_type, ribbon_color):
        if badge_type is BadgeType.Crew:
            if ribbon_color is BadgeRibbonColor.Black:
                return Image.open('resources/crewtemplates/layer_sidebar_black.png').convert("RGBA")
            if ribbon_color is BadgeRibbonColor.Blue:
                return Image.open('resources/crewtemplates/layer_sidebar_blue.png').convert("RGBA")
            if ribbon_color is BadgeRibbonColor.Red:
                return Image.open('resources/crewtemplates/layer_sidebar_blue.png').convert("RGBA")
        if badge_type is BadgeType.Blank:
            if ribbon_color is BadgeRibbonColor.Black:
                return Image.open('resources/templates/otherbadge_black.png').convert("RGBA")
            if ribbon_color is BadgeRibbonColor.Red:
                return Image.open('resources/templates/otherbadge_red.png').convert("RGBA")

        raise ValueError('Invalid ribbon color')


