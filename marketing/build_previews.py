"""Create silent CrazyGames previews that illustrate the game's actual rules."""

from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw
from build_covers import NAVY, CREAM, GOLD, font, parcel, base_canvas

try:
    import imageio_ffmpeg
except ImportError:
    sys.path.insert(0, str(Path.home() / "AppData/Local/Temp/pochta-video-deps"))
    import imageio_ffmpeg

OUT = Path(__file__).parent
FPS = 12
SECONDS = 15
EVENTS = [
    (2, 0, "box"), (3, 1, "tube"), (4, 2, "envelope"),
    (5, 3, "sack"), (7, 10, "basket"),
    (8, 8, "box"), (9, 9, "box"), (10, 12, "box"), (11, 13, "box"),
]
COLORS = {"box": "#c8935a", "tube": "#5b9bd5", "envelope": "#e3b74f", "sack": "#7fae5f", "basket": "#a06cc9"}
NAMES = {"box": "BOX", "tube": "TUBE", "envelope": "LETTER", "sack": "SACK", "basket": "BASKET"}


def rr(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(tuple(map(int, box)), int(radius), fill=fill, outline=outline, width=int(width))


def text(draw, xy, content, size, fill, anchor=None):
    draw.text(xy, content, font=font(size), fill=fill, anchor=anchor)


class Scene:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.portrait = h > w
        self.bg = base_canvas(w, h).convert("RGB")
        self.scale = min(w / 1080, h / 1080)
        if self.portrait:
            self.board = (35, 148, w - 35, 1104)
            self.grid = (128, 246, 824)
            self.hand = (35, 1128, w - 35, 1378)
            self.goals = (35, 1400, w - 35, h - 30)
        else:
            self.board = (45, 155, 1108, h - 42)
            self.grid = (180, 250, 735)
            self.goals = (1145, 155, w - 45, 565)
            self.hand = (1145, 595, w - 45, h - 42)
        self.grid_x, self.grid_y, self.grid_size = self.grid
        self.gap = int(self.grid_size * .014)
        self.cell = (self.grid_size - self.gap * 5) / 4
        self.icons = {kind: parcel(kind, int(self.cell * .86)) for kind in COLORS}
        self.hand_icons = {kind: parcel(kind, int((self.hand[2]-self.hand[0])*.19)) for kind in COLORS}
        self.mouse = parcel("mouse", int(self.cell * .83))
        cover = "cover-portrait.png" if self.portrait else "cover-landscape.png"
        self.cover = Image.open(OUT / cover).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)

    def cell_xy(self, index):
        col, row = index % 4, index // 4
        x = self.grid_x + self.gap + col * (self.cell + self.gap)
        y = self.grid_y + self.gap + row * (self.cell + self.gap)
        return x, y

    def frame(self, t):
        if t < .9:
            return self.cover
        img = self.bg.copy()
        d = ImageDraw.Draw(img)
        w, h = self.w, self.h
        # Header
        text(d, (50, 38), "MOUSEPROOF MAILROOM", 37 if self.portrait else 45, CREAM)
        stat_x = w - (420 if self.portrait else 575)
        rr(d, (stat_x, 28, stat_x+200, 112), 14, GOLD)
        rr(d, (stat_x+214, 28, stat_x+410, 112), 14, "#31545a")
        placed = sum(t >= event_t for event_t, _, _ in EVENTS)
        # Include delivery points, completed missions and the second bonus move's combo.
        score = placed + (20 if t >= 5 else 0) + (18 if t >= 7 else 0) + (14 if t >= 11 else 0)
        text(d, (stat_x+18, 37), "SCORE / 70", 19, NAVY)
        text(d, (stat_x+18, 64), str(score), 35, NAVY)
        text(d, (stat_x+230, 37), "DELIVERED", 17, CREAM)
        text(d, (stat_x+230, 65), f"{placed}/16", 34, CREAM)
        # Main panels
        rr(d, self.board, 26, "#f6eedc", "#092128", 6)
        rr(d, self.goals, 23, "#f6eedc", "#092128", 6)
        rr(d, self.hand, 23, "#e9e5d5", "#092128", 6)
        bx1, by1, bx2, by2 = self.board
        text(d, (bx1+32, by1+24), "WAREHOUSE / 01", 17, "#178d85")
        text(d, (bx1+32, by1+51), "SORTING FLOOR", 31, NAVY)
        # Shelf board
        gx, gy, gs = self.grid
        rr(d, (gx, gy, gx+gs, gy+gs), 20, "#d5bda0", "#9f795c", 6)
        for i in range(16):
            x, y = self.cell_xy(i)
            rr(d, (x,y,x+self.cell,y+self.cell), 14, "#ebdcc0", "#c5a886", 5)
            rr(d, (x+10,y+10,x+self.cell-10,y+self.cell-10), 9, None, "#cbb99e", 2)
        for event_t, i, kind in EVENTS:
            if t < event_t:
                continue
            x, y = self.cell_xy(i)
            icon = self.icons[kind]
            scale = min(1, .55 + (t-event_t)*3)
            if scale < 1:
                sw = int(icon.width*scale)
                shown = icon.resize((sw,sw), Image.Resampling.LANCZOS)
            else:
                shown = icon
            img.paste(shown, (int(x+(self.cell-shown.width)/2),int(y+(self.cell-shown.height)/2)), shown)
        if 6 <= t < 7:
            x, y = self.cell_xy(10)
            img.paste(self.mouse, (int(x+6),int(y+11)), self.mouse)
        d = ImageDraw.Draw(img)
        if t >= 5:
            y = self.grid_y + self.gap + self.cell*.5
            d.line((gx+4,y,gx+gs-4,y), fill="#178d85", width=max(18,int(gs*.026)))
            d.line((gx+4,y-5,gx+gs-4,y-5), fill="#d9f7df", width=3)
        if t >= 11:
            for i in (8,9,12,13):
                x, y = self.cell_xy(i)
                d.ellipse((x+self.cell-40,y+8,x+self.cell-8,y+40), fill=GOLD, outline="#9f795c", width=2)
                text(d, (x+self.cell-24,y+8), "✓", 25, NAVY, "mt")
        # Missions
        x1,y1,x2,y2 = self.goals
        text(d, (x1+25,y1+20), "TODAY'S ROUTE", 17, "#178d85")
        text(d, (x1+25,y1+51), "MISSIONS", 31, NAVY)
        missions = [("Seal a shelf", t>=5), ("Catch a mouse", t>=7), ("Make a tape patch", t>=11)]
        for j,(label,done) in enumerate(missions):
            if self.portrait:
                mw = (x2-x1-70)/3
                mx = x1+25+j*(mw+10)
                yy = y1+87
                box = (mx,yy,mx+mw,yy+56)
                label_size = 17
            else:
                yy = y1+102+j*76
                box = (x1+25,yy,x2-25,yy+66)
                mx = x1+25
                label_size = 23
            rr(d, box, 12, "#daf1e0" if done else "#fffaf0", "#d7d0ba", 2)
            iy = yy+17
            d.ellipse((mx+13,iy,mx+36,iy+23), fill="#178d85" if done else "#d7d0ba")
            if done:
                d.line((mx+18,iy+11,mx+23,iy+16,mx+32,iy+6), fill=CREAM, width=3)
            text(d, (mx+47,yy+14), label, label_size, NAVY)
        # Hand
        x1,y1,x2,y2 = self.hand
        text(d, (x1+25,y1+18), "READY TO DELIVER", 17, "#178d85")
        text(d, (x1+25,y1+43), "YOUR PARCELS", 31, NAVY)
        upcoming = next(((et,idx,kind) for et,idx,kind in EVENTS if et>t), EVENTS[-1])
        selection = upcoming[2]
        options = [selection, "tube" if selection!="tube" else "box", "envelope" if selection!="envelope" else "sack"]
        card_top = y1+90
        card_gap = 13
        card_w = (x2-x1-50-card_gap*2)/3
        card_h = max(72,y2-card_top-16)
        for j,kind in enumerate(options):
            cx = x1+25+j*(card_w+card_gap)
            rr(d, (cx,card_top,cx+card_w,card_top+card_h), 12, "#fffaf0", "#178d85" if j==0 else "#cfc8b5", 5 if j==0 else 3)
            d.rectangle((cx+5,card_top+2,cx+card_w-5,card_top+10), fill=COLORS[kind])
            icon = self.hand_icons[kind]
            if self.portrait:
                icon = icon.resize((int(card_h*.57),int(card_h*.57)), Image.Resampling.LANCZOS)
            img.paste(icon, (int(cx+(card_w-icon.width)/2),int(card_top+card_h*.08)), icon)
            text(d, (cx+card_w/2,card_top+card_h-35), NAMES[kind], 20, NAVY, "mt")
        # Reward popups
        reward = None
        if 5 <= t < 5.9: reward = "SHELF SEALED!  +10"
        elif 7 <= t < 7.9: reward = "MOUSE CAUGHT!  +5"
        elif 11 <= t < 11.9: reward = "TAPE PATCH!  +4"
        if reward:
            pw = 525 if not self.portrait else 650
            px = (w-pw)/2
            py = 38 if not self.portrait else 90
            rr(d, (px,py,px+pw,py+70), 16, GOLD, "#9e7136", 4)
            text(d, (w/2,py+18), reward, 34 if not self.portrait else 38, NAVY, "mt")
        return img


def build(name, w, h):
    scene = Scene(w,h)
    output = OUT / f"preview-{name}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for n in range(FPS*SECONDS):
            frame = scene.frame(n/FPS)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError("ffmpeg failed")
    finally:
        if proc.poll() is None:
            proc.kill()
    print(output, output.stat().st_size)


if __name__ == "__main__":
    build("landscape",1920,1080)
    build("portrait",1080,1620)
