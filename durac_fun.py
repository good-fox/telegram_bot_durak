import shelve
from APY import shelve_game
from random import shuffle
from telebot import types


#def add_coloda(message):
#    """
#    Записуємо колоду в храніліще
#    """
#    with shelve.open(shelve_game) as storage:
#        storage['coloda'] = message.text

def get_coloda():
    """
    Полулаємо колоду із храніліща
    :return: (str) Колода 36 карт
    """
#    with shelve.open(shelve_game) as storage:
    coloda = '6♥️,7♥️,8♥️,9♥️,10♥️,V♥️,D♥️,K♥️,T♥️,6♠️,7♠️,8♠️,9♠️,10♠️,V♠️,D♠️,K♠️,T♠️,6♦️,7♦️,8♦️,9♦️,10♦️,V♦️,D♦️,K♦️,T♦️,6♣️,7♣️,8♣️,9♣️,10♣️,V♣️,D♣️,K♣️,T♣️' #storage['coloda']
    coloda_demo = '6♥️,7♥️,8♥️,9♥️,6♠️,7♠️,8♠️,9♠️,6♦️,7♦️,8♦️,9♦️,6♣️,7♣️,8♣️,9♣️'
    list_coloda = []
    for card in coloda.split(','):
        list_coloda.append(card)
    shuffle(list_coloda)
    return list_coloda

def get_str_coloda(list):

    str = ''
    print('Прийшла список ', list)
    for item in list:
        str += '{},'.format(item)
    return str

def get_list_coloda(str):

    list = []
    print('Прийшла строка ', str)
    if str != None:
        for item in str.split(','):
            list.append(item)
        list.pop()
    return list


def get_min_cozer(arm, cozer):

    mast = cozer[-2]
    print('Козер у нас такої масті: ', mast)
    list = []
    for card in arm:
        if card[-2] == mast:
            print('Карта яку порівнюєм у нас такої масті: ', card[-2])
            if card[0] == '6':
                list.append(1)
            elif card[0] == '7':
                list.append(2)
            elif card[0] == '8':
                list.append(3)
            elif card[0] == '9':
                list.append(4)
            elif card[0] == '1':
                list.append(5)
            elif card[0] == 'V':
                list.append(6)
            elif card[0] == 'D':
                list.append(7)
            elif card[0] == 'K':
                list.append(8)
            elif card[0] == 'T':
                list.append(9)
    if list == []:
        list.append(10)
    list.sort()
    return list[0]


def get_data (key, id):
    try:
        with shelve.open(shelve_game) as storage:
            data = storage['{}:{}'.format(key, id)]
        return data
    except KeyError:
        print('Error from get_data')

def set_data (key, id, data):
    try:
        with shelve.open(shelve_game) as storage:
            if data != '0':
                storage['{}:{}'.format(key, id)] = data
            else:
                del storage['{}:{}'.format(key, id)]
    except KeyError:
        print('Error from set_data')


def del_game(id1, id2):
    set_data('game', id1, '0')
    set_data('game', id2, '0')

    set_data('game_all_coloda', id1, '0')
    set_data('game_all_coloda', id2, '0')

    set_data('game_cozer', id1, '0')
    set_data('game_cozer', id2, '0')

    set_data('game_arm', id1, '0')
    set_data('game_arm', id2, '0')

    set_data('game_hid', id1, '0')
    set_data('game_hid', id2, '0')

    set_data('game_hid_status', id1, '0')
    set_data('game_hid_status', id2, '0')

    set_data('game_hid_status_cards', id1, '0')
    set_data('game_hid_status_cards', id2, '0')

    set_data('game_hid_status_fite', id1, '0')
    set_data('game_hid_status_fite', id2, '0')

    set_data('game_hid_status_all_fite', id1, '0')
    set_data('game_hid_status_all_fite', id2, '0')


def set_user_add_game(chat_id):
    """
    Записуємо що юзер створив гру і йому мають відповісти по його id 
    :param chat_id: id юзера
    :return: (str)    
    """
    text1 = 'Ви вже створили гру очікуйте, ваш id: {}, щоб удалити її скористайтесь командою /end_game'.format(chat_id)
    text2 = 'Надішліць цей id користувачу з яким хочете зіграти: {}'.format(chat_id)

    with shelve.open(shelve_game) as storage:
        try:
            if storage[str(chat_id)] == 'add_game':
                return text1
            else:
                storage[str(chat_id)] = 'add_game'
                return text2
        except KeyError:
            storage[str(chat_id)] = 'add_game'
            return text2

