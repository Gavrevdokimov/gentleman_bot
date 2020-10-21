# -*- coding: utf8 -*-

import telebot
from telebot import types
import random
import copy
import math
import json
import os

token = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(token)

companies = {1: {'Standard Oil': 0, 'White Star Line': 0, 'Charron': 0, 'Путиловские заводы': 0, 'Grönvik glasbruk': 0},
             2: {'Тульский оружейный завод': 0, 'US steel': 0, 'Victor Talking Machine Company': 0, 'Darmstädter-National bank': 0, 'Benz and Cie': 0, 'Пивоваренная компания Alexander Keith’s': 0},
             3: {'RKO pictures': 0, 'Procter and Gamble': 0, 'Parker Brothers': 0, 'Waggonfabriek L. Steinfurt': 0, 'Bally Пинбольные столы': 0},
             4: {'BMW': 0, 'Sumitomo': 0, 'IBM': 0, 'Cuban Telephone Company': 0, 'Grundig': 0},
             5: {'Panther': 0, 'Chrysler': 0, 'Consett Iron Company': 0, 'Peabody Energy': 0, 'Esso': 0},
             6: {'Federal Express': 0, 'Singer': 0, 'Ultimate': 0, 'Starbucks': 0, 'Firma Gebrüder Grill': 0},
             7: {'Lego': 0, 'Kodak': 0, 'Apple': 0, 'Polaroid': 0, 'Global Crossing': 0, 'Nintendo': 0}}

multipliers = {1: {'Standard Oil': 4, 'White Star Line': 0, 'Charron': 5, 'Путиловские заводы': 2, 'Grönvik glasbruk': 0},
             2: {'Тульский оружейный завод': 0, 'US steel': 1/3, 'Victor Talking Machine Company': 5, 'Darmstädter-National bank': 0, 'Benz and Cie': 1, 'Пивоваренная компания Alexander Keith’s': 4},
             3: {'RKO pictures': 5, 'Procter and Gamble': 8, 'Parker Brothers': 3, 'Waggonfabriek L. Steinfurt': 0, 'Bally Пинбольные столы': 0},
             4: {'BMW': 4, 'Sumitomo': 10, 'IBM': 8, 'Cuban Telephone Company': 0, 'Grundig': 5},
             5: {'Panther': 3, 'Chrysler': 0.1, 'Consett Iron Company': 0.1, 'Peabody Energy': 2, 'Esso': 3},
             6: {'Federal Express': 15, 'Singer': 0.2, 'Ultimate': 10, 'Starbucks': 2, 'Firma Gebrüder Grill': 0},
             7: {'Lego': 0.1, 'Kodak': 0, 'Apple': 2, 'Polaroid': 0, 'Global Crossing': 0, 'Nintendo': 1}}

finish = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

years = {1: "1900 — 1915", 2: "1915 — 1932", 3: "1932 — 1945", 4: "1945 — 1960", 5: "1960 — 1975", 6: "1975 — 1990", 7: "1990 — 2005"}

sport_years = {1: "Скачки\nПриз президента РФ 2019", 2: "MMA: Емельяненко - Чой, 2007", 3: "Футбол: Реал Мадрид - Барселона, 2014", 4: "Хоккей: Россия - Канада, 2008"}

debt = {1: 6, 2: 11, 3: 36, 4: 195, 5: 321, 6: 1746, 7: 0}

sports = {1: ['Лошадь №1', 'Лошадь №2', 'Лошадь №3', 'Лошадь №4', 'Лошадь №5', 'Лошадь №6', 'Лошадь №7', 'Лошадь №8', 'Лошадь №9', 'Лошадь №10'],
             2: ['Победит Емельяненко', 'Победит Чой'],
             3: ['Победит Реал Мадрид', 'Победит Барселона', 'Ничья в матче'],
             4: ['Победит Россия', 'Победит Канада', 'Ничья']}

meanings = {'Победит Емельяненко': "Емельяненко", 'Победит Чой': "Чой", 'Победит Реал Мадрид': "победу ФК Реал Мадрид", 'Победит Барселона': "победу ФК Барселона", 'Ничья': "ничью", 'Ничья в матче': "ничью", 'Победит Россия': "победу Сборной России", 'Победит Канада': "победу Сборной Канады", 'Лошадь №1': 'Лошадь №1', 'Лошадь №2': 'Лошадь №2', 'Лошадь №3': 'Лошадь №3', 'Лошадь №4': 'Лошадь №4', 'Лошадь №5': 'Лошадь №5', 'Лошадь №6': 'Лошадь №6', 'Лошадь №7': 'Лошадь №7', 'Лошадь №8': 'Лошадь №8', 'Лошадь №9': 'Лошадь №9', 'Лошадь №10': 'Лошадь №10'}

sports_list = ['Лошадь №1', 'Лошадь №2', 'Лошадь №3', 'Лошадь №4', 'Лошадь №5', 'Лошадь №6', 'Лошадь №7', 'Лошадь №8', 'Лошадь №9', 'Лошадь №10', 'Победит Емельяненко', 'Победит Чой',
               'Победит Реал Мадрид', 'Победит Барселона', 'Ничья', 'Ничья в матче', 'Победит Россия', 'Победит Канада', "want_knockout", "no_knockout", "want_knockout_round", "no_knockout_round",
               "want_result", "no_result", "want_hockey_result", "no_hockey_result", "0 goal", "1 goal", "2 goals", "3 goals", "4 goals", "5 goals", "6 goals", "7 goals", "1 round", "2 round", "3 round"]

bits = {1: {'winner': 0},
        2: {'winner': 0, 'knockout': 0, 'knockout_round': 0},
        3: {'winner': 0, 'result': "no bit yet"},
        4: {'winner': 0, 'result': "no bit yet"}}

chess_list = ["Пешка", "Конь", "Слон", "Ладья", "Ферзь", "eat", "lose", "checkmate", "got_checkmate", "next_player", "really_checkmate"]
chesspiece_price = {"Пешка": 1, "Конь": 3, "Слон": 3, "Ладья": 5, "Ферзь": 9}

game_flag = "sport"  # sport/chess/fond_market


# открываем сохраненную игру
with open('save_players.json') as f:
    try:
        file = json.load(f)
        game_flag = file[0]
        players = file[1]
        players_2 = copy.deepcopy(players)
        players = {}
        for player in players_2:
            player_2 = int(player)
            players[player_2] = copy.deepcopy(players_2[player])
            companies_2 = copy.deepcopy(players[player_2]["companies"])
            players[player_2]["companies"] = {}
            for round_n in companies_2:
                round_2 = int(round_n)
                players[player_2]["companies"][round_2] = copy.deepcopy(companies_2[round_n])
            finish_2 = copy.deepcopy(players[player_2]["finish"])
            players[player_2]["finish"] = {}
            for round_num in finish_2:
                round_3 = int(round_num)
                players[player_2]["finish"][round_3] = copy.deepcopy(finish_2[round_num])
            bits_2 = copy.deepcopy(players[player_2]["bits"])
            players[player_2]["bits"] = {}
            for round_nu in bits_2:
                round_3 = int(round_nu)
                players[player_2]["bits"][round_3] = copy.deepcopy(bits_2[round_nu])
    except:
        players = {}


sticker = 'CAACAgIAAxkBAAIPnV67u5l7uBx-N1IYtu70VgclQuO4AAIVAwACnNbnCgbnCWarj1O-GQQ'
sticker_2 = 'CAACAgIAAxkBAAIP3167xcJI92k-JiH6O1tBSEvKzSUEAAISAwACnNbnChxSQ7QkdV0oGQQ'
sticker_3 = 'CAACAgIAAxkBAAIiGV6_wT-LBUzOSIcwmBNHdCFuUNp2AAIXAwACnNbnCtb0SKu1OIHZGQQ'


