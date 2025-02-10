import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import time
import random
import pickle  # Untuk penyimpanan cookies menggunakan pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style, init

# Inisialisasi colorama agar bekerja pada Windows
init(autoreset=True)

# =============================================================
# FUNCTION: print_banner
# =============================================================
def print_banner():
    print(Fore.MAGENTA + """
          █████╗ ██╗   ██╗████████╗ ██████╗ 
         ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
         ███████║██║   ██║   ██║   ██║   ██║
         ██╔══██║██║   ██║   ██║   ██║   ██║
         ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
         ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ 
    """ + Style.RESET_ALL)

# =============================================================
# FUNCTION: init_chrome_driver_incognito (untuk login Gmail menggunakan mode incognito)
# =============================================================
def init_chrome_driver_incognito():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # Tambahkan "enable-logging" agar tidak mencetak log berlebih
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# =============================================================
# FUNCTION: init_chrome_driver
# (Mode default dengan opsi headless yang bisa diaktifkan/nonaktifkan)
# =============================================================
def init_chrome_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        # Atur ukuran window pada mode headless agar sesuai dengan resolusi yang diinginkan
        chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# =============================================================
# FUNCTION: save_cookies
# =============================================================
def save_cookies(driver, account_name):
    # Pastikan folder cookies ada
    if not os.path.exists("cookies"):
        os.makedirs("cookies")
    filepath = os.path.join("cookies", f"cookies_{account_name}.pkl")
    with open(filepath, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(Fore.GREEN + f"Cookies berhasil disimpan untuk akun: {account_name}" + Style.RESET_ALL)

# =============================================================
# FUNCTION: load_cookies
# =============================================================
def load_cookies(driver, account_name):
    try:
        filepath = os.path.join("cookies", f"cookies_{account_name}.pkl")
        with open(filepath, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            # Hapus atribut 'sameSite' jika ada agar tidak terjadi masalah
            cookie.pop('sameSite', None)
            # Sesuaikan domain jika diperlukan
            if 'domain' in cookie and cookie['domain'].startswith('.'):
                cookie['domain'] = cookie['domain'].lstrip('.')
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(Fore.YELLOW + f"Gagal menambahkan cookie: {cookie}. Error: {e}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Cookies berhasil dimuat untuk akun: {account_name}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Gagal memuat cookies untuk akun {account_name}, silakan login manual terlebih dahulu!" + Style.RESET_ALL)

# =============================================================
# FUNCTION: load_file_content
# =============================================================
def load_file_content(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# =============================================================
# FUNCTION: delay_with_countdown
# =============================================================
def delay_with_countdown(duration):
    for remaining in range(int(duration), 0, -1):
        print(Fore.YELLOW + f"Menunggu {remaining} detik..." + Style.RESET_ALL, end="\r")
        time.sleep(1)
    print("\n")

# =============================================================
# FUNCTION: auto_scroll
# =============================================================
def auto_scroll(driver, distance=300, count=1):
    try:
        for _ in range(count):
            driver.execute_script("window.scrollBy(0, arguments[0]);", distance)
            time.sleep(2)
    except Exception as e:
        print(Fore.YELLOW + f"Tidak bisa scroll. Error: {e}" + Style.RESET_ALL)

# =============================================================
# FUNCTION: auto_like_video
# =============================================================
def auto_like_video(driver, filename, xpath, do_scroll=False):
    links = load_file_content(filename)
    for link in links:
        if not link.startswith("http"):
            print(Fore.RED + f"URL tidak valid: {link}" + Style.RESET_ALL)
            continue
        print(Fore.CYAN + f"Menyukai video: {link}" + Style.RESET_ALL)
        try:
            driver.get(link)
        except Exception as e:
            print(Fore.RED + f"Gagal membuka URL: {link}. Error: {e}" + Style.RESET_ALL)
            continue
        delay_with_countdown(random.uniform(10.5, 15.5))
        try:
            if do_scroll:
                auto_scroll(driver)
            like_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            like_button.click()
            print(Fore.GREEN + "Video berhasil di-Like!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Gagal menyukai video! Error: {e}" + Style.RESET_ALL)
        delay_with_countdown(random.uniform(10.5, 15.5))

# =============================================================
# FUNCTION: auto_comment_video_youtube
# (Opsi 3: Auto Comment Video YouTube)
# =============================================================
def auto_comment_video_youtube(driver, video_file, comment_file, placeholder_xpath, input_xpath, do_scroll=False):
    links = load_file_content(video_file)
    comments = load_file_content(comment_file)
    for link in links:
        if not link.startswith("http"):
            print(Fore.RED + f"URL tidak valid: {link}" + Style.RESET_ALL)
            continue
        print(Fore.CYAN + f"Mengomentari video: {link}" + Style.RESET_ALL)
        try:
            driver.get(link)
        except Exception as e:
            print(Fore.RED + f"Gagal membuka URL: {link}. Error: {e}" + Style.RESET_ALL)
            continue
        delay_with_countdown(random.uniform(10.5, 15.5))
        try:
            if do_scroll:
                auto_scroll(driver, distance=300, count=1)
            placeholder = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, placeholder_xpath))
            )
            placeholder.click()
            time.sleep(1)
            comment_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, input_xpath))
            )
            comment = random.choice(comments)
            comment_input.send_keys(comment)
            time.sleep(3)
            comment_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='submit-button']"))
            )
            comment_button.click()
            print(Fore.GREEN + "Komentar berhasil dikirim!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Gagal mengomentari video! Error: {e}" + Style.RESET_ALL)
        delay_with_countdown(random.uniform(10.5, 15.5))

