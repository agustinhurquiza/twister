import pixie

image = pixie.Image(800, 656)

typeface = pixie.read_typeface("src/Ubuntu-Regular_1.ttf")
background = pixie.read_image("src/img/backgrounds/03.png")
icon = pixie.read_image("src/img/icons/wsymbol_0002_sunny_intervals.png")
tmper = pixie.read_image("src/img/icons/cool.png")

def make_font(typeface, size, color):
    font = typeface.new_font()
    font.size = size
    font.paint.color = color
    return font

path = pixie.Path()
path.rounded_rect(50, 300, 700, 306, 25, 25, 25, 25)

mask = pixie.Mask(800, 656)
mask.fill_path(path)

blur = background.copy()
blur.blur(50)
blur.mask_draw(mask)

image.draw(background)
image.draw(icon,
    pixie.translate(100, 50) *
    pixie.scale(0.4, 0.4)
)
image.draw(tmper,
    pixie.translate(360, 50) *
    pixie.scale(0.4, 0.4)
)
image.draw(blur)

image.fill_text(
    font=make_font(typeface, 70, pixie.Color(0, 0, 0, 1)),
    text="-18 °C",
    h_align=pixie.LEFT_ALIGN,
    bounds=pixie.Vector2(365, 280),
    transform=pixie.translate(510, 95)
)

image.fill_text(
    font=make_font(typeface, 30, pixie.Color(0, 0, 0, 1)),
    text="Stockport, United Kingdom",
    h_align=pixie.CENTER_ALIGN,
    bounds=pixie.Vector2(800, 180),
    transform=pixie.translate(0, 320)
)

image.fill_text(
    font=make_font(typeface, 30, pixie.Color(0, 0, 0, 1)),
    text="Partly cloudy",
    h_align=pixie.CENTER_ALIGN,
    bounds=pixie.Vector2(800, 180),
    transform=pixie.translate(0, 360)
)

image.fill_text(
    font=make_font(typeface, 25, pixie.Color(0, 0, 0, 1)),
    text="Wind speed : 6 Km/H \nWind degree : 190°\nWind Dir : S \nPressure : 1012 MB\nPrecip : 0 MM",
    h_align=pixie.LEFT_ALIGN,
    bounds=pixie.Vector2(300, 300),
    transform=pixie.translate(90, 430)
)

image.fill_text(
    font=make_font(typeface, 25, pixie.Color(0, 0, 0, 1)),
    text="Humidity : 87 kPa\nCloud cover : 75 okta\nFeelslike : 8 °C\nUV index : 1 \nVisibility : 10 Km/H\n",
    h_align=pixie.RIGHT_ALIGN,
    bounds=pixie.Vector2(300, 300),
    transform=pixie.translate(410, 430)
)

image.write_file("examples/template.png")