def set_user_end_game(chat_id):
    """
    Записуємо що юзер створив гру і йому мають відповісти по його id 
    :param chat_id: id юзера
    :return: (str)
    """
    text1 = 'Вашу гру успішно видалено'
    text2 = 'Ви не створювали гру, щоб удалити, створіть спочатку її, це можна зробити командою /add_game'

    with shelve.open(shelve_game) as storage:
        try:
            if storage[str(chat_id)] == 'add_game':
                del storage[str(chat_id)]
                return text1
            else:
                return text2
        except KeyError:
            return text2


def set_user_start_game(chat_id, game_id = 0):
    """
    Додаємо юзера до створеної гри по id яке він нам передає 
    :param chat_id: id юзера
    :param game_id: id юзера який створив гру
    :return: (str)    
    """
    text0 = 'До вашої гри підключились, ведіть команду /start_game для запуску гри'
    text1 = 'Ви підключились до гри, очікуйте...'
    text2 = 'По заданому id гри не знайдено, спробуйте інший id'

    with shelve.open(shelve_game) as storage:
        try:
            if storage[str(game_id)] == 'add_game':
                storage['game:{}'.format(game_id)] = str(chat_id)
                storage['game:{}'.format(chat_id)] = str(game_id)
                return text1, True, text0

        except KeyError:
            return text2, False, None


def get_start_game_for_user(chat_id):
    """
    Получаєм початкові дані з гри для даного юзера та його опонента.
    У випадку якщо юзер не почав гру, вертаємо None
    :param chat_id: id юзера
    :return: (list) початкові дані / None
    """
    with shelve.open(shelve_game) as storage:
        try:

            print('Бот починає гру')

            if storage[str(chat_id)] == 'add_game':
                print('Я зайшов у першу функцію')
                user_id = storage['game:{}'.format(chat_id)]
                print('Я получив id противника')
                all_coloda = get_coloda()
                print('Дані є, колода потасована')
                arm1 = []
                arm2 = []
                for i in range(6):
                    arm1.append(all_coloda.pop())
                    arm2.append(all_coloda.pop())
                list = [get_str_coloda(arm1), get_str_coloda(arm2), user_id, len(all_coloda), all_coloda[0]]

                storage['game_all_coloda:{}'.format(chat_id)] = get_str_coloda(all_coloda)
                storage['game_all_coloda:{}'.format(user_id)] = get_str_coloda(all_coloda)

                storage['game_cozer:{}'.format(chat_id)] = all_coloda[0]
                storage['game_cozer:{}'.format(user_id)] = all_coloda[0]

                storage['game_arm:{}'.format(chat_id)] = get_str_coloda(arm1)
                storage['game_arm:{}'.format(user_id)] = get_str_coloda(arm2)

                storage['game_hid:{}'.format(chat_id)] = '0'
                storage['game_hid_status:{}'.format(chat_id)] = 'hid'
                storage['game_hid:{}'.format(user_id)] = '0'
                storage['game_hid_status:{}'.format(user_id)] = 'hid'

                hid1 = get_min_cozer(arm1, all_coloda[0])
                hid2 = get_min_cozer(arm2, all_coloda[0])

                if hid1 <= hid2:
                    storage['game_hid:{}'.format(chat_id)] = '1'
                    storage['game_hid_status:{}'.format(user_id)] = 'fite'
                    storage['game_hid_status_cards:{}'.format(chat_id)] = '6,7,8,9,1,V,D,K,T,'
                    print('Ходить перший гравець його id: ', chat_id)
#                    storage['game_hid_status_fite:{}'.format(chat_id)] = '0'
                else:
                    storage['game_hid:{}'.format(user_id)] = '1'
                    storage['game_hid_status:{}'.format(chat_id)] = 'fite'
                    storage['game_hid_status_cards:{}'.format(user_id)] = '6,7,8,9,1,V,D,K,T,'
                    print('Ходить другий гравець його id: ', user_id)
#                    storage['game_hid_status_fite:{}'.format(user_id)] = '0'

                return list
            print('Я не зайшов у першу функцію')
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None



def get_game_for_user(chat_id, text):
    """
    Получаєм дані з гри для даного юзера та його опонента.
    У випадку якщо юзер не почав гру, вертаємо None
    :param chat_id: id юзера
    :param text: message юзера
    :return: (str) дані / None
    """
#    with shelve.open(shelve_game) as storage:
    try:
            print('game_id:', chat_id)
            print('game_hid:', get_data('game_hid', chat_id))
            print('game_hid_status:', get_data('game_hid_status', chat_id))

            if get_data('game_hid', chat_id) == '1':

                if get_data('game_hid_status', chat_id) == 'hid':

                    if set_hid_for_user(chat_id, text):
                        id = get_data('game', chat_id)