# =============================================================
# FUNCTION: auto_comment_video (Opsi 5: Auto Comment Video Short)
# =============================================================
def auto_comment_video(driver, video_file, comment_file, do_scroll=False):
    links = load_file_content(video_file)
    comments = load_file_content(comment_file)
    for link in links:
        if not link.startswith("http"):
            print(Fore.RED + f"URL tidak valid: {link}" + Style.RESET_ALL)
            continue
        print(Fore.CYAN + f"Mengomentari video Short: {link}" + Style.RESET_ALL)
        try:
            driver.get(link)
        except Exception as e:
            print(Fore.RED + f"Gagal membuka URL: {link}. Error: {e}" + Style.RESET_ALL)
            continue
        delay_with_countdown(random.uniform(10.5, 15.5))
        try:
            if do_scroll:
                auto_scroll(driver, distance=300, count=1)
            comment_logo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='comments-button']"))
            )
            comment_logo.click()
            time.sleep(3)
            placeholder = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='placeholder-area']"))
            )
            placeholder.click()
            time.sleep(3)
            comment_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='contenteditable-root']"))
            )
            comment = random.choice(comments)
            comment_input.send_keys(comment)
            time.sleep(3)
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='submit-button']"))
            )
            send_button.click()
            time.sleep(3)
            print(Fore.GREEN + "Komentar Short berhasil dikirim!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Gagal mengomentari video Short! Error: {e}" + Style.RESET_ALL)
        delay_with_countdown(random.uniform(10.5, 15.5))

# =============================================================
# FUNCTION: auto_subscribe_channel
# (Opsi 6: Auto Subscribe Channel)
# =============================================================
def auto_subscribe_channel(driver, channel_file, xpath):
    channels = load_file_content(channel_file)
    for link in channels:
        if not link.startswith("http"):
            print(Fore.RED + f"URL tidak valid: {link}" + Style.RESET_ALL)
            continue
        print(Fore.CYAN + f"Mengunjungi channel: {link}" + Style.RESET_ALL)
        try:
            driver.get(link)
        except Exception as e:
            print(Fore.RED + f"Gagal membuka URL: {link}. Error: {e}" + Style.RESET_ALL)
            continue
        delay_with_countdown(random.uniform(10.5, 15.5))
        try:
            subscribe_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            subscribe_button.click()
            print(Fore.GREEN + "Berhasil subscribe channel!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Gagal subscribe channel. Error: {e}" + Style.RESET_ALL)
        delay_with_countdown(random.uniform(10.5, 15.5))

