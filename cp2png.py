import math
from PIL import Image, ImageDraw
import cairo
from cp import CpLine
import time

border_lines = []
def cp2png(cp, size=2048, margin=6, aa_scale=2):
    global border_lines
    width, height = cp.size()
    min_x = cp.minX
    min_y = cp.minY
    lines = cp.lines

    size /= aa_scale

    if width < height:
        factor = int(size) * aa_scale / height
    else:
        factor = int(size) * aa_scale / width

    if width < height:
        inner_factor = (size - margin) * aa_scale / height
    else:
        inner_factor = (size - margin) * aa_scale / width

    # Setting up surface to draw on
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, math.ceil(width * factor), math.ceil(height * factor))
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_NONE)

    # Making background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, width * factor, height * factor)
    ctx.fill()
    ctx.set_line_width(aa_scale)

    get_border(lines)

    for line in lines:
        ctx.set_source_rgb(line.color()[0], line.color()[1], line.color()[2])
        ctx.move_to((line.x1 - min_x) * inner_factor + margin, (line.y1 - min_y) * inner_factor + margin)  # Starting point
        ctx.line_to((line.x2 - min_x) * inner_factor + margin, (line.y2 - min_y) * inner_factor + margin)  # Ending point
        ctx.stroke()  # Drawing line

    data = surface.get_data()
    image = Image.frombuffer("RGBA", (math.ceil(width * factor), math.ceil(height * factor)), data, "raw", "BGRA", 0, 1)
    return image

def space_lines(cp, shrink_factor):
    start = time.time()
    lines = cp.lines
    for line in lines:
        x1 = line.x1
        x2 = line.x2
        y1 = line.y1
        y2 = line.y2
        x = abs(x2 - x1)
        y = abs(y2 - y1)
        length = math.sqrt(x * x + y * y)
        x_change = shrink_factor * x / length
        y_change = shrink_factor * y / length

        # print("x: " + str(x) + " y: " + str(y) + " length: " + str(length) + " x change: " + str(x_change) + " y change: " + str(y_change))
        if line.type != 1:
            if x1 < x2:
                line.x1 += x_change
                line.x2 -= x_change
            else:
                line.x1 -= x_change
                line.x2 += x_change

            if y1 < y2:
                line.y1 += y_change
                line.y2 -= y_change
            else:
                line.y1 -= y_change
                line.y2 += y_change

    end = time.time()
    #print("Spacing Lines: ", (end - start) * 10 ** 3, "ms")

def space_lines_fast(cp, shrink_factor):
    #print("minX " + str(cp.minX) + "minY" + str(cp.minY))
    start = time.time()
    lines = cp.lines
    line_adjustments = []
    for line in lines:
        x1, x2, y1, y2 = line.x1, line.x2, line.y1, line.y2

        x = abs(x2 - x1)
        y = abs(y2 - y1)
        length = math.sqrt(x * x + y * y)
        x_change = shrink_factor * x / length
        y_change = shrink_factor * y / length

        x1_end, x2_end, y1_end, y2_end = x1, x2, y1, y2

        if line.type != 1:
            if x1 < x2:
                x1_end += x_change
                x2_end -= x_change
            else:
                x1_end -= x_change
                x2_end += x_change

            if y1 < y2:
                y1_end += y_change
                y2_end -= y_change
            else:
                y1_end -= y_change
                y2_end += y_change

            line_adjustments.append(CpLine(line.type, x1, y1, x1_end, y1_end))
            line_adjustments.append(CpLine(line.type, x2, y2, x2_end, y2_end))

    end = time.time()
    #print("Spacing Lines 2: ", (end - start) * 10 ** 3, "ms")

    return line_adjustments

def update_png(cp, lines, image, size=2048, margin=6, aa_scale=2):
    width, height = cp.size()
    min_x = cp.minX
    min_y = cp.minY

    size /= aa_scale

    if width < height:
        inner_factor = (size - margin) * aa_scale / height
    else:
        inner_factor = (size - margin) * aa_scale / width

    surface = from_pil(image)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_NONE)
    ctx.set_source_rgb(255, 255, 255)
    ctx.set_line_width(aa_scale)

    for line in lines:
        ctx.move_to((line.x1 - min_x) * inner_factor + margin,
                    (line.y1 - min_y) * inner_factor + margin)  # Starting point
        ctx.line_to((line.x2 - min_x) * inner_factor + margin,
                    (line.y2 - min_y) * inner_factor + margin)  # Ending point
        ctx.stroke()  # Drawing line

    ctx.set_source_rgb(0, 0, 0)
    for line in border_lines:
        ctx.move_to((line.x1 - min_x) * inner_factor + margin,
                    (line.y1 - min_y) * inner_factor + margin)  # Starting point
        ctx.line_to((line.x2 - min_x) * inner_factor + margin,
                    (line.y2 - min_y) * inner_factor + margin)  # Ending point
        ctx.stroke()  # Drawing line

    data = surface.get_data()
    image = Image.frombuffer("RGBA", (image.width, image.height), data, "raw", "BGRA", 0, 1)
    return image

def get_border(lines):
    global border_lines
    global border_lines
    for line in lines:
        if line.type == 1:
            border_lines.append(line)



def from_pil(im: Image, alpha: float=1.0, format: cairo.Format=cairo.FORMAT_ARGB32) -> cairo.ImageSurface:
    """
    :param im: Pillow Image
    :param alpha: 0..1 alpha to add to non-alpha images
    :param format: Pixel format for output surface
    """
    assert format in (
        cairo.FORMAT_RGB24,
        cairo.FORMAT_ARGB32,
    ), f"Unsupported pixel format: {format}"
    if 'A' not in im.getbands():
        im.putalpha(int(alpha * 256.))
    arr = bytearray(im.tobytes('raw', 'BGRa'))
    surface = cairo.ImageSurface.create_for_data(arr, format, im.width, im.height)
    return surface