#                        set_data('game_hid_status', chat_id, 'fite')
                        print('Хід принято вертаю текст: {}, по id: {}'.format(text, id))

                        str_temp = get_data('game_all_coloda', chat_id)
                        list_temp = get_list_coloda(str_temp)

                        str_arm = get_data('game_arm', chat_id)
                        list_arm = get_list_coloda(str_arm)

                        if len(list_temp) == 0 and len(list_arm) == 0:
                            text = '{}, Ти програв!!!'.format(text)
                            del_game(chat_id, id)

                        return id, text 

                    elif text == '⚔️':
                        print('Користувач нажав бій!')

                        id = get_data('game', chat_id)
                        set_data('game_hid', chat_id, '0')
                        set_data('game_hid', id, '1')
                        set_data('game_hid_status', chat_id, 'fite')
                        set_data('game_hid_status', id, 'hid')

                        set_data('game_hid_status_cards', id, '6,7,8,9,1,V,D,K,T,')

                        str_temp = get_data('game_all_coloda', chat_id)
                        list_temp = get_list_coloda(str_temp)

                        list_arm = get_list_coloda(get_data('game_arm', chat_id))

                        while len(list_arm) < 6 and len(list_temp) != 0:
                            list_arm.append(list_temp.pop())
                        
                        set_data('game_arm', chat_id, get_str_coloda(list_arm))

                        list_arm = get_list_coloda(get_data('game_arm', id))

                        while len(list_arm) < 6 and len(list_temp) != 0:
                            list_arm.append(list_temp.pop())
                        
                        set_data('game_arm', id, get_str_coloda(list_arm))

                        text = '⚔️ _ {}  🀄️ - {}'.format(get_data('game_cozer', id), len(list_temp))

                        set_data('game_all_coloda', chat_id, get_str_coloda(list_temp))
                        set_data('game_all_coloda', id, get_str_coloda(list_temp))

#                        print('1')
#                        print('game_hid_status_cards', storage['game_hid_status_cards:{}'.format(id)])
#                        print('2')
#                        print('game_arm', storage['game_arm:{}'.format(id)])
#                        print('3')
#                        print('game_hid', storage['game_hid:{}'.format(id)])
#                        print('4')
#                        print('game_hid_status_fite', storage['game_hid_status_fite:{}'.format(id)])

                        print('Бій принято вертаю текст: {}, по id: {}'.format(text, id))

                        data = [id, text]

                        return data

                elif get_data('game_hid_status', chat_id) == 'fite':
#                        print('game_hid_status:', storage['game_hid_status:{}'.format(chat_id)])
#                        fite = storage['game_hid_status_fite:{}'.format(id)]
#                        print(fite)

                        if set_fite_for_user(chat_id, text):

                            id = get_data('game', chat_id)
#                            set_data('game_hid_status', chat_id, 'hid')


                            str_temp = get_data('game_all_coloda', chat_id)
                            list_temp = get_list_coloda(str_temp)

                            str_arm = get_data('game_arm', chat_id)
                            list_arm = get_list_coloda(str_arm)

                            if len(list_temp) == 0 and len(list_arm) == 0:
                                text = '{}, Ти програв!!!'.format(text)
                                del_game(chat_id, id)

                            print('Хід по бою принято вертаю текст: {}, по id: {}'.format(text, id))

                            return id, text

                        elif text == '👋':

                            print('Гравець хоче снімати')

                            id = get_data('game', chat_id)
                            set_data('game_hid', chat_id, '0')
                            set_data('game_hid', id, '1')
                            set_data('game_hid_status', chat_id, 'fite')
                            set_data('game_hid_status', id, 'hid')

                            set_data('game_hid_status_cards', id, '6,7,8,9,1,V,D,K,T,')

                            str_temp = get_data('game_all_coloda', chat_id)
                            list_temp = get_list_coloda(str_temp)

                            str_arm = get_data('game_arm', chat_id)
                            str_fite = get_data('game_hid_status_all_fite', chat_id)

                            print('Гравець снімає такі карти', str_fite)

                            str_new_arm = str_arm + str_fite

                            set_data('game_hid_status_all_fite', chat_id, '0')

                            set_data('game_arm', chat_id, str_new_arm)

                            list_arm = get_list_coloda(get_data('game_arm', id))

                            while len(list_arm) < 6 and len(list_temp) != 0:
                                list_arm.append(list_temp.pop())
                        
                            set_data('game_arm', id, get_str_coloda(list_arm))

                            text = '👋 _ {}  🀄️ - {}'.format(get_data('game_cozer', id), len(list_temp))

                            set_data('game_all_coloda', chat_id, get_str_coloda(list_temp))
                            set_data('game_all_coloda', id, get_str_coloda(list_temp))

                            data = [id, text]

                            print('Снімання принято вертаю текст: {}, по id: {}'.format(text, id))

                            return data
            return None

    except KeyError:
        return None


def set_hid_for_user(id, text):