yesfraselist = [
    "Это были непростые годы. Давно скопились обиды государств друг на друга, и к ним постоянно прибавлялись новые. Назревавший конфликт обернулся кровопролитной войной, которая прямо сейчас в самом разгаре. Но деньги и эмоции — несовместимые вещи, мы надеемся, что даже из этого периода, вы смогли извлечь выгоду.",
    "Это были непростые годы. Только закончилась крупнейшая в истории человечества война, и по миру прокатилась волна революций, как разгорелся экономический кризис. Но настоящая акула фондового рынка только рада потрясениям, потому что на них можно заработать. ",
    "Это были непростые годы. Вы думали, что хуже Первой Мировой некуда? Оказалось, что есть. Война - это ад... если ты не догадался не ввязываться в нее. Гораздо приятнее смотреть на драку со стороны, а еще приятнее продавать драчунам бейсбольные биты.",
    "Это были непростые годы. Только-только закончилась война. Целый материк оказался в руинах. Но жизнь продолжается. Наконец агрессивный трейдинг может уступить место вдумчивому долгосрочному инвестированию.",
    "Это были непростые годы. Казалось бы, живите себе спокойно, все же поняли, каким ужасом может обернуться война. Но битвы бывают не только на полях сражений с автоматами в руках, но и экономические, за богатство этого мира. И если ты скопил богатства и получил власть, готовься их защищать.",
    "Это были непростые годы. Но человечество держалось молодцом. Конфликты носили больше локальный характер. Мир стал чуть более предсказуемым, а это лучшее состояние для бизнеса и инвесторов, когда вы уверены в завтрашнем дне и можете спокойно вкладывать деньги.",
    "Это были непростые годы. Скорость жизни постоянно увеличивается, за какие-то 15 лет мир изменился до неузнаваемости. Целые состояния появляются из ниоткуда за считанные годы и также быстро растворяются. Да что там состояния, если теперь можно утром проснуться в другой стране. Но мастер фондового рынка только рад такой волатильности."]


# пишем правильную форму слова "доллар"
def dollar_word(dollar_sum):
    if isinstance(dollar_sum, float):
        return "доллара"
    elif 11 <= int(str(dollar_sum).split()[0][-2:]) <= 14:
        return "долларов"
    elif 1 < int(str(dollar_sum).split()[0][-1]) <= 4:
        return "доллара"
    elif int(str(dollar_sum).split()[0][-1]) == 1:
        return "доллар"
    else:
        return "долларов"


# ответ на простые сообщения
def small_talk(message):
    if ("привет" in message.text.lower()) or ("hi" in message.text.lower()) or ("hello" in message.text.lower()) or ("здравствуй" in message.text.lower()) or ("хай" in message.text.lower()):
        bot.send_message(message.from_user.id, "Здравствуйте! Как поживаете?")
    elif ("хорошо" in message.text.lower()) or ("отлично" in message.text.lower()) or ("лучше всех" in message.text.lower()) or ("прекрасно" in message.text.lower()):
        if ("ты" in message.text.lower() and "милый" not in message.text.lower()) or ("тебя" in message.text.lower()) or ("твои" in message.text.lower()) or ("ваши" in message.text.lower()) or ("вас" in message.text.lower()) or ("вы" in message.text.lower()):
            bot.send_message(message.from_user.id, "И у меня все хорошо) Желаю удачи в игре!\nP.S. Я болею именно за вас 😉, только никому не говорите)")
        else:
            bot.send_message(message.from_user.id, "Я очень рад за вас! Желаю удачи в игре!\nP.S. Я болею именно за вас 😉, только никому не говорите)")
    elif ("не очень" in message.text.lower()) or ("плохо" in message.text.lower()) or ("так себе" in message.text.lower()) or ("грустно" in message.text.lower()) or ("скучно" in message.text.lower()) or ("сойдет" in message.text.lower()) or ("бомж" in message.text.lower()) or ("проиграл" in message.text.lower()) or ("проебал" in message.text.lower()) or ("просрал" in message.text.lower()):
        if ("ты" in message.text.lower()) or ("тебя" in message.text.lower()) or ("твои" in message.text.lower()) or ("ваши" in message.text.lower()) or ("вас" in message.text.lower()) or ("вы" in message.text.lower()):
            bot.send_message(message.from_user.id, "У меня хорошо, и у вас все обязательно наладится! Желаю удачи в игре!\nP.S. Я болею именно за вас 😉, только никому не говорите)")
        else:
            bot.send_message(message.from_user.id, "Я уверен, все обязательно наладится, когда вы победите в этой игре) Желаю удачи!\nP.S. Я болею именно за вас 😉, только никому не говорите)")
    elif ("спасибо" in message.text.lower()) or ("приятно" in message.text.lower()) or ("мило" in message.text.lower()) or ("милый" in message.text.lower()) or ("классный" in message.text.lower()):
        bot.send_sticker(chat_id=message.from_user.id, data=sticker_2)
    elif ("тебя" in message.text.lower()) or ("твои" in message.text.lower()) or ("ваши" in message.text.lower()) or ("вас" in message.text.lower()) or ("вы" in message.text.lower()) or ("как сам" in message.text.lower()) or ("че как" in message.text.lower()) or ("как поживае" in message.text.lower()) or ("дела" in message.text.lower()):
        bot.send_message(message.from_user.id, "У меня все хорошо, только Роспотребнадзор постоянно блокирует 😔")
    else:
        bot.send_message(message.from_user.id, "Извините, я не понимаю такие сообщения")
        bot.send_message(325051402, f"**{message.text}**")


# красивая выдача описания раунда в начале
def beautiful(id):
    if game_flag == "sport":
        return f"Раунд {players[id]['round_number']}/4: {sport_years[players[id]['round_number']]}"
    else:
        return f"Раунд {players[id]['round_number']}/7: {years[players[id]['round_number']]} годы."


# составляем список компаний на раунд по номеру раунда
def round_list(id):
    roundlist = []
    if game_flag == "sport":
        for participant in sports[players[id]["round_number"]]:
            roundlist.append(participant)
    else:
        for company in companies[players[id]["round_number"]]:
            roundlist.append(company)
    return roundlist


# считаем деньги на конец раунда
def money_result(id):
    investment_list = []
    for i in players[id]["companies"][players[id]["round_number"]].values():
        investment_list.append(i)
    multipliers_list = []
    for i in multipliers[players[id]["round_number"]].values():
        multipliers_list.append(i)
    almost_result = [x * y for x, y in zip(investment_list, multipliers_list)]
    round_result = sum([int(x) for x in almost_result])
    return round_result


# компания с максимальной доходностью
def max_profitable_company(id):
    investment_list = []
    result_list = []
    max_profit_companies = []
    for round in players[id]["companies"]:
        for company in players[id]["companies"][round]:
            if players[id]["companies"][round][company] > 0:
                investment_list.append(company)
    for round in multipliers:
        for company in multipliers[round]:
            if company in investment_list:
                result_list.append(multipliers[round][company])
    max_result = max(result_list)
    for round in multipliers:
        for company in multipliers[round]:
            if multipliers[round][company] == max_result:
                max_profit_companies.append(company)
    if len(max_profit_companies) == 1:
        return f"Ваше самое успешное вложение - {max_profit_companies[0]}, доходность составила {(max_result - 1) * 100}%"
    elif len(max_profit_companies) > 1:
        return f"Ваши самые успешные вложения - {', '.join(max_profit_companies)}, доходность составила {(max_result - 1) * 100}%"


# компания с наибольшим выигрышем в деньгах
def max_profit_from_company(id):
    players[id]["companies_result"] = copy.deepcopy(multipliers)
    all_results_list = []
    max_profit_companies = []
    max_lose_companies = []
    for round in multipliers:
        for company in multipliers[round]:
            players[id]["companies_result"][round][company] = players[id]["companies"][round][company] * (multipliers[round][company] - 1)
    for round in players[id]["companies_result"]:
        for company in players[id]["companies_result"][round]:
            all_results_list.append(players[id]["companies_result"][round][company])
    max_result = max(all_results_list)
    for round in players[id]["companies_result"]:
        for company in players[id]["companies_result"][round]:
            if players[id]["companies_result"][round][company] == max_result:
                max_profit_companies.append(company)
    if len(max_profit_companies) == 1:
        max_profit = f"Больше всего вы заработали на компании {max_profit_companies[0]}, прибыль от инвестиции составила {max_result} {dollar_word(max_result)}"
    else:  # len(max_profit_companies) > 1
        max_profit = f"Больше всего вы заработали на компаниях - {', '.join(max_profit_companies)}, прибыль от каждой инвестиции равнялась {max_result} {dollar_word(max_result)}"
    min_result = min(all_results_list)
    for round in players[id]["companies_result"]:
        for company in players[id]["companies_result"][round]:
            if players[id]["companies_result"][round][company] == min_result:
                max_lose_companies.append(company)
    if len(max_lose_companies) == 1:
        max_lose = f"Больше всего вы потеряли на компании {max_lose_companies[0]}, убыток от инвестиции составил {math.ceil(-min_result)} {dollar_word(math.ceil(-min_result))}"
    else:  # len(max_lose_companies) > 1
        max_lose = f"Больше всего вы потеряли на компаниях - {', '.join(max_lose_companies)}, убыток от каждой инвестиции равнялся {math.ceil(-min_result)} {dollar_word(math.ceil(-min_result))}"
    if min_result >= 0:
        return max_profit
    else:
        a = '\n'.join([max_profit, max_lose])
        return a