# =============================================================
# FUNCTION: main
# =============================================================
def main():
    print_banner()
    while True:
        print(Fore.CYAN + "\nPilih opsi:" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Login manual dan menyimpan sesi di cookies (Gmail & YouTube)" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Auto Like Video/Live streaming YouTube (link di video.txt)" + Style.RESET_ALL)
        print(Fore.GREEN + "3. Auto Comment Video YouTube" + Style.RESET_ALL)
        print(Fore.GREEN + "4. Auto Like Video Short" + Style.RESET_ALL)
        print(Fore.GREEN + "5. Auto Comment Video Short" + Style.RESET_ALL)
        print(Fore.GREEN + "6. Auto Subscribe Channel (link di channel.txt)" + Style.RESET_ALL)
        print(Fore.GREEN + "7. Exit" + Style.RESET_ALL)
        choice = input(Fore.YELLOW + "Masukkan pilihan: " + Style.RESET_ALL)

        if choice == "1":
            account_name = input(Fore.YELLOW + "Masukkan nama akun: " + Style.RESET_ALL)
            print("\033[94m")
            print("""
          ██████╗  ███╗   ███╗ █████╗ ██╗██╗     
         ██╔═══╗ ██ ██╗ ████║██╔══██╗██║██║     
         ██║   ██║██╔████╔██║███████║██║██║     
         ██║   ██║██║╚██╔╝██║██╔══██║██║██║     
         ╚██████╔╝██║ ╚═╝ ██║██║  ██║██║███████╗
          ╚═════╝ ╚═╝     ╚═╝╚═╝  ██║╚═╝╚══════╝
            """)
            print("\033[0m")
            driver = init_chrome_driver_incognito()
            try:
                driver.get("https://accounts.google.com/signin")
            except Exception as e:
                print(Fore.RED + f"Gagal membuka halaman login Gmail. Error: {e}" + Style.RESET_ALL)
                driver.quit()
                continue
            print(Fore.BLUE + "Silakan login ke Gmail secara manual." + Style.RESET_ALL)
            input(Fore.YELLOW + "Tekan Enter jika sudah selesai login di Gmail..." + Style.RESET_ALL)
            try:
                driver.get("https://www.youtube.com")
            except Exception as e:
                print(Fore.RED + f"Gagal membuka YouTube. Error: {e}" + Style.RESET_ALL)
                driver.quit()
                continue
            print(Fore.BLUE + "Sedang menunggu halaman YouTube termuat untuk menyimpan cookies..." + Style.RESET_ALL)
            time.sleep(10)
            save_cookies(driver, account_name)
            driver.quit()

        elif choice in ["2", "3", "4", "5", "6"]:
            mode_select = input(Fore.YELLOW + "Jalankan cookies pernama/perbaris: " + Style.RESET_ALL).strip().lower()
            if mode_select == "pernama":
                account_name = input(Fore.YELLOW + "Masukkan nama akun yang ingin digunakan: " + Style.RESET_ALL)
                selected_accounts = [account_name]
            elif mode_select == "perbaris":
                if not os.path.exists("cookies"):
                    print(Fore.RED + "Folder 'cookies' tidak ditemukan." + Style.RESET_ALL)
                    continue
                all_files = os.listdir("cookies")
                cookies_files = [f for f in all_files if f.startswith("cookies_") and f.endswith(".pkl")]
                cookies_files = sorted(cookies_files)
                if not cookies_files:
                    print(Fore.RED + "Tidak ada file cookies di folder 'cookies'." + Style.RESET_ALL)
                    continue
                print(Fore.CYAN + "Daftar akun cookies:" + Style.RESET_ALL)
                for idx, f in enumerate(cookies_files, start=1):
                    print(f"{idx}. {f}")
                range_input = input(Fore.YELLOW + "Masukkan range (contoh: 1-3) atau satu angka: " + Style.RESET_ALL)
                try:
                    if '-' in range_input:
                        start_str, end_str = range_input.split("-")
                        start_idx, end_idx = int(start_str), int(end_str)
                        if start_idx < 1 or end_idx > len(cookies_files) or start_idx > end_idx:
                            print(Fore.RED + "Range tidak valid." + Style.RESET_ALL)
                            continue
                        selected_files = cookies_files[start_idx-1:end_idx]
                    else:
                        index = int(range_input)
                        if index < 1 or index > len(cookies_files):
                            print(Fore.RED + "Index tidak valid." + Style.RESET_ALL)
                            continue
                        selected_files = [cookies_files[index-1]]
                    selected_accounts = [f[len("cookies_"):-len(".pkl")] for f in selected_files]
                except Exception as e:
                    print(Fore.RED + "Format input tidak valid." + Style.RESET_ALL)
                    continue
            else:
                print(Fore.RED + "Pilihan tidak valid untuk mode cookies." + Style.RESET_ALL)
                continue

            headless_input = input(Fore.YELLOW + "Mode headless diaktifkan (true/false): " + Style.RESET_ALL).strip().lower()
            headless_mode = (headless_input == "true")

            for account in selected_accounts:
                print(Fore.CYAN + f"Menggunakan cookies untuk akun: {account}" + Style.RESET_ALL)
                driver = init_chrome_driver(headless=headless_mode)
                try:
                    driver.get("https://www.youtube.com/")
                except Exception as e:
                    print(Fore.RED + f"Gagal membuka YouTube. Error: {e}" + Style.RESET_ALL)
                    driver.quit()
                    continue
                time.sleep(5)
                load_cookies(driver, account)
                driver.refresh()

                if choice == "2":
                    auto_like_video(driver, "video.txt", "//button[contains(@aria-label, 'like')]", do_scroll=False)
                elif choice == "3":
                    auto_comment_video_youtube(driver, "video.txt", "commentvideo.txt",
                                               "//*[@id='placeholder-area']",
                                               "//*[@id='contenteditable-root']",
                                               do_scroll=True)
                elif choice == "4":
                    auto_like_video(driver, "short.txt", "//button[contains(@aria-label, 'like')]", do_scroll=False)
                elif choice == "5":
                    auto_comment_video(driver, "short.txt", "commentshort.txt", do_scroll=False)
                elif choice == "6":
                    auto_subscribe_channel(driver, "channel.txt", "//*[@id='page-header']/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-flexible-actions-view-model/div/yt-subscribe-button-view-model/yt-animated-action/div[1]/div[2]/button/yt-touch-feedback-shape/div")
                driver.quit()

        elif choice == "7":
            print(Fore.YELLOW + "Keluar..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Pilihan tidak valid, coba lagi!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
