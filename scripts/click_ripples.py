import subprocess, sys, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]
Wd, H, FPS = 1080, 1920, 30
# (time, x, y) in full-frame pixels; top strip recordings only
CLICKS = [(27.10, 118, 618), (35.08, 264, 231), (36.95, 789, 460), (40.45, 945, 465)]
DUR = 0.5
dec = subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{Wd}x{H}','-r',str(FPS),'-i','-',
                        '-i',src,'-map','0:v','-map','1:a','-c:v','libx264','-crf','15','-preset','fast','-pix_fmt','yuv420p','-c:a','copy',out], stdin=subprocess.PIPE)
n = 0; fs = Wd*H*3
while True:
    buf = dec.stdout.read(fs)
    if len(buf) < fs: break
    t = n / FPS; n += 1
    act = [(t-c, x, y) for c, x, y in CLICKS if 0 <= t-c < DUR]
    if act:
        f = np.frombuffer(buf, np.uint8).reshape(H, Wd, 3).copy()
        for dt, x, y in act:
            p = dt / DUR; e = 1 - (1-p)**3
            ov = f.copy()
            # soft press dot
            if p < 0.45:
                cv2.circle(ov, (x, y), int(16 - 4*p), (211, 1, 53), -1, cv2.LINE_AA)
                a_dot = 0.55 * (1 - p/0.45)
                f = cv2.addWeighted(ov, a_dot, f, 1-a_dot, 0)
            ov = f.copy()
            cv2.circle(ov, (x, y), int(14 + 46*e), (255, 255, 255), 4, cv2.LINE_AA)
            if p > 0.12:
                q = (p-0.12)/0.88; e2 = 1-(1-q)**3
                cv2.circle(ov, (x, y), int(10 + 30*e2), (255, 255, 255), 2, cv2.LINE_AA)
            a = 0.95 * (1 - p)
            f = cv2.addWeighted(ov, a, f, 1-a, 0)
        buf = f.tobytes()
    enc.stdin.write(buf)
enc.stdin.close(); enc.wait(); dec.wait()
print('frames', n)