# клавиатура со списком компаний
def keyboard(id):
    keyboard = types.InlineKeyboardMarkup()
    for company in round_list(id):   # x = round_list
        keyboard.add(types.InlineKeyboardButton(text=company, callback_data=company))
    return keyboard


# клавиатура готовы начать раунд?
def keyboard_begin_round():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data='begin')
    keyboard.add(yes)
    return keyboard


# клавиатура Ведущий, покажи результат
def keyboard_result():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Показать", callback_data='yes')
    keyboard.add(yes)
    return keyboard


# табличка, кто куда инвестировал
def investment_table():
    invest = {}
    local_round_list = []
    result = []
    for player in players:
        round_number = players[player]["round_number"]
        break
    for company in players[player]["companies"][round_number]:
        invest[company] = []
        local_round_list.append(company)
    for company in local_round_list:
        for player in players:
            if players[player]["companies"][round_number][company] > 0:
               invest[company].append(players[player]["name"])
    for company in invest:
        invest[company] = ", ".join(invest[company])
        result.append(": ".join([company, invest[company]]))
        final = "\n".join(result)
    return final


# табличка с уже сделанными инвестициями для участника
def already_invested(id):
    invest_list = sorted([players[id]["companies"][players[id]["round_number"]][company] for company in players[id]["companies"][players[id]["round_number"]] if players[id]["companies"][players[id]["round_number"]][company] > 0], reverse=True)
    company_list = []
    for result in invest_list:
        for company in players[id]["companies"][players[id]["round_number"]]:
            if players[id]["companies"][players[id]["round_number"]][company] == result:
                company_list.append(company)
    company_list_2 = company_list[::-1]
    for i in range(0, len(company_list_2)):
        if company_list_2[i] in company_list_2[i + 1:]:
            company_list.remove(company_list_2[i])
    table_list = []
    for i in range(0, len(company_list)):
        a = "".join(str(company_list[i]) +" — "+ str(invest_list[i]) + " " + str(dollar_word(invest_list[i])))
        table_list.append(a)
    table_str = "\n".join(table_list)
    return table_str


# табличка с результатами раунда
def round_table():
    for player in players:   # проверяем, всё ли игрок инвестировал, если нет, бабло не сгорает
        round_investment = sum([i for i in players[player]["companies"][players[player]["round_number"]].values()])
        if players[player]["money"] != round_investment:
            players[player]["round_result"] = money_result(player) + (players[player]["money"] - round_investment)
    result_money_list = sorted([players[i]["round_result"] - players[i]["debt"] for i in players], reverse=True)
    players_list = []
    money_list = []
    debt_list = []
    for result in result_money_list:
        for player in players:
            if players[player]["round_result"] - players[player]["debt"] == result:
                players_list.append(players[player]["name"])
    players_list_2 = players_list[::-1]
    for i in range(0, len(players_list_2)):
        if players_list_2[i] in players_list_2[i + 1:]:
            players_list.remove(players_list_2[i])
    for player in players_list:
        for i in players:
            if player == players[i]["name"]:
                money_list.append(players[i]["round_result"])
                debt_list.append(players[i]["debt"])
    table_list = []
    if players[[player for player in players][0]]["round_number"] == 7:
        for i in range(0, len(players_list)):
            a = "".join(str(players_list[i]) + " — " + str(result_money_list[i]) + " " + str(dollar_word(result_money_list[i])))
            table_list.append(a)
        table_str = "\n".join(table_list)
        return table_str, players_list[0]
    else:
        for i in range(0, len(players_list)):
            if debt_list[i] > 0:
                a = "".join(str(players_list[i]) + " — " + str(money_list[i]) + " " + str(dollar_word(result_money_list[i])) + ", " + "долг — " + str(debt_list[i]) + " " + str(dollar_word(debt_list[i])))
                table_list.append(a)
            else:
                a = "".join(str(players_list[i]) + " — " + str(money_list[i]) + " " + str(dollar_word(result_money_list[i])))
                table_list.append(a)
        table_str = "\n".join(table_list)
    return table_str


# итоговый прирост денег
def delta(money):
    delta_abs = round((money - 3) / 105, 2)
    if money >= 0:
        delta_otn = round(((money / 3) ** (1 / 105) - 1) * 100, 2)
        return f"Каждый год он в среднем рос на {delta_otn}% и прибавлял {delta_abs} {dollar_word(delta_abs)}! Это впечатляющий результат, и вы по праву можете им гордиться!"
    else:
        return f"Каждый год в среднем вы теряли {-delta_abs} {dollar_word(-delta_abs)}! Это полезный опыт, который позволит вам сберечь деньги в реальной жизни!"


# сообщение о появлении долга у игрока
def lose_money(player):
    creditor_list = ['ваш богатый дядюшка одолжил вам', 'ваша любимая бабуленька одолжила вам', 'сын маминой подруги одолжил вам', 'Банк "Деньги под залог почки" дал вам в кредит', 'ваш богатый дядюшка', 'местный бандит одолжил вам']
    return f"К сожалению, в прошлом раунде вы все потеряли. Но {creditor_list[players[player]['round_number']-1]} {debt[players[player]['round_number']]} {dollar_word(debt[players[player]['round_number']])}, " \
    f"чтобы вы могли продолжить попытки разбогатеть. До конца игры долг будет увеличиваться на 100% каждый раунд и будет вычтен из вашего результата в 7 раунде."


# подсчитываем риск профиль участника
def risk_profile(id):
    company_list = []
    for round in players[id]["companies"]:
        for company in players[id]["companies"][round]:
            if players[id]["companies"][round][company] > 0:
                company_list.append(company)
    risk = len(company_list)
    if 29 <= risk <= 35:
        return "Ваш риск-профиль: Неразборчивый перестраховщик, уровень риска 1 из 5. Вы вкладываетесь во все подряд, не вникая в особенности каждой компании. Диверсификация - это, разумеется, очень хорошо, но, даже диверсифицируясь, стоит с умом выбирать компании для инвестиций."
    elif 21 <= risk <= 28:
        return "Ваш риск-профиль: Диверсификатор, уровень риска 2 из 5. Вы молодец, у вас очень грамотный и взвешенный подход. Вы не кидались на все, что вам предлогалось, но и не складывали все яйца в одну корзину. Вас можно обойти по доходности на дистанции нескольких лет, но в долгосрочной перспективе вы кому угодно дадите фору."
    elif 17 <= risk <= 20:
        return "Ваш риск-профиль: Умеренно рискованный, уровень риска 3 из 5. Данный уровень риска подходит людям, которые давно на рынке и уделяют достаточное время анализу компаний. Если вы из таких, то так держать! Если нет, то советуем в реальной жизни составлять чуть более диверсифицированный портфель."
    elif 12 <= risk <= 16:
        return "Ваш риск-профиль: Очень рискованный, уровень риска 4 из 5. Либо вы профессиональный трейдер, которой по 16 часов в день тратит на анализ компаний и оценку ситуации на рынке, либо вы просто слишком самонадеянны и считаете себя умнее других. Если вы из вторых, то скоро рынок преподаст вам урок, но он будет дорогой."
    else:
        return 'Ваш риск-профиль: "Стальные яйца", уровень риска 5 из 5. Вы явно либо Ванга, либо инсайдер. Если я угадал, то давайте дружить) Если ни то, ни другое, то рынок вас очень скоро прожует и выплюнет. Нельзя все яйца класть в одну корзину.'