#    with shelve.open(shelve_game) as storage:
        print('Гравець хоче ходити із ', text)

        str = get_data('game_hid_status_cards', id)
        print('Гравець може кинути карти ', str)

        str_arm = get_data('game_arm', id)
        print('Гравець має такі карти ', str_arm)

        cards = get_list_coloda(str)

        cards_arm = get_list_coloda(str_arm)


        try:
            if text[0] in set(cards) and text in set(cards_arm):
                user_id = get_data('game', id)
                set_data('game_hid_status_fite', user_id, text)

                if  str == '6,7,8,9,1,V,D,K,T,':
                    set_data('game_hid_status_cards', id, '{},'.format(text[0]))

                    set_data('game_hid_status_all_fite', user_id, '{},'.format(text))
                else:
                    str_temp = '{}{},'.format(get_data('game_hid_status_cards', id), text[0]) 
                    set_data('game_hid_status_cards', id, str_temp)

                    str_fite = get_data('game_hid_status_all_fite', user_id)
                    set_data('game_hid_status_all_fite', user_id, '{}{},'.format(str_fite, text))
            
                list = get_list_coloda(get_data('game_arm', id))
                list.remove(text)
                set_data('game_arm', id, get_str_coloda(list))

                set_data('game_hid', id, '0')
                set_data('game_hid', user_id, '1')

#                print('game_hid_status_fite', storage['game_hid_status_fite:{}'.format(id)])
#                print('game_hid_status_cards', storage['game_hid_status_cards:{}'.format(id)])
#                print('game_arm', storage['game_arm:{}'.format(id)])
#                print('game_hid', storage['game_hid:{}'.format(id)])

                return True
            else:
                return False
        except KeyError:

            return False


def set_fite_for_user(id, text):

        print('Гравець хоче ходити із ', text)

        card_fite = get_data('game_hid_status_fite', id)
        print('Гравець має побити таку карту ', card_fite)

        str_arm = get_data('game_arm', id)
        print('Гравець має такі карти ', str_arm)

        cards_arm = get_list_coloda(str_arm)

        cozer = get_data('game_cozer', id)

        cards = [card_fite, text]

        try:
            if text in set(cards_arm):
                if get_game_logic(cards, cozer):
                    user_id = get_data('game', id)
                    set_data('game_hid_status_fite', id, '0')
                    str_temp = '{}{},'.format(get_data('game_hid_status_cards', user_id), text[0]) 
                    set_data('game_hid_status_cards', user_id, str_temp)

                    list = get_list_coloda(get_data('game_arm', id))
                    list.remove(text)
                    set_data('game_arm', id, get_str_coloda(list))
           
                    set_data('game_hid', id, '0')
                    set_data('game_hid', user_id, '1')

                    text_temp = get_data('game_hid_status_all_fite', id)
                    print('Карти із минулого бою: ', text_temp)

                    set_data('game_hid_status_all_fite', id, '{}{},'.format(text_temp, text))
                    print('Гравець побився і карти у бойові зараз такі: ', get_data('game_hid_status_all_fite', id))

                    return True
            else:
                return False
        except KeyError:
            return False


def get_game_logic(cards, cozer):

    mast = cozer[-2]
    print('cart_1',cards[0])
    print('cart_2',cards[1])
    print('cozer',mast)

    cards_int = [0, 0]

    if cards[0][-2] == cards[1][-2]:
        for i in range(2):
            if cards[i][0] == '6':
                cards_int[i] = 1
            elif cards[i][0] == '7':
                 cards_int[i] = 2
            elif cards[i][0] == '8':     
                cards_int[i] = 3
            elif cards[i][0] == '9':
                cards_int[i] = 4
            elif cards[i][0] == '1':
                cards_int[i] = 5
            elif cards[i][0] == 'V':
                cards_int[i] = 6
            elif cards[i][0] == 'D':
                cards_int[i] = 7
            elif cards[i][0] == 'K':
                cards_int[i] = 8
            elif cards[i][0] == 'T':
                cards_int[i] = 9
        if cards_int[0] < cards_int[1]:
            print('true')
            return True

    elif cards[1][-2] == mast:
        print('true')
        return True
    else:
        print('false')
        return False

        


def generate_markup(id):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    
    list = get_list_coloda(get_data('game_arm', id))

    # Создаем лист (массив) и записываем в него все элементы

    for i in range(len(list) // 3):
        markup.add(list.pop(), list.pop(), list.pop())
    for i in range(len(list) // 2):
        markup.add(list.pop(), list.pop())
    for i in range(len(list) // 1):
        markup.add(list.pop())
   
    if get_data('game_hid_status', id) == 'hid' and get_data('game_hid_status_cards', id) != '6,7,8,9,1,V,D,K,T,':
        markup.add('⚔️')
    elif get_data('game_hid_status', id) == 'fite':
        markup.add('👋')

    return markup







