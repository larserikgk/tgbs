from PIL import Image, ImageFont, ImageDraw, ImageOps

template = Image.open('crewtemplates/layer_background.png').convert("RGBA")
profile_photo = Image.open('6268.png').convert("RGBA")
ribbon_image = Image.open('crewtemplates/layer_sidebar_blue.png').convert("RGBA")

template.paste(ribbon_image, ribbon_image)

profile_photo = profile_photo.resize((394, 525), Image.ANTIALIAS)

f = ImageFont.truetype('fonts/DroidSans.ttf', 26)
font_bold = ImageFont.truetype('fonts/DroidSans-Bold.ttf', 50)

text_addition = ImageDraw.Draw(template)
text_addition.text((412, 344), "ID: 6268", font=f, fill=0)
text_addition.text((412, 384), "Lars Erik Græsdal-Knutrud", font=f, fill=0)
text_addition.text((412, 424), "Larsynoob", font=f, fill=0)
text_addition.text((412, 464), "MEMBER", font=f, fill=0)
text_addition.text((360, 554), "CORE:SYSTEMS", font=font_bold)

# pic size (394, 525)

template.paste(profile_photo, profile_photo)

template.show()