# сохраняем players в файл
def saving():
    file = [game_flag, players]
    with open("save_players.json", "w") as write_file:
        json.dump(file, write_file)
    return


# заносим участника в базу игроков
def put_gamer_to_base(message):
    try:
        with open('players_base.json') as f:
                history_players = json.load(f)
        history_players_2 = copy.deepcopy(history_players)
        history_players = {}
        for player in history_players_2:
            player_2 = int(player)
            history_players[player_2] = copy.deepcopy(history_players_2[player])
    except:
        history_players = {}
    player = message.from_user.id
    if player == 325051402:
        for gamer in players:
            history_players[gamer]["game_result"] = players[gamer]["money"]
    else:
        if player in history_players:
            bot.send_message(325051402, f"Вошел человек, уже игравший с нами - {message.from_user.first_name} {message.from_user.last_name}, в той игре он заработал {history_players[player]['game_result']}")
        else:
            history_players[player] = {}
            history_players[player]["name"] = message.from_user.first_name
            history_players[player]["last_name"] = message.from_user.last_name
            history_players[player]["game_result"] = players[player]["money"]
    with open("players_base.json", "w") as write_file:
        json.dump(history_players, write_file)
    return


# клавиатура со списком участников для удаления
def delete_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for player in players:
        keyboard.add(types.InlineKeyboardButton(text=players[player]["name"], callback_data=player))
    return keyboard


# клавиатура со списком участников для изменения денег
def correction_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for player in players:
        keyboard.add(types.InlineKeyboardButton(text=players[player]["name"], callback_data=(f"correction {player}")))
    return keyboard


# клавиатура нокаут
def keyboard_knockout():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Хочу", callback_data='want_knockout')
    no = types.InlineKeyboardButton(text="Нет, просто на победителя", callback_data='no_knockout')
    keyboard.add(yes, no)
    return keyboard


# клавиатура раунд нокаута
def keyboard_knockout_round():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Хочу", callback_data='want_knockout_round')
    no = types.InlineKeyboardButton(text="Только досрочное завершение", callback_data='no_knockout_round')
    keyboard.add(yes, no)
    return keyboard


# клавиатура хочешь поставить на результат футбола?
def keyboard_football_result():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Хочу", callback_data='want_result')
    no = types.InlineKeyboardButton(text="Нет, просто на победителя", callback_data='no_result')
    keyboard.add(yes, no)
    return keyboard


# клавиатура хочешь поставить на результат хоккея?
def keyboard_hockey_result():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Хочу", callback_data='want_hockey_result')
    no = types.InlineKeyboardButton(text="Нет, просто на победителя", callback_data='no_hockey_result')
    keyboard.add(yes, no)
    return keyboard


# клавиатура футбольная ничья
def keyboard_no_football_winner():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Хочу", callback_data='want_result')
    no = types.InlineKeyboardButton(text="Нет, просто на ничью", callback_data='no_result')
    keyboard.add(yes, no)
    return keyboard


# клавиатура хоккейная ничья
def keyboard_no_hockey_winner():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Хочу", callback_data='want_hockey_result')
    no = types.InlineKeyboardButton(text="Нет, просто на ничью", callback_data='no_hockey_result')
    keyboard.add(yes, no)
    return keyboard


# клавиатура результат футбола
def keyboard_match_result():
    keyboard = types.InlineKeyboardMarkup()
    nul = types.InlineKeyboardButton(text="0 голов", callback_data='0 goal')
    one = types.InlineKeyboardButton(text="1 гол", callback_data='1 goal')
    two = types.InlineKeyboardButton(text="2 гола", callback_data='2 goals')
    three = types.InlineKeyboardButton(text="3 гола", callback_data='3 goals')
    four = types.InlineKeyboardButton(text="4 гола", callback_data='4 goals')
    five = types.InlineKeyboardButton(text="5 голов", callback_data='5 goals')
    six = types.InlineKeyboardButton(text="6 голов", callback_data='6 goals')
    seven = types.InlineKeyboardButton(text="7 голов", callback_data='7 goals')
    keyboard.add(nul, one, two, three, four, five, six, seven)
    return keyboard


# клавиатура результат хоккея
def keyboard_hockey_match_result():
    keyboard = types.InlineKeyboardMarkup()
    nul = types.InlineKeyboardButton(text="0 шайб", callback_data='0 goal')
    one = types.InlineKeyboardButton(text="1 шайбу", callback_data='1 goal')
    two = types.InlineKeyboardButton(text="2 шайбы", callback_data='2 goals')
    three = types.InlineKeyboardButton(text="3 шайбы", callback_data='3 goals')
    four = types.InlineKeyboardButton(text="4 шайбы", callback_data='4 goals')
    five = types.InlineKeyboardButton(text="5 шайб", callback_data='5 goals')
    six = types.InlineKeyboardButton(text="6 шайб", callback_data='6 goals')
    seven = types.InlineKeyboardButton(text="7 шайб", callback_data='7 goals')
    keyboard.add(nul, one, two, three, four, five, six, seven)
    return keyboard


# клава количество раундов MMA
def keyboard_MMA_round():
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text="В 1 раунде", callback_data='1 round')
    two = types.InlineKeyboardButton(text="В 2 раунде", callback_data='2 round')
    three = types.InlineKeyboardButton(text="В 3 раунде", callback_data='3 round')
    keyboard.add(one, two, three)
    return keyboard


# клава для начала игры
def keyboard_start_game():
    keyboard = types.InlineKeyboardMarkup()
    go = types.InlineKeyboardButton(text="Начать игру", callback_data='start_game')
    keyboard.add(go)
    return keyboard


# клава силовой смены раунда
def keyboard_change_flag():
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text="Ставки на спорт", callback_data='round_sport')
    two = types.InlineKeyboardButton(text="Шахматы", callback_data='round_chess')
    three = types.InlineKeyboardButton(text="Фондовый рынок", callback_data='round_fond_market')
    keyboard.add(one, two, three)
    return keyboard


# клава шахматы
def keyboard_chess():
    keyboard = types.InlineKeyboardMarkup()
    eat = types.InlineKeyboardButton(text="Срубил", callback_data='eat')
    lose = types.InlineKeyboardButton(text="Потерял", callback_data='lose')
    checkmate = types.InlineKeyboardButton(text="Поставил мат", callback_data='checkmate')
    got = types.InlineKeyboardButton(text="Получил мат", callback_data='got_checkmate')
    next_player = types.InlineKeyboardButton(text="Следующий игрок", callback_data='next_player')
    keyboard.add(eat, lose, checkmate, got, next_player)
    return keyboard


# клава потерял ли фигуру после своего хода
def keyboard_also_lose():
    keyboard = types.InlineKeyboardMarkup()
    lose = types.InlineKeyboardButton(text="Потерял", callback_data='lose')
    next_player = types.InlineKeyboardButton(text="Следующий игрок", callback_data='next_player')
    keyboard.add(lose, next_player)
    return keyboard


# клава шахматы фигуры
def keyboard_chesspiece():
    keyboard = types.InlineKeyboardMarkup()
    for chesspiece in chess_list[0:5]:
        keyboard.add(types.InlineKeyboardButton(text=chesspiece, callback_data=chesspiece))
    return keyboard


# клава правда ли мат?
def keyboard_really_checkmate():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Действительно мат", callback_data="really_checkmate"))
    return keyboard


# красивая выдача, на что чел ставит
def sport_choose_result(id):
    team = players[id]["choose"]
    result = players[id]["bits"][players[id]["round_number"]]["result"]
    result_2 = "-".join([result[0], result[1]])
    return f"Сколько вы хотите поставить на {team} co счетом {result_2}? У вас {players[id]['money']} {dollar_word(players[id]['money'])}."


bits = {1: {'winner': 0},
        2: {'winner': 0, 'knockout': 0, 'knockout_round': 0},
        3: {'winner': 0, 'result': "no bit yet"},
        4: {'winner': 0, 'result': "no bit yet"}}

