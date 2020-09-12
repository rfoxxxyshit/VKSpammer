import random, time, vk_api

print("""\n██╗   ██╗██╗  ██╗    ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
██║   ██║██║ ██╔╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
██║   ██║█████╔╝     ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
╚██╗ ██╔╝██╔═██╗     ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
 ╚████╔╝ ██║  ██╗    ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
  ╚═══╝  ╚═╝  ╚═╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝\n""")

time.sleep(3);
vk_login = input('[Auth] Login: ');
vk_password = input('[Auth] Password: ')
vk_session = vk_api.VkApi(vk_login, vk_password)
vkapi, rucaptcha = 'api.vk.com', 'rucaptcha.com'
try:
    print('\n[Auth] Вхожу...'); vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
get_me = vk_session.method('users.get')[0]
full_name = f'{get_me["first_name"]} {get_me["last_name"]}'
vk_id = get_me['id'];
token = dict(vk_session.token)['access_token']
print(f"[Auth] Успешно вошел! {full_name} ({vk_id})")
users = list()
print('\n[Spammer] Собираю список пользователь(ей)...')
for a in vk_session.method('messages.getConversations', {"count": 200,
                                                         "type": "all"})['items']:
    if a['conversation']['peer']['type'] != 'user':
        continue
    users.append(a['conversation']['peer']['id'])
for a in vk_session.method('friends.get')['items']:
    if a not in users:
        users.append(a)

print(f'[Spammer] Загружено {len(users)} пользователей.')
print('\n[Spammer] Загружаю текст рассылки из файла "input.txt"...')
with open('input.txt', 'r', encoding='utf8') as f:
    text = f.read()
print('[Spammer] Текст рассылки загружен: \n' + text)
if input('\n[Spammer] Подтвердите рассылку (Y/n): ') != 'Y':
    exit(0)
random.shuffle(users)
sent = 0
not_sent = 0
for user in users:
    try:
        vk_session.method('messages.send', {'user_id': user, 'message': text,
                                            'random_id': random.randint(10000, 10000000000)})
        to_user = vk_session.method('users.get', {"user_ids": user})[0]
        to_user_first_name = to_user['first_name']
        to_user_last_name = to_user['last_name']
        to_user_full_name = to_user_first_name + ' ' + to_user_last_name
        sent += 1
        print(f'[{to_user_full_name}] Отправлено! ({sent}/{not_sent})')
        time.sleep(5)
    except (BaseException, Exception):
        to_user = vk_session.method('users.get', {"user_ids": user})[0]
        to_user_first_name = to_user['first_name']
        to_user_last_name = to_user['last_name']
        to_user_full_name = to_user_first_name + ' ' + to_user_last_name
        not_sent += 1
        print(f'[{to_user_full_name}] Не отправлено! ({sent}/{not_sent})')
        time.sleep(15)

print(f'\n[Spammer] Рассылка окончена!\n\n[Spammer] Успешно отправлено - {sent}\n[Spammer] '
      f'Неудачно отправлено - {not_sent}')
