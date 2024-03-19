import time
import ulab.numpy as np

def track_time(div):
    characterising_speed = not input(f"""
                  Press the 'Enter' key whenever you see a division of {div}um.
                  When you are done, press any other key + Enter.
                  Are you ready? Press 'Enter' to start!""")
    t0 = time.monotonic_ns()

    ts = [t0]
    while characterising_speed:
        trigger = input(f"Press Enter")
        if trigger == '': ts.append(time.monotonic_ns());
        else: break

    t0 = 0
    t1 = 1
    del_ts = []
    while t0 < len(ts)-1:
        del_ts.append((ts[t1]-ts[t0]) * 1E-9)
        t0+=1
        t1+=1

    print(del_ts)
    return del_ts

def get_speed(div, ts):
    mean_t = np.mean(ts)
    err_t = np.std(ts)/np.sqrt(len(ts))
    print(f"The mean time between measurements was {mean_t} +/- {err_t}")
    print(f"Therefore, the mean um/second is:", div*1E-6/mean_t)