# функция работы со ставками
def sport_bits(message):
    horses = ['Лошадь №1', 'Лошадь №2', 'Лошадь №3', 'Лошадь №4', 'Лошадь №5', 'Лошадь №6', 'Лошадь №7', 'Лошадь №8', 'Лошадь №9', 'Лошадь №10']
    if message.data == 'Победит Емельяненко' or message.data == 'Победит Чой':
        players[message.from_user.id]["bits"][2] = copy.deepcopy(bits[2])      # если участник хочет поменять решение
        players[message.from_user.id]["choose"] = meanings[message.data]
        players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["winner"] = meanings[message.data]
        bot.send_message(message.from_user.id, "Хотите поставить на досрочное завершение боя? Если угадаете, коэффициент будет равен 3!", reply_markup=keyboard_knockout())
    elif message.data == 'want_knockout':
        players[message.from_user.id]["bits"][2]["knockout_round"] = 0     # если участник хочет поменять решение
        players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["knockout"] = 1
        bot.send_message(message.from_user.id, "Хотите поставить на досрочное завершение боя в конкретном раунде? Если угадаете, коэффициент будет равен 5!", reply_markup=keyboard_knockout_round())
    elif message.data == 'no_knockout':
        players[message.from_user.id]["bits"][2]["knockout"] = 0  # если участник хочет поменять решение
        players[message.from_user.id]["bits"][2]["knockout_round"] = 0  # если участник хочет поменять решение
        bot.send_message(message.from_user.id, f"Сколько вы хотите поставить на победу {players[message.from_user.id]['choose']}? У вас {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}.")
    elif message.data == 'want_knockout_round':
        bot.send_message(message.from_user.id, f"В каком раунде вы предвидите победу {players[message.from_user.id]['choose']}?", reply_markup=keyboard_MMA_round())
    elif message.data == 'no_knockout_round':
        players[message.from_user.id]["bits"][2]["knockout_round"] = 0  # если участник хочет поменять решение
        bot.send_message(message.from_user.id, f"Сколько вы хотите поставить на досрочную победу {players[message.from_user.id]['choose']}? У вас {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}.")
    elif message.data == 'Победит Реал Мадрид' or message.data == 'Победит Барселона' or message.data == 'Ничья в матче':
        players[message.from_user.id]["bits"][3] = copy.deepcopy(bits[3])  # если участник хочет поменять решение
        players[message.from_user.id]["choose"] = meanings[message.data]
        players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["winner"] = message.data
        if message.data == 'Ничья в матче':
            bot.send_message(message.from_user.id, "Хотите поставить на точный счет во встрече? Если угадаете, коэффициент будет равен 5!", reply_markup=keyboard_no_football_winner())
        else:
            bot.send_message(message.from_user.id, "Хотите поставить на точный счет во встрече? Если угадаете, коэффициент будет равен 5!", reply_markup=keyboard_football_result())
    elif message.data == 'want_result':
        players[message.from_user.id]["bits"][3]["result"] = "no bit yet"  # если участник хочет поменять решение
        bot.send_message(message.from_user.id, "Сколько голов забьет Реал Мадрид?", reply_markup=keyboard_match_result())
    elif message.data == 'no_result':
        players[message.from_user.id]["bits"][3]["result"] = "no bit yet"  # если участник хочет поменять решение
        bot.send_message(message.from_user.id, f"Сколько вы хотите поставить на {players[message.from_user.id]['choose']}? У вас {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}.")
    elif message.data == 'Победит Россия' or message.data == 'Победит Канада' or message.data == 'Ничья':
        players[message.from_user.id]["bits"][4] = copy.deepcopy(bits[4])  # если участник хочет поменять решение
        players[message.from_user.id]["choose"] = meanings[message.data]
        players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["winner"] = message.data
        if message.data == 'Ничья':
            bot.send_message(message.from_user.id, "Хотите поставить на точный счет во встрече? Если угадаете, коэффициент будет равен 5!", reply_markup=keyboard_no_hockey_winner())
        else:
            bot.send_message(message.from_user.id, "Хотите поставить на точный счет во встрече? Если угадаете, коэффициент будет равен 5!", reply_markup=keyboard_hockey_result())
    elif message.data == 'want_hockey_result':
        players[message.from_user.id]["bits"][4]["result"] = "no bit yet"  # если участник хочет поменять решение
        bot.send_message(message.from_user.id, "Сколько шайб забросит Сборная России?", reply_markup=keyboard_hockey_match_result())
    elif message.data == 'no_hockey_result':
        players[message.from_user.id]["bits"][4]["result"] = "no bit yet"  # если участник хочет поменять решение
        bot.send_message(message.from_user.id, f"Сколько вы хотите поставить на {players[message.from_user.id]['choose']}? У вас {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}.")
    elif message.data in horses:
        players[message.from_user.id]["choose"] = meanings[message.data]
        players[message.from_user.id]["bits"][1] = meanings[message.data]
        bot.send_message(message.from_user.id, f"Сколько вы хотите поставить на {message.data}? У вас {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}.")
    elif "goal" in message.data:
        if players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"] == "no bit yet":
            players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"] = str(message.data).split()[0]
            if players[message.from_user.id]["round_number"] == 3:
                bot.send_message(message.from_user.id, "Сколько голов забьет Барселона?", reply_markup=keyboard_match_result())
            else:
                bot.send_message(message.from_user.id, "Сколько шайб забросит Сборная Канады?", reply_markup=keyboard_hockey_match_result())
        else:
            if (players[message.from_user.id]["choose"] == "победу ФК Реал Мадрид" and int(players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"]) <= int(str(message.data).split()[0])) or (players[message.from_user.id]["choose"] == "победу ФК Барселона" and int(players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"]) >= int(str(message.data).split()[0])):
                players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"] = "no bit yet"
                bot.send_message(message.from_user.id, "Будьте внимательнее. У вас счет не соответствует указанному победителю. Давайте попробуем еще раз.")
                bot.send_message(message.from_user.id, f"{beautiful(message.from_user.id)}\nНа что хотите поставить?", reply_markup=keyboard(message.from_user.id))
            elif (players[message.from_user.id]["choose"] == "победу Сборной России" and int(players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"]) <= int(str(message.data).split()[0])) or (players[message.from_user.id]["choose"] == "победу Сборной Канады" and int(players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"]) >= int(str(message.data).split()[0])):
                players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"] = "no bit yet"
                bot.send_message(message.from_user.id, "Будьте внимательнее. У вас счет не соответствует указанному победителю. Давайте попробуем еще раз.")
                bot.send_message(message.from_user.id, f"{beautiful(message.from_user.id)}\nНа что хотите поставить?", reply_markup=keyboard(message.from_user.id))
            else:
                players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"] = "".join([players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["result"], str(message.data).split()[0]])
                bot.send_message(message.from_user.id, f"{sport_choose_result(message.from_user.id)}")
    elif "round" in message.data:
        players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["knockout_round"] = int(str(message.data).split()[0])
        bot.send_message(message.from_user.id, f'Сколько вы хотите поставить на досрочную победу {players[message.from_user.id]["choose"]} в {players[message.from_user.id]["bits"][players[message.from_user.id]["round_number"]]["knockout_round"]} раунде? У вас {players[message.from_user.id]["money"]} {dollar_word(players[message.from_user.id]["money"])}.')


