import sys
import subprocess
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.commands import *

def get_latest_release_version(username, repo_name):
    """
    Get the latest release version of a GitHub repository.

    Parameters:
    username (str): The GitHub username.
    repo_name (str): The repository name.

    Returns:
    str: The latest release version, or None if the version could not be determined.
    """
    # Construct the URL for the latest release page
    repo_url = f'https://github.com/{username}/{repo_name}/releases/latest'

    # Send a GET request to the latest release page
    response = requests.get(repo_url, allow_redirects=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the final URL after redirection
        final_url = response.url

        # Extract the version from the final URL
        version = final_url.split('/')[-1]
        return version
    else:
        return None

################## Print color functions ##################
def print_green(text):
    color_start = "\033[0;32m"
    color_end = "\033[00m"
    print(color_start, text, color_end)

def print_red(text):
    color_start = "\033[0;31m"
    color_end = "\033[00m"
    print(color_start, text, color_end)

def print_yellow(text):
    color_start = "\033[0;93m"
    color_end = "\033[00m"
    print(color_start, text, color_end)
################## End Print color functions ##################

################## START functions to install packages ##################

def download_file(url, dest, chunk_size=1024):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(dest, 'wb') as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                downloaded_size += len(data)

        return dest

    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return None


def sparrow_wallet():
    sparrow_v = get_latest_release_version("sparrowwallet", "sparrow")
    sparrow_file = f"sparrow-{sparrow_v}-x86_64.tar.gz"
    try:
        if os.path.exists("shared_with_chroot/" + sparrow_file):
            print_yellow(f"{sparrow_file} already created. Skipping...\n")
            add_script_config(f"\ntar -xvf /tmp/{sparrow_file} -C /opt")
            subprocess.run("cp dotfiles/dotdesktop/sparrow.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/sparrow.desktop /usr/share/applications/")
        else:
            print_green("Downloading...")
            download_file(f"https://github.com/sparrowwallet/sparrow/releases/download/{sparrow_v}/{sparrow_file}",
                          f"shared_with_chroot/{sparrow_file}")
            add_script_config(f"\ntar -xvf /tmp/{sparrow_file} -C /opt")
            subprocess.run("cp dotfiles/dotdesktop/sparrow.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/sparrow.desktop /usr/share/applications/")
    except Exception as e:
        print(f"Error downloading {sparrow_file}: {e}")

def bisq():
    bisq_v = get_latest_release_version("bisq-network", "bisq")
    bisq_file = f"Bisq-64bit-{bisq_v.lstrip('v')}.deb"
    try:
        if os.path.exists("shared_with_chroot/" + bisq_file):
            print_yellow(f"{bisq_file} already created. Skipping...\n")
            add_script_config(f"\ndpkg -i /tmp/{bisq_file}")
            subprocess.run("cp dotfiles/scripts/setup_bisq shared_with_chroot/", shell=True)
            add_script_config("\n/tmp/./setup_bisq")
        else:
            download_file(f"https://github.com/bisq-network/bisq/releases/download/{bisq_v}/{bisq_file}",
                          f"shared_with_chroot/{bisq_file}")
            add_script_config(f"\ndpkg -i /tmp/{bisq_file}")
            subprocess.run("cp dotfiles/scripts/setup_bisq shared_with_chroot/", shell=True)
            add_script_config("\n/tmp/./setup_bisq")
    except Exception as e:
        print(f"Error downloading {bisq_file}: {e}")

def briar():
    briar_file = f"briar-desktop-debian-bullseye.deb"
    try:
        if os.path.exists("shared_with_chroot/" + briar_file):
            print_yellow(f"{briar_file} already created. Skipping...\n")
            add_script_config(f"\ndpkg -i /tmp/{briar_file}")
        else:
            download_file(f"https://debian.briarproject.org/pool/main/b/briar-desktop/briar-desktop_1.2.6_amd64.deb",
                          f"shared_with_chroot/{briar_file}")
            add_script_config(f"\ndpkg -i /tmp/{briar_file}")
    except Exception as e:
        print(f"Error downloading/installing {briar_file}: {e}")

def simplex_chat():
    simplex_v = get_latest_release_version("simplex-chat", "simplex-chat")
    simplex_file = "simplex-desktop-ubuntu-20_04-x86_64.deb"
    try:
        if os.path.exists("shared_with_chroot/" + simplex_file):
            print_yellow(f"{simplex_file} already created. Skipping...\n")
            add_script_config(f"\ndpkg -i /tmp/{simplex_file}")
        else:
            download_file(f"https://github.com/simplex-chat/simplex-chat/releases/download/{simplex_v}/{simplex_file}",
                          f"shared_with_chroot/{simplex_file}")
            add_script_config(f"\ndpkg -i /tmp/{simplex_file}")
    except Exception as e:
        print(f"Error downloading/installing {simplex_file}: {e}")

def bip39_iancoleman():
    bip39_iancoleman_v = get_latest_release_version("iancoleman", "bip39")
    bip39_iancoleman_file = "bip39-standalone.html"
    try:
        if os.path.exists("shared_with_chroot/" + bip39_iancoleman_file):
            subprocess.run("cp dotfiles/dotdesktop/bip39ian.desktop shared_with_chroot/", shell=True)
            add_script_config("\nmkdir /etc/skel/Tor\\ Browser/")
            add_script_config("\ncp /tmp/bip39ian.desktop /usr/share/applications/")
            add_script_config(f"\ncp /tmp/{bip39_iancoleman_file} /etc/skel/Tor\\ Browser/")
        else:
            download_file(f"https://github.com/iancoleman/bip39/releases/download/{bip39_iancoleman_v}/{bip39_iancoleman_file}",
                          f"shared_with_chroot/{bip39_iancoleman_file}")
            subprocess.run("cp dotfiles/dotdesktop/bip39ian.desktop shared_with_chroot/", shell=True)
            add_script_config("\nmkdir /etc/skel/Tor\\ Browser/")
            add_script_config("\ncp /tmp/bip39ian.desktop /usr/share/applications/")
            add_script_config(f"\ncp /tmp/{bip39_iancoleman_file} /etc/skel/Tor\\ Browser/")
    except Exception as e:
        print(f"Error downloading BIP39 {bip39_iancoleman_file}: {e}")

def seedtool():
    seedtool_v = get_latest_release_version("BitcoinQnA", "seedtool")
    seedtool_file = "index.html"
    try:
        if os.path.exists("shared_with_chroot/" + seedtool_file):
            subprocess.run("cp dotfiles/dotdesktop/seedtool.desktop shared_with_chroot/", shell=True)
            add_script_config("\nmkdir /etc/skel/Tor\\ Browser/")
            add_script_config("\nmkdir /opt/logos/")
            subprocess.run("cp dotfiles/logos/seedtool.png shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/seedtool.png /opt/logos/")
            add_script_config("\ncp /tmp/seedtool.desktop /usr/share/applications/")
            add_script_config(f"\ncp /tmp/{seedtool_file} /etc/skel/Tor\\ Browser/")
        else:
            download_file(f"https://github.com/BitcoinQnA/seedtool/releases/download/{seedtool_v}/{seedtool_file}",
                          f"shared_with_chroot/{seedtool_file}")
            subprocess.run("cp dotfiles/dotdesktop/seedtool.desktop shared_with_chroot/", shell=True)
            add_script_config("\nmkdir /etc/skel/Tor\\ Browser/")
            add_script_config("\nmkdir /opt/logos/")
            subprocess.run("cp dotfiles/logos/seedtool.png shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/seedtool.png /opt/logos/")
            add_script_config("\ncp /tmp/seedtool.desktop /usr/share/applications/")
            add_script_config(f"\ncp /tmp/{seedtool_file} /etc/skel/Tor\\ Browser/")
    except Exception as e:
        print(f"Error downloading {seedtool_file}: {e}")

def border_wallets():
    border_wallets_v = get_latest_release_version("microchad", "borderwallets")
    border_wallets_file = "borderwallets.html"
    try:
        if os.path.exists("shared_with_chroot/" + border_wallets_file):
            install_border_wallets()
        else:
            download_file(f"https://github.com/microchad/borderwallets/releases/download/{border_wallets_v}/{border_wallets_file}",
                          f"shared_with_chroot/{border_wallets_file}")
            subprocess.run("cp dotfiles/dotdesktop/borderwallet.desktop shared_with_chroot/", shell=True)
            add_script_config("\nmkdir /etc/skel/Tor\\ Browser/")
            add_script_config("\nmkdir /opt/logos/")
            subprocess.run("cp dotfiles/logos/borderwallet.svg shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/borderwallet.svg /opt/logos/")
            add_script_config("\ncp /tmp/borderwallet.desktop /usr/share/applications/")
            add_script_config(f"\ncp /tmp/{border_wallets_file} /etc/skel/Tor\\ Browser/")
    except Exception as e:
        print(f"Error downloading {border_wallets_file}: {e}")

def specter_desktop():
    specter_v = get_latest_release_version("cryptoadvance", "specter-desktop")
    specterd_v = specter_v
    specter_file = f"specter_desktop-{specter_v}.tar.gz"
    try:
        if os.path.exists("shared_with_chroot/" + specter_file):
            print_green(f"Downloading {specter_file} ...")
            add_script_config(f"\ncd /tmp/ ; tar -zxvf {specter_file} --wildcards *.AppImage")
            add_script_config("\nmkdir /opt/specter/")
            download_file(f"https://raw.githubusercontent.com/cryptoadvance/specter-desktop/72fed92dd5d00e3164adcc97decf5ae03328538a/src/cryptoadvance/specter/static/img/v1-icons/icon.png",
                          f"shared_with_chroot/specter_logo.png")
            add_script_config("\ncp /tmp/specter_logo.png /opt/specter/logo.png")
            add_script_config("\ncp /tmp/Specter-*.AppImage /opt/specter/Specter.AppImage")
            add_script_config("\ncp /tmp/udev/*.rules /etc/udev/rules.d/")
            print_green("Downloading specterd...")
            download_file(f"https://github.com/cryptoadvance/specter-desktop/releases/download/{specterd_v}.zip",
                          f"shared_with_chroot/{specterd_v}.zip")
            add_script_config("\nmkdir -p /etc/skel/.specter/specterd-binaries/")
            subprocess.run(f"sudo unzip shared_with_chroot/{specterd_v}.zip -d shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/specterd /etc/skel/.specter/specterd-binaries/")
            add_script_config("\nmkdir /etc/skel/.fonts/")
            download_file(f"https://raw.githubusercontent.com/googlefonts/noto-emoji/main/fonts/NotoColorEmoji.ttf",
                          f"shared_with_chroot/NotoColorEmoji.ttf")
            add_script_config("\ncp /tmp/NotoColorEmoji.ttf /etc/skel/.fonts/NotoColorEmoji.ttf")
            subprocess.run("cp dotfiles/dotconf/ferm_specter.conf shared_with_chroot/", shell=True)
            add_script_config("\nmv /tmp/ferm_specter.conf /etc/ferm/ferm.conf")
            subprocess.run("cp dotfiles/dotdesktop/specter.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/specter.desktop /usr/share/applications/")
        else:
            download_file(f"https://github.com/cryptoadvance/specter-desktop/releases/download/{specter_v}/{specter_file}",
                          f"shared_with_chroot/{specter_file}")
            add_script_config(f"\ncd /tmp/ ; tar -zxvf {specter_file} --wildcards *.AppImage")
            add_script_config("\nmkdir /opt/specter/")
            download_file(f"https://raw.githubusercontent.com/cryptoadvance/specter-desktop/72fed92dd5d00e3164adcc97decf5ae03328538a/src/cryptoadvance/specter/static/img/v1-icons/icon.png",
                          f"shared_with_chroot/specter_logo.png")
            add_script_config("\ncp /tmp/specter_logo.png /opt/specter/logo.png")
            add_script_config("\ncp /tmp/Specter-*.AppImage /opt/specter/Specter.AppImage")
            add_script_config("\ncp /tmp/udev/*.rules /etc/udev/rules.d/")
            print_green("Downloading specterd...")
            download_file(f"https://github.com/cryptoadvance/specter-desktop/releases/download/{specterd_v}.zip",
                          f"shared_with_chroot/{specterd_v}.zip")
            add_script_config("\nmkdir -p /etc/skel/.specter/specterd-binaries/")
            subprocess.run(f"sudo unzip shared_with_chroot/{specterd_v}.zip -d shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/specterd /etc/skel/.specter/specterd-binaries/")
            add_script_config("\nmkdir /etc/skel/.fonts/")
            download_file(f"https://raw.githubusercontent.com/googlefonts/noto-emoji/main/fonts/NotoColorEmoji.ttf",
                          f"shared_with_chroot/NotoColorEmoji.ttf")
            add_script_config("\ncp /tmp/NotoColorEmoji.ttf /etc/skel/.fonts/NotoColorEmoji.ttf")
            subprocess.run("cp dotfiles/dotconf/ferm_specter.conf shared_with_chroot/", shell=True)
            add_script_config("\nmv /tmp/ferm_specter.conf /etc/ferm/ferm.conf")
            subprocess.run("cp dotfiles/dotdesktop/specter.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/specter.desktop /usr/share/applications/")
    except Exception as e:
        print(f"Error downloading {specter_file}: {e}")

def mycitadel_desktop():
    mycitadel_v = get_latest_release_version("mycitadel", "mycitadel-desktop")
    mycitadel_file = f"mycitadel_{mycitadel_v.lstrip('v')}_debian11_amd64.deb"
    try:
        if os.path.exists("shared_with_chroot/" + mycitadel_file):
            add_script_config(f"\ndpkg -i /tmp/{mycitadel_file}")
            subprocess.run("cp dotfiles/dotdesktop/io.mycitadel.Wallet.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/io.mycitadel.Wallet.desktop /usr/share/applications/")
        else:
            download_file(f"https://github.com/mycitadel/mycitadel-desktop/releases/download/{mycitadel_v}/{mycitadel_file}",
                          f"shared_with_chroot/{mycitadel_file}")
            add_script_config(f"\ndpkg -i /tmp/{mycitadel_file}")
            subprocess.run("cp dotfiles/dotdesktop/io.mycitadel.Wallet.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/io.mycitadel.Wallet.desktop /usr/share/applications/")
    except Exception as e:
        print(f"Error downloading {mycitadel_file}: {e}")

def rana_nostr_pubkeys_mining_tool():
    rana_v = get_latest_release_version("grunch", "rana")
    rana_file = "rana-x86_64-unknown-linux-musl.tar.gz"
    try:
        if os.path.exists("shared_with_chroot/" + rana_file):
            add_script_config("\nmkdir -p /opt/rana/")
            add_script_config(f"\ntar xvf /tmp/{rana_file} -C /opt/rana/ --strip-components=1")
            subprocess.run("cp dotfiles/dotdesktop/rana.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/rana.desktop /usr/share/applications/")
            subprocess.run("cp dotfiles/logos/rana.png shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/rana.png /opt/rana/")
            add_script_config("\nln -s /opt/rana/rana /usr/bin")
        else:
            download_file(f"https://github.com/grunch/rana/releases/download/{rana_v}/{rana_file}",
                          f"shared_with_chroot/{rana_file}")
            add_script_config("\nmkdir -p /opt/rana/")
            add_script_config(f"\ntar xvf /tmp/{rana_file} -C /opt/rana/ --strip-components=1")
            subprocess.run("cp dotfiles/dotdesktop/rana.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/rana.desktop /usr/share/applications/")
            subprocess.run("cp dotfiles/logos/rana.png shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/rana.png /opt/rana/")
            add_script_config("\nln -s /opt/rana/rana /usr/bin")
    except Exception as e:
        print(f"Error downloading {rana_file}: {e}")

def hodl_hodl_and_robosats():
    try:
        subprocess.run("cp dotfiles/dotdesktop/robosats.desktop shared_with_chroot/", shell=True)
        subprocess.run("cp dotfiles/dotdesktop/hodlhodl.desktop shared_with_chroot/", shell=True)
        add_script_config("\ncp /tmp/robosats.desktop /usr/share/applications/")
        add_script_config("\ncp /tmp/hodlhodl.desktop /usr/share/applications/")
        add_script_config("\nmkdir /opt/logos/")
        subprocess.run("cp dotfiles/logos/robosats.png shared_with_chroot/", shell=True)
        subprocess.run("cp dotfiles/logos/hodlhodl.png shared_with_chroot/", shell=True)
        add_script_config("\ncp /tmp/robosats.png /opt/logos/")
        add_script_config("\ncp /tmp/hodlhodl.png /opt/logos/")
    except Exception as e:
        print(f"Error downloading Hodl Hodl and Robosats: {e}")

def nostr_web_clients():
    try:
        subprocess.run("cp dotfiles/dotdesktop/snort.desktop shared_with_chroot/", shell=True)
        subprocess.run("cp dotfiles/dotdesktop/iris_to.desktop shared_with_chroot/", shell=True)
        add_script_config("\ncp /tmp/snort.desktop /usr/share/applications/")
        add_script_config("\ncp /tmp/iris_to.desktop /usr/share/applications/")
        add_script_config("\nmkdir /opt/logos/")
        subprocess.run("cp dotfiles/logos/snort.png shared_with_chroot/", shell=True)
        subprocess.run("cp dotfiles/logos/iris_to.png shared_with_chroot/", shell=True)
        add_script_config("\ncp /tmp/snort.png /opt/logos/")
        add_script_config("\ncp /tmp/iris_to.png /opt/logos/")
    except Exception as e:
        print(f"Error downloading Nostr Web Clients: {e}")

def mempool_space():
    try:
        subprocess.run("cp dotfiles/dotdesktop/mempool_space.desktop shared_with_chroot/", shell=True)
        add_script_config("\ncp /tmp/mempool_space.desktop /usr/share/applications/")
        add_script_config("\nmkdir /opt/logos/")
        subprocess.run("cp dotfiles/logos/mempool_space.png shared_with_chroot/", shell=True)
        add_script_config("\ncp /tmp/mempool_space.png /opt/logos/")
    except Exception as e:
        print(f"Error downloading Mempool Space: {e}")

def bitcoin_core():
    bitcoincore_v = get_latest_release_version("bitcoin", "bitcoin")
    bitcoincore_file = f"bitcoin-{bitcoincore_v.lstrip('v')}-x86_64-linux-gnu.tar.gz"
    try:
        if os.path.exists("shared_with_chroot/" + bitcoincore_file):
            print_yellow(f"{bitcoincore_file} already created. Skipping...\n")
            add_script_config("\nmkdir -p /opt/bitcoin/")
            add_script_config("\ncp /tmp/bitcoin256.png /opt/bitcoin/bitcoin256.png")
            add_script_config(f"\ntar xzf /tmp/{bitcoincore_file} -C /opt/bitcoin --strip-components=1")
            subprocess.run("cp dotfiles/dotdesktop/bitcoincore.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/bitcoincore.desktop /usr/share/applications/")
        else:
            print_green("Downloading...")
            download_file(f"https://bitcoincore.org/bin/bitcoin-core-{bitcoincore_v}/{bitcoincore_file}",
                          f"shared_with_chroot/{bitcoincore_file}")
            download_file(f"https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/pixmaps/bitcoin256.png",
                          f"shared_with_chroot/bitcoin256.png")
            add_script_config("\nmkdir -p /opt/bitcoin/")
            add_script_config("\ncp /tmp/bitcoin256.png /opt/bitcoin/bitcoin256.png")
            add_script_config(f"\ntar xzf /tmp/{bitcoincore_file} -C /opt/bitcoin --strip-components=1")
            subprocess.run("cp dotfiles/dotdesktop/bitcoincore.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/bitcoincore.desktop /usr/share/applications/")
    except Exception as e:
        print(f"Error downloading {bitcoincore_file}: {e}")

def feather_wallet():
    feather_v = get_latest_release_version("feather-wallet", "feather")
    feather_file = f"feather-{feather_v}-a.AppImage"
    try:
        if os.path.exists("shared_with_chroot/" + feather_file):
            print_yellow(f"{feather_file} already created. Skipping...\n")
            add_script_config("\nmkdir -p /opt/feather/")
            add_script_config("\ncp /tmp/feather.png /opt/feather/feather.png")
            add_script_config(f"\ncp /tmp/{feather_file} /opt/feather/feather.AppImage")
            subprocess.run("cp dotfiles/dotdesktop/featherwallet.desktop shared_with_chroot/", shell=True)
            add_script_config("\nchmod +x /opt/feather/feather.AppImage")
            add_script_config("\ncp /tmp/featherwallet.desktop /usr/share/applications/")
        else:
            print_green("Downloading...")
            download_file(f"https://featherwallet.org/files/releases/linux-appimage-a/{feather_file}",
                          f"shared_with_chroot/{feather_file}")
            download_file(f"https://featherwallet.org/img/feather.png",
                          f"shared_with_chroot/feather.png")
            add_script_config("\nmkdir -p /opt/feather/")
            add_script_config("\ncp /tmp/feather.png /opt/feather/feather.png")
            add_script_config(f"\ncp /tmp/{feather_file} /opt/feather/feather.AppImage")
            subprocess.run("cp dotfiles/dotdesktop/featherwallet.desktop shared_with_chroot/", shell=True)
            add_script_config("\nchmod +x /opt/feather/feather.AppImage")
            add_script_config("\ncp /tmp/featherwallet.desktop /usr/share/applications/")
    except Exception as e:
        print(f"Error downloading {feather_file}: {e}")

def cake_wallet():
    cake_v = get_latest_release_version("cake-tech", "cake_wallet")
    cake_file = f"Cake_Wallet_{cake_v}_Linux.tar.xz"
    try:
        if os.path.exists("shared_with_chroot/" + cake_file):
            print_yellow(f"{cake_file} already created. Skipping...\n")
            add_script_config("\nmkdir -p /opt/cakewallet/")
            add_script_config(f"\ntar xf /tmp/{cake_file} -C /opt/cakewallet --strip-components=1")
            subprocess.run("cp dotfiles/dotdesktop/cakewallet.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/cakewallet.desktop /usr/share/applications/")
        else:
            print_green("Downloading...")
            download_file(f"https://github.com/cake-tech/cake_wallet/releases/download/{cake_v}/{cake_file}",
                          f"shared_with_chroot/{cake_file}")
            add_script_config("\nmkdir -p /opt/cakewallet/")
            add_script_config(f"\ntar xf /tmp/{cake_file} -C /opt/cakewallet --strip-components=1")
            subprocess.run("cp dotfiles/dotdesktop/cakewallet.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/cakewallet.desktop /usr/share/applications/")
    except Exception as e:
        print(f"Error downloading {cake_file}: {e}")

def liana_wallet():
    liana_v = get_latest_release_version("wizardsardine", "liana")
    liana_file = f"liana-{liana_v.lstrip('v')}-x86_64-linux-gnu.tar.gz"
    try:
        if os.path.exists("shared_with_chroot/" + liana_file):
            print_yellow(f"{liana_file} already created. Skipping...\n")
            add_script_config(f"\ntar -xvf /tmp/{liana_file} -C /opt")
            subprocess.run("cp dotfiles/dotdesktop/liana.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/liana.desktop /usr/share/applications/")
        else:
            print_green("Downloading...")
            download_file(f"https://github.com/wizardsardine/liana/releases/download/{liana_v}/{liana_file}",
                          f"shared_with_chroot/{liana_file}")
            add_script_config(f"\nmkdir /opt/liana/ && tar -xvf /tmp/{liana_file} -C /opt/liana/ --strip-components 1")
            subprocess.run("cp dotfiles/logos/liana.svg shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/liana.svg /opt/liana/")
            subprocess.run("cp dotfiles/dotdesktop/liana.desktop shared_with_chroot/", shell=True)
            add_script_config("\ncp /tmp/liana.desktop /usr/share/applications/")
    except Exception as e:
        print(f"Error downloading {liana_file}: {e}")

################## END functions to install packages ##################
################## START functions to remove packages ##################
def thunderbird():
    try:
        add_script_config("\ndpkg -r --force-depends thunderbird")
    except Exception as e:
        print(f"Error removing Thunderbird: {e}")

def gimp():
    try:
        add_script_config("\ndpkg -r --force-depends gimp")
    except Exception as e:
        print(f"Error removing Gimp: {e}")

################## END functions to remove packages ##################

def add_script_config(text):
    try:
        if not os.path.exists("shared_with_chroot"):
            subprocess.run("mkdir shared_with_chroot", shell=True)

        with open("shared_with_chroot/script", "a") as config_script_file:
            config_script_file.write(text)
    except Exception as e:
        print(f"Error adding script config: {e}")

def add_menu():
    try:
        subprocess.run("cp dotfiles/menu/Bitcoin.menu shared_with_chroot/", shell=True)
        subprocess.run("cp dotfiles/menu/Nostr.menu shared_with_chroot/", shell=True)
        subprocess.run("cp dotfiles/menu/Monero.menu shared_with_chroot/", shell=True)
        add_script_config("\ncp /tmp/Bitcoin.menu /etc/xdg/menus/applications-merged/")
        add_script_config("\ncp /tmp/Nostr.menu /etc/xdg/menus/applications-merged/")
        add_script_config("\ncp /tmp/Monero.menu /etc/xdg/menus/applications-merged/")
    except Exception as e:
        print(f"Error adding menu: {e}")

############################################
