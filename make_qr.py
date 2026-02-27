from argparse import ArgumentParser
from io import BytesIO

from PIL import Image
import qrcode
from cairosvg import svg2png

def make_highres_qr_with_logo(
    url: str,
    logo_svg_path: str,
    output_path: str,
    box_size: int = 40,
):
    
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    qr_width, qr_height = qr_img.size

    logo_size = int(min(qr_width, qr_height) * 0.22)

    with open(logo_svg_path, "rb") as f:
        logo_svg_bytes = f.read()

    png_bytes = svg2png(
        bytestring=logo_svg_bytes,
        output_width=logo_size,
        output_height=logo_size
    )

    logo_img = Image.open(BytesIO(png_bytes)).convert("RGBA")

    padding = int(logo_size * 0.15)
    bg_size = logo_size + padding * 2

    logo_bg = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 255))
    logo_bg.paste(logo_img, (padding, padding), logo_img)

    pos = (
        (qr_width - bg_size) // 2,
        (qr_height - bg_size) // 2
    )
    qr_img.paste(logo_bg, pos, logo_bg)

    qr_img.save(output_path, dpi=(300, 300))
    print(f"Saved high-resolution QR to {output_path}")


parser = ArgumentParser(description="Generate a high-resolution QR code with a logo")
parser.add_argument("--url", type=str, required=True, help="URL to encode in the QR code")
parser.add_argument("--logo_svg_path", type=str, required=True, help="Path to the logo SVG file")
parser.add_argument("--output_path", type=str, default="qr_with_logo.png", help="Output path for the generated QR code image")
args = parser.parse_args()

if __name__ == "__main__":

    make_highres_qr_with_logo(
        url=args.url,
        logo_svg_path=args.logo_svg_path,
        output_path=args.output_path,
        box_size=40
    )