# расчет результата ставок
def sport_result_counting():
    round_number = [players[player]["round_number"] for player in players][0]
    if round_number == 1:
        for player in players:
            if players[player]["choose"] == "Лошадь №9":
                players[player]["money"] += 5 * players[player]["bit"]
            elif players[player]["choose"] == "Лошадь №1":
                players[player]["money"] +=  3 * players[player]["bit"]
            elif players[player]["choose"] == "Лошадь №7":
                players[player]["money"] +=  2 * players[player]["bit"]
            elif players[player]["choose"] == "Лошадь №5" or players[player]["choose"] == "Лошадь №6":
                players[player]["money"] += 0
            else:
                players[player]["money"] -= players[player]["bit"]
    elif round_number == 2:
        for player in players:
            if players[player]["choose"] == "Емельяненко":
                if players[player]["bits"][round_number]["knockout"] == 1:
                    if players[player]["bits"][round_number]["knockout_round"] != 0:
                        if players[player]["bits"][round_number]["knockout"] == 1:
                            players[player]["money"] += 5 * players[player]["bit"]
                        else:
                            players[player]["money"] -= players[player]["bit"]
                    else:
                        players[player]["money"] += 3 * players[player]["bit"]
                else:
                    players[player]["money"] += 2 * players[player]["bit"]
            else:
                players[player]["money"] -= players[player]["bit"]
    elif round_number == 3:
        for player in players:
            if players[player]["choose"] == "победу ФК Барселона":
                if players[player]["bits"][round_number]["result"] != "no bit yet":
                    if players[player]["bits"][round_number]["result"] == "34":
                        players[player]["money"] += 5 * players[player]["bit"]
                    else:
                        players[player]["money"] -= players[player]["bit"]
                else:
                    players[player]["money"] += players[player]["bit"]
            else:
                players[player]["money"] -= players[player]["bit"]
    elif round_number == 4:
        for player in players:
            if players[player]["choose"] == "победу Сборной России":
                if players[player]["bits"][round_number]["result"] != "no bit yet":
                    if players[player]["bits"][round_number]["result"] == "54":
                        players[player]["money"] += 5 * players[player]["bit"]
                    else:
                        players[player]["money"] -= players[player]["bit"]
                else:
                    players[player]["money"] += players[player]["bit"]
            else:
                players[player]["money"] -= players[player]["bit"]


# показываем результат ставок
def sport_result_show():
    round_number = [players[player]["round_number"] for player in players][0]
    money_list = list(set([players[player]["money"] for player in players]))
    money_list.sort(reverse=True)
    names_list = []
    last_names_list = []
    for i in range(0, len(money_list)):
        for player in players:
            if players[player]["money"] == money_list[i]:
                names_list.append(players[player]["name"])
                last_names_list.append(players[player]["last_name"])
    money_list = [players[player]["money"] for player in players]
    money_list.sort(reverse=True)
    rows = []
    for i in range(0, len(money_list)):
        row = "".join(names_list[i] + " " + last_names_list[i] + " " + str(money_list[i]) + " " + dollar_word(money_list[i]))
        rows.append(row)
    send_it = "\n".join(rows)
    for player in players:
        bot.send_message(player, f"Результаты {round_number} раунда ставок:\n{send_it}")
    bot.send_message(325051402, f"Результаты {round_number} раунда ставок:\n{send_it}")


# кто на что поставил
def players_bits_table():
    gamers = []
    for player in players:
        gamer = " ".join(players[player]["name"] + players[player]["last_name"] + str(players[player]["bits"][players[player]["round_number"]]))
        gamers.append(gamer)
    return "\n".join(gamers)


# выбираем игрока, который будет ходить в шахматах
def choose_player_for_chess():
    if len(players) > 1:
        if "ходит следующий" in [players[player]["chess"] for player in players]:
            previous = [player for player in players if players[player]["chess"] == "ходит сейчас"][0]
            players[previous]["chess"] = "сходил"
            right_now = [player for player in players if players[player]["chess"] == "ходит следующий"][0]
            players[right_now]["chess"] = "ходит сейчас"
            chess_players = [player for player in players if players[player]["chess"] == 0]
            if len(chess_players) > 0:
                next_one = random.choice(chess_players)
                players[next_one]["chess"] = "ходит следующий"
                bot.send_message(325051402, f"Ходит {players[right_now]['name']} {players[right_now]['last_name']}.\nГотовится {players[next_one]['name']} {players[next_one]['last_name']}.", reply_markup=keyboard_chess())
            else:
                for player in players:
                    if player != right_now:
                        players[player]["chess"] = 0
                chess_players = [player for player in players if players[player]["chess"] == 0]
                next_one = random.choice(chess_players)
                players[next_one]["chess"] = "ходит следующий"
                bot.send_message(325051402, f"Ходит {players[right_now]['name']} {players[right_now]['last_name']}.\nГотовится {players[next_one]['name']} {players[next_one]['last_name']}.", reply_markup=keyboard_chess())
        else:
            chess_players = [player for player in players if players[player]["chess"] == 0]
            right_now = random.choice(chess_players)
            players[right_now]["chess"] = "ходит сейчас"
            chess_players.remove(right_now)
            next_one = random.choice(chess_players)
            players[next_one]["chess"] = "ходит следующий"
            bot.send_message(325051402, f"Ходит {players[right_now]['name']} {players[right_now]['last_name']}.\nГотовится {players[next_one]['name']} {players[next_one]['last_name']}.", reply_markup=keyboard_chess())
    elif len(players) == 1:
        for player in players:
            players[player]["chess"] = "ходит сейчас"
        bot.send_message(325051402, f"Играем в шахматы. {players[player]['name']} {players[player]['last_name']}...", reply_markup=keyboard_chess())
    else:
        bot.send_message(325051402, "Ведущий, в игре нет игроков", reply_markup=keyboard_start_game())


def chess_game(message):
    global game_flag
    if message.data == "eat":
        right_now = [player for player in players if players[player]["chess"] == "ходит сейчас"][0]
        players[right_now]["choose"] = "eat"
        bot.send_message(325051402, f"Что срубил {players[right_now]['name']} {players[right_now]['last_name']}?", reply_markup=keyboard_chesspiece())
    elif message.data == "lose":
        right_now = [player for player in players if players[player]["chess"] == "ходит сейчас"][0]
        players[right_now]["choose"] = "lose"
        bot.send_message(325051402, f"Что потерял {players[right_now]['name']} {players[right_now]['last_name']}?", reply_markup=keyboard_chesspiece())
    elif message.data == "checkmate":
        right_now = [player for player in players if players[player]["chess"] == "ходит сейчас"][0]
        players[right_now]["choose"] = "checkmate"
        bot.send_message(325051402, f"Ведущий, {players[right_now]['name']} {players[right_now]['last_name']} точно поставил мат?", reply_markup=keyboard_really_checkmate())
    elif message.data == "got_checkmate":
        right_now = [player for player in players if players[player]["chess"] == "ходит сейчас"][0]
        players[right_now]["choose"] = "got_checkmate"
        bot.send_message(325051402, f"Ведущий, {players[right_now]['name']} {players[right_now]['last_name']} точно получил мат?", reply_markup=keyboard_really_checkmate())
    elif message.data == "next_player":
        choose_player_for_chess()
    elif message.data == "really_checkmate":
        right_now = [player for player in players if players[player]["chess"] == "ходит сейчас"][0]
        if players[right_now]["choose"] == "checkmate":
            players[right_now]["money"] += 10
            players[right_now]["round_result"] += 10
            bot.send_message(325051402, f"Ведущий, {players[right_now]['name']} {players[right_now]['last_name']} срубил что-нибудь, когда ставил мат?", reply_markup=keyboard_chesspiece())
        elif players[right_now]["choose"] == "got_checkmate":
            players[right_now]["money"] -= 10
            players[right_now]["round_result"] -= 10
            bot.send_message(325051402, f"Ведущий, {players[right_now]['name']} {players[right_now]['last_name']} потерял что-нибудь, когда получил мат?", reply_markup=keyboard_chesspiece())
    elif message.data in chesspiece_price:
        right_now = [player for player in players if players[player]["chess"] == "ходит сейчас"][0]
        if players[right_now]["choose"] == "eat" or players[right_now]["choose"] == "checkmate":
            players[right_now]["money"] += chesspiece_price[message.data]
            players[right_now]["round_result"] += chesspiece_price[message.data]
        elif players[right_now]["choose"] == "lose" or players[right_now]["choose"] == "got_checkmate":
            players[right_now]["money"] -= chesspiece_price[message.data]
            players[right_now]["round_result"] -= chesspiece_price[message.data]
        if players[right_now]["choose"] == "eat":
            bot.send_message(325051402, f"Ведущий, {players[right_now]['name']} {players[right_now]['last_name']} потерял что-нибудь?", reply_markup=keyboard_also_lose())
        elif players[right_now]["choose"] == "lose":
            choose_player_for_chess()
        elif players[right_now]["choose"] == "checkmate" or players[right_now]["choose"] == "got_checkmate":
            for player in players:
                bot.send_message(player, f"Итоги шахматной партии:\n{common_chess_result()}")
            bot.send_message(325051402, f"Итоги шахматного раунда:\n{common_chess_result()}")
            game_flag = "fond_market"
            bot.send_message(325051402, "Ведущий, начнем игру (фонд рынок)?", reply_markup=keyboard_start_game())
    saving()


