#!/usr/bin/env python
from argparse import ArgumentParser
from segno import make
from io import BytesIO
from PIL import Image
from pylatex import Document, TikZ, TikZDraw, TikZCoordinate, TikZOptions, \
                    TikZNode, NewLine,HorizontalSpace, VerticalSpace, \
                        NoEscape, StandAloneGraphic, HugeText
from pylatex.utils import bold
from pathlib import Path

def run():
    
    args = parse_cli()
    generate_qr_image(**args)
    generate_wifi_card(**args)
    # Clean up generated QR image
    Path("wifi_qr.png").unlink(missing_ok=True)

def generate_wifi_card(network, passwd) -> None:
    """Generate Latex document"""
    doc = Document(geometry_options={"margin": "0.5in", "landscape": True}, page_numbers=False, lmodern=False, indent=False)
    # Separate card images
    separators = [
        [HorizontalSpace("2em")],
        [VerticalSpace("2em"), NewLine()],
        [HorizontalSpace("2em")],
        []
    ]

    # Create Tikz image around each separator
    for line in separators:
        with doc.create(TikZ(options=["x=1in", "y=1in", "transform shape", NoEscape(r"font=\fontfamily{phv}")])) as pic:
            pic.append(TikZDraw([
                TikZCoordinate(0, 0),
                'rectangle',
                TikZCoordinate(4.0, 2.5)
            ], TikZOptions("gray")))
            pic.append(TikZNode(
                at=TikZCoordinate(3.9, 1.25),
                text=StandAloneGraphic("wifi_qr.png", image_options=[NoEscape("width=2.0in"), NoEscape("keepaspectratio")]).dumps(),
                options=TikZOptions(anchor="east")
            ))

            opts = {
                "anchor": "west",
                "align": "left",
                "inner sep": "0.2in",
                "font": NoEscape(r"\Large")
            }
            wifi_code = [
                HugeText(bold("Wifi")).dumps(),
                NoEscape(""),
                NoEscape(r"\underline{Network}"),
                f"{network}",
                NoEscape(""),
                NoEscape(r"\underline{Password}"),
                f"{passwd}"
            ]
            pic.append(TikZNode(
                at=TikZCoordinate(0, 1.25),
                text=r"\\".join(wifi_code),
                options=TikZOptions(**opts)
            ))
        doc.extend(line)

    doc.generate_pdf("wifi-card", compiler="pdflatex", clean=True)

def generate_qr_image(network, passwd) -> None:
    """Generate QR Code from Network info"""
    out = BytesIO()
    make(f"WIFI:T:WPA;S:{network:s};P:{passwd:s};;", error="H", version=10) \
        .save(out, kind="png", scale=100)
    out.seek(0)

    # Add wifi logo to QR code
    img = Image.open(out)
    qr_width, qr_height = img.size
    logo_max_size = qr_height // 3
    logo = Image.open('.wifi-icon.jpeg')
    logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
    box = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)
    img.paste(logo, box)
    img.save("wifi_qr.png")

def parse_cli():
    parser = ArgumentParser("Generate a PDF Wifi Card with QR Code")
    parser.add_argument("-n", dest="network", help="Network Name (network)", type=str, required=True)
    parser.add_argument("-p", dest="passwd", help="Network Password", type=str, required=True)

    return vars(parser.parse_args())

if __name__ == "__main__":
    run()
