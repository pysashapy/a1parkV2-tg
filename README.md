# Telegram Bot and Settings Server

## Installation

### Установка и настройка Git
```bash
sudo apt-get install git
git config --global user.name your_github_username
git config --global user.email your_github_email
```

### Получение персонального токена на GitHub
Settings => Developer Settings => Personal Access Token => Generate New Token (Give your password) => Fillup the form => click Generate token => Copy the generated Token, it will be something like ghp_sFhFsSHhTzMDreGRLjmks4Tzuzgthdvfsrta

Используйте токен вместо пароля при клонирование репозитория 

### Клонирование репозитория
```bash
cd ~
git clone https://github.com/pysashapy/a1parkV2-tg.git
cd a1parkV2-tg
```

### Установка библиотек

python3 >= 3.7

```bash
sudo apt-get install python3-pip
sudo pip3 install -r req.txt
```
## Основные настройки
### Время
```bash
sudo timedatectl set-timezone 'Europe/Moscow'
```

## Настройка Сервера

```bash
cd a1parkV2-tg/server
chmod +x install.sh
./install.sh
```
Помере продвижения спросит IP, PORT а так же данные для создание Профиля Администратора.
http://IP:PORT/admin

## Настройка Бота
```bash
nano ~/a1parkV2-tg/server/bot/settings.py
```

В файле settings.py должно быть: 
```python
url_django_tg_server = 'http://IP:PORT/'  # url:port которые вводили при настройке сервера
tg_secret_key = 'TOKEN BOT'
```

### Автостарт Бота
```bash
cd ~/a1parkV2-tg/server/bot
sudo cp tg.service /etc/systemd/system/
sudo systemctl enable tg
sudo systemctl start tg
sudo reboot
```