def common_chess_result():
    money_list = sorted([players[gamer]["money"] for gamer in players], reverse=True)
    short_money_list = sorted(list(set(money_list)), reverse=True)
    name_list = []
    last_name_list = []
    chess_result_list = []
    for money in short_money_list:
        for player in players:
            if players[player]["money"] == money:
                name_list.append(players[player]["name"])
                last_name_list.append(players[player]["last_name"])
                chess_result_list.append(players[player]["round_result"])
    rows = []
    for i in range(len(name_list)):
        row = "".join(name_list[i] + " " + last_name_list[i] + ":" + " " + str(money_list[i]) + " " + dollar_word(money_list[i]) + "\n" + "(шахматный итог: " + str(chess_result_list[i]) + " " + dollar_word(chess_result_list[i]) + ")")
        rows.append(row)
    return "\n".join(rows)


# таблица у кого сколько денег
def rich():
    players_names = []
    players_last_names = []
    money_list = []
    table_list = []
    for player in players:
        players_names.append(players[player]["name"])
        players_last_names.append(players[player]["last_name"])
        money_list.append(players[player]["money"])
    for i in range(0, len(players_names)):
        a = "".join(players_names[i] + " " + players_last_names[i] + " " + str(money_list[i]) + " " + dollar_word(money_list[i]))
        table_list.append(a)
    return "\n".join(table_list)


#  делаем форматирование чисел на выдачу
def finance_formatting(number):
    a = str(number)
    parts = []
    while len(a) > 0:
        part = a[-3:]
        a = a[0:-3]
        parts.append(part)
    parts = parts[::-1]
    result = ""
    for i in range(len(parts)):
        result = " ".join([result, parts[i]])
    return result[1:]


@bot.message_handler(commands=["start", "delete", "cleaning", "rich", "help", "change_game", "correction", "round_result"])  # реакция на команду, которая вводится после /
def command_hadler(message):
    global players
    global game_flag
    if message.text == "/start":
        if message.from_user.id not in players:
            put_gamer_to_base(message)
            players[message.from_user.id] = {}
            players[message.from_user.id]["money"] = -1000000
            players[message.from_user.id]["choose"] = 0
            players[message.from_user.id]["debt"] = 0
            players[message.from_user.id]["finish"] = copy.deepcopy(finish)
            players[message.from_user.id]["name"] = message.from_user.first_name
            players[message.from_user.id]["last_name"] = message.from_user.last_name
            players[message.from_user.id]["companies"] = copy.deepcopy(companies)
            players[message.from_user.id]["bits"] = copy.deepcopy(bits)
            players[message.from_user.id]["bit"] = 0
            players[message.from_user.id]["chess"] = 0
            players[message.from_user.id]["round_result"] = 0
            if len(players) == 1:
                players[message.from_user.id]["round_number"] = 1
                bot.send_message(message.from_user.id, "Добро пожаловать в игру Джентльмен!\nНадеюсь вы были успешны в карточной игре. Сколько вам удалось заработать?")
                bot.send_message(325051402, "Ведущий, начнем игру (ставки)?\n\nТолько не забудь проверить, сколько они внесли на счет - /rich", reply_markup=keyboard_start_game())
            else:
                players[message.from_user.id]["round_number"] = [players[player]["round_number"] for player in players if player != message.from_user.id][0]
                if players[message.from_user.id]["round_number"] == 1 and game_flag == "sport":
                    bot.send_message(message.from_user.id, "Добро пожаловать в игру Джентльмен!\nНадеюсь вы были успешны в карточной игре. Сколько вам удалось заработать?")
                else:
                    players[message.from_user.id]["money"] = min([players[player]["money"] for player in players if player != message.from_user.id])
                    bot.send_message(message.from_user.id, f"Добро пожаловать в игру Джентльмен!\nК сожалению вы пропустили первые раунды, но оставшиеся можете сыграть вместе со всеми.\nВключайтесь в игру!\nУ вас {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}")
                    bot.send_message(325051402, f"Подключился новый игрок - {message.from_user.first_name} {message.from_user.last_name} c {players[message.from_user.id]['money']}")
                    for player in [gamer for gamer in players if gamer != message.from_user.id]:
                            bot.send_message(player, f"В игре новый игрок - {message.from_user.first_name} {message.from_user.last_name} c {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}")
            saving()
        else:
            bot.send_message(message.from_user.id, "Вы уже в игре")
    elif message.text == "/delete":
        bot.send_message(message.from_user.id, "Кого удалим?", reply_markup=delete_keyboard())
    elif message.text == "/cleaning":
        players = {}
        game_flag = "sport"
        bot.send_message(325051402, "Все чисто")
    elif message.text == "/rich":
        bot.send_message(325051402, f"Состояние игроков: {rich()}\nGame_flag = {game_flag}")
    elif message.text == "/help":
        bot.send_message(325051402, "/rich - у кого сколько денег\n\n/delete - удалить одного игрока\n\n/cleaning - удалить всех игроков, флаг на 'sport'\n\n/change_game - сменить раунд игры\n\n/correction - изменить деньги у одного игрока\n\n/round_result - показать резальтаты раунда")
    elif message.text == "/change_game":
        bot.send_message(325051402, "Какой раунд начнем?", reply_markup=keyboard_change_flag())
    elif message.text == "/correction":
        bot.send_message(325051402, "Чье состояние нужно изменить?", reply_markup=correction_keyboard())
    elif message.text == "/round_result":
        bot.send_message(325051402, 'Показать результаты?', reply_markup=keyboard_result())



