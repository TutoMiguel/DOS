from pathlib import Path
from PIL import Image, ImageDraw

d = Path(r"C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\qa_word_workspace")
fs = sorted(d.glob("page-[0-9]*.png"), key=lambda p: int(p.stem.split("-")[1]))
ims = [Image.open(f).convert("RGB") for f in fs]
w = 180
h = round(ims[0].height * w / ims[0].width)
thumbs = []
for i, im in enumerate(ims, 1):
    x = im.resize((w, h))
    c = Image.new("RGB", (w, h + 24), "white")
    c.paste(x, (0, 24))
    ImageDraw.Draw(c).text((5, 5), str(i), fill="black")
    thumbs.append(c)
cols = 4
rows = (len(thumbs) + cols - 1) // cols
out = Image.new("RGB", (cols * w, rows * (h + 24)), "#dddddd")
for j, im in enumerate(thumbs):
    out.paste(im, ((j % cols) * w, (j // cols) * (h + 24)))
out.save(d / "contact_sheet.png")