@bot.callback_query_handler(func=lambda message: True)
def answer(message):
    global players
    global game_flag
    if message.data == 'yes':
        if game_flag == "sport":
            sport_result_counting()
            sport_result_show()
            if [players[player]["round_number"] for player in players][0] != 4:
                bot.send_message(325051402, "Ведущий, начнем новый раунд?", reply_markup=keyboard_begin_round())
            else:
                for player in players:
                    players[player]["round_number"] = 1
                game_flag = "chess"
                bot.send_message(325051402, "Ведущий, начнем игру (шахматы)?", reply_markup=keyboard_start_game())
        else:
            for i in players:
                players[i]["debt"] *= 2
            round_table_str = round_table()
            for player in players:
                if players[player]['round_number'] == 7:
                    players[player]["money"] = (money_result(player) - players[player]["debt"])   # players[player]["money"] = money_result(message.from_user.id) - players[player]["debt"]
                    money = players[player]["money"]
                    bot.send_message(player, f"Незаметно пролетел целый век! Ваш капитал после 105 лет инвестирования составляет {money} {dollar_word(money)}! {delta(money)}\n\n{max_profitable_company(player)}.\n\n{max_profit_from_company(player)}.\n\n{risk_profile(player)}")
                    bot.send_message(player, f"{round_table_str[0]}")
                    bot.send_message(player, f"{round_table_str[1]} ⬇")
                    bot.send_sticker(chat_id=player, data=sticker_3)
                    put_gamer_to_base(message)
                else:
                    if money_result(player) == 0:
                        bot.send_message(player, lose_money(player))
            bot.send_message(325051402, f"{round_table_str[0] if players[player]['round_number'] == 7 else round_table_str}")
            if players[player]['round_number'] < 7:
                bot.send_message(325051402, f"Ведущий, начнем следующий раунд?", reply_markup=keyboard_begin_round())
        saving()
    elif message.data == 'begin':
        if game_flag == "sport":
            for player in players:
                players[player]["round_number"] += 1
                bot.send_message(player, f"{beautiful(player)}\nКак вы считаете, кто победит?", reply_markup=keyboard(player))
        else:
            for player in players:
                if players[player]["round_result"] == 0:
                    players[player]["money"] = debt[players[player]['round_number']]
                    players[player]["debt"] += debt[players[player]['round_number']]
                    players[player]["round_number"] += 1
                    bot.send_message(player, f"{beautiful(player)}\nВ какую компанию вы хотите инвестировать?", reply_markup=keyboard(player))
                else:
                    players[player]["money"] = players[player]["round_result"]
                    players[player]["round_number"] += 1
                    bot.send_message(player, f"{beautiful(player)}\nВ какую компанию вы хотите инвестировать?", reply_markup=keyboard(player))
        saving()
    elif message.data == "start_game":
        if game_flag == "sport":
            for player in players:
                bot.send_message(player, f"{beautiful(player)}\nКак вы считаете, кто победит?", reply_markup=keyboard(player))
        elif game_flag == "chess":
            choose_player_for_chess()
        else:
            for player in players:
                if players[player]["money"] <= 0:
                    players[player]["money"] = 50
                    players[player]["debt"] = 50
                    bot.send_message(player, "К сожалению, вы проиграли в прошлом раунде все свои деньги, зато вы можете хвалиться тем, что проиграли их в шахматы! Состоятельный человек, следивший за вашей игрой, "
                   "одолжил вам 50 долларов, чтобы вы могли продолжить попытки разбогатеть. До конца игры долг будет увеличиваться на 100% каждый раунд и будет вычтен из вашего результата в конце.")
            for player in players:
                bot.send_message(player, f"{beautiful(player)}\nВ какую компанию вы хотите инвестировать?", reply_markup=keyboard(player))
    elif message.data in chess_list:
        chess_game(message)
    elif message.data.isdigit():
        if int(message.data) in [player for player in players]:
            leaver = int(message.data)
            bot.send_message(325051402, f"{players[leaver]['name']} {players[leaver]['last_name']} удален из игры")
            players.pop(leaver)
            saving()
        else:
            bot.send_message(325051402, "Этот игрок уже был удален ранее")
    elif message.data == 'round_sport':
        game_flag = "sport"
        bot.send_message(325051402, "Ведущий, начнем игру (ставки)?", reply_markup=keyboard_start_game())
    elif message.data == 'round_chess':
        game_flag = "chess"
        bot.send_message(325051402, "Ведущий, начнем игру (шахматы)?", reply_markup=keyboard_start_game())
    elif message.data == 'round_fond_market':
        game_flag = "fond_market"
        bot.send_message(325051402, "Ведущий, начнем игру (фонд рынок)?", reply_markup=keyboard_start_game())
    elif message.data[:10] == "correction":
        if 325051402 in players:
            players[325051402]["correction"] = int(message.data[11:])
        else:
            players[325051402] = {}
            players[325051402]["correction"] = int(message.data[11:])
        bot.send_message(325051402, f"Сколько денег должно быть у {players[int(message.data[11:])]['name']} {players[int(message.data[11:])]['last_name']}?")
    else:
        if message.data in sports_list:
            sport_bits(message)
            saving()
        else:
            if message.data in round_list(message.from_user.id):
                bot.send_message(message.from_user.id, f"Сколько вы хотите инвестировать в {message.data}?\nСвободные средства — {players[message.from_user.id]['money'] - sum([i for i in players[message.from_user.id]['companies'][players[message.from_user.id]['round_number']].values()])} {dollar_word(players[message.from_user.id]['money'] - sum([i for i in players[message.from_user.id]['companies'][players[message.from_user.id]['round_number']].values()]))}.")
                players[message.from_user.id]["choose"] = message.data
                saving()
            else:
                bot.send_message(message.from_user.id, f'Компания "{message.data}" более не нуждается в инвестициях. Выберите компанию из нынешнего раунда.')


@bot.message_handler(content_types=["text"])
def sticker_hadler(message):
    global players
    if message.from_user.id in players:
        if message.text.isdigit() == False:
            small_talk(message)
        else:
            if message.from_user.id == 325051402 and "correction" in players[325051402]:
                players[players[325051402]["correction"]]["money"] = int(message.text)
                bot.send_message(325051402, f'{players[players[325051402]["correction"]]["name"]} {players[players[325051402]["correction"]]["last_name"]} теперь играет с {players[players[325051402]["correction"]]["money"]}')
                bot.send_message(players[325051402]["correction"], f'У вас {finance_formatting(players[players[325051402]["correction"]]["money"])} {dollar_word(players[players[325051402]["correction"]]["money"])}')
                if len(players[325051402]) == 1:
                    players.pop(325051402)
                else:
                    players[325051402].pop("correction")
            else:
                if players[message.from_user.id]["money"] == -1000000:
                    players[message.from_user.id]["money"] = int(message.text)
                    bot.send_message(message.from_user.id, "Вы в игре. Дождемся остальных и начнем.")
                    bot.send_message(325051402, f"{players[message.from_user.id]['name']} {players[message.from_user.id]['last_name']} вошел с {players[message.from_user.id]['money']} долларами")
                elif game_flag == "sport":
                    if int(message.text) > players[message.from_user.id]['money']:
                        bot.send_message(message.from_user.id, f"К сожалению, у вас только {players[message.from_user.id]['money']} {dollar_word(players[message.from_user.id]['money'])}.\nСколько вы хотите поставить?")
                    else:
                        players[message.from_user.id]["bit"] = int(message.text)
                        bot.send_message(message.from_user.id, "Ваша ставка принята. Подождем остальных и посмотрим, чья ставка сыграла.")
                        if 0 not in [players[player]["bit"] for player in players]:
                            bot.send_message(325051402, players_bits_table())
                            bot.send_message(325051402, "Ведущий, все сделали ставки. Показать результаты?", reply_markup=keyboard_result())
                else:
                    if players[message.from_user.id]['choose'] in round_list(message.from_user.id):
                        investment = int(message.text)
                        money = players[message.from_user.id]["money"]
                        round_investment = sum([i for i in players[message.from_user.id]["companies"][players[message.from_user.id]["round_number"]].values()])
                        if investment > money - round_investment:
                            bot.send_message(message.from_user.id, f"К сожалению, у вас только {money - round_investment} {dollar_word(money - round_investment)}. Сколько вы хотите инвестировать в {players[message.from_user.id]['choose']}?")
                        else:
                            players[message.from_user.id]["companies"][players[message.from_user.id]["round_number"]][players[message.from_user.id]["choose"]] += investment
                            round_investment = sum([i for i in players[message.from_user.id]["companies"][players[message.from_user.id]["round_number"]].values()])
                            if money == round_investment:
                                players[message.from_user.id]["round_result"] = money_result(message.from_user.id)
                                bot.send_message(message.from_user.id, f"Свободные средства закончились. Ваши инвестиции:\n{already_invested(message.from_user.id)}.\n\nКраткая справка об этом периоде истории.\n\n{yesfraselist[players[message.from_user.id]['round_number'] - 1]}")
                                bot.send_message(325051402, f'{players[message.from_user.id]["name"]} закончил {players[message.from_user.id]["round_number"]} раунд c {money_result(message.from_user.id)} долларов')
                                players[message.from_user.id]["finish"][players[message.from_user.id]["round_number"]] = 1
                                if sum([players[i]["finish"][players[message.from_user.id]["round_number"]] for i in players]) == len(players):
                                    bot.send_message(325051402, 'Ведущий, разреши посмотреть результаты', reply_markup=keyboard_result())
                                    bot.send_message(325051402, investment_table())
                            else:
                                bot.send_message(message.from_user.id, f"Не останавливайтесь, у вас еще {money - round_investment} {dollar_word(money - round_investment)}.\n\nВы уже проинвестировали:\n{already_invested(message.from_user.id)}.\n\nЧьи акции хотите купить?", reply_markup=keyboard(message.from_user.id))
                    else:
                        bot.send_message(message.from_user.id, "Сначала выберите компанию из списка предложенного выше. Иначе мы раздадим ваши деньги стартаперам из Сколково.")
        saving()
    else:
        bot.send_message(message.from_user.id, 'Извините, мне разрешают разговаривать только с участниками игры. Чтобы начать игру, нажмите сюда >>> /start')


@bot.message_handler(content_types=["sticker"])     # отправил стикер в ответ на стикер
def sticker_hadler(message):
    bot.send_sticker(chat_id=message.from_user.id, data=sticker)


bot.polling(timeout=60)
