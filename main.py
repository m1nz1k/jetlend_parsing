import requests
import db_api as commands
import asyncio
import json
import time




########################################################################################################################
async def secondary_main():
    cookies = {
        '_jl_uid': 'vETZ4WUILvEgftokBER4Ag==',
        '_gcl_au': '1.1.1801966748.1695035050',
        'referrer': 'https://client.work-zilla.com/',
        '_ym_uid': '1695035051576708091',
        '_ym_d': '1695035051',
        'tmr_lvid': '79a9abd783270f5e68cbc6f0ba57bfa2',
        'tmr_lvidTS': '1695035055405',
        '_tt_enable_cookie': '1',
        '_ttp': 'rALbsDXw_v8KYn8xszNzyrPqCrx',
        'jl_features': 'headerFeatures%3Dheader_1_counter%3BfeedbacksFeature%3Ddefault%3BpopUpInvestorFeature%3Ddefault',
        '_gid': 'GA1.2.244274248.1697817596',
        '_ym_visorc': 'b',
        '_ym_isad': '1',
        '_clck': 'flvtcj|2|fg0|0|1373',
        'csrftoken': 'YdMujkr5zKr25QfI5KzAHfwdYC0pGg3O',
        'sessionid': '7fhol55ac5e230ill0mtm43cfnx65nry',
        '_ga_NR0DV46HQK': 'GS1.1.1697817596.31.1.1697817673.50.0.0',
        '_ga': 'GA1.2.97225234.1695035049',
        'tmr_detect': '1%7C1697817673555',
        '_clsk': '1qy797u|1697817888574|10|1|i.clarity.ms/collect',
    }

    headers = {
        'authority': 'jetlend.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=utf-8',
        'referer': 'https://jetlend.ru/invest/v3/company/16578/loans',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    params = {
        'limit': '100000',
        'offset': '0',
        'sort_dir': 'desc',
        'sort_field': 'ytm',
    }
    while True:
        try:
            response = requests.get('https://jetlend.ru/invest/api/exchange/loans', params=params, cookies=cookies,
                                    headers=headers).json()
        except Exception as ex:
            print(f'Запрос не прошел: {ex}')
            continue
        ids_company_list = []
        for num in response['data']:
            ids_company_list.append(num['loan_id'])

        ################## получаем список компаний, которые есть с БД, но нет в списке и удаляем ######################
        ids_to_delete = []

        db_ids = await commands.secondary_get_all_company_ids()

        for db_id in db_ids:
            if db_id not in ids_company_list:
                ids_to_delete.append(db_id)

        for id_to_delete in ids_to_delete:
            await commands.secondary_delete_company_by_id(id_to_delete)
        ################################################################################################################

        for num in ids_company_list:
            # Проверяем, есть ли id в БД
            if not await commands.secondary_select_id_company(num):
                # Если id отсутствует, то добавляем его и получаем информацию
                result = await secondary_add_company_and_get_info(num, headers, cookies)
                if result:
                    print(f'Вторичный рынок | Добавляю в БД компанию с id {num}')

        # Пауза на 10 секунд перед следующей проверкой
        time.sleep(10)


async def secondary_add_company_and_get_info(company_id, headers, cookies):
    try:
        await secondary_get_first_info(company_id, headers, cookies)
        await secondary_get_two_info(company_id, headers, cookies)
        await secondary_get_three_info(company_id, headers, cookies)
        await secondary_get_four_info(company_id, headers, cookies)
        await secondary_get_six_info(company_id, headers, cookies)
        print(f'Вторичный рынок | Компания {company_id} успешно добавлена.')
        return True  # Успешно добавлено
    except Exception as ex:
        print(f'Вторичный рынок | Ошибка со стороны сервера - \n{ex}')
        return False  # Произошла ошибка
async def secondary_get_first_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/info', cookies=cookies, headers=headers).json()
    # Извлечение значений
    amount = response['data'].get('amount', '')  # Сумма
    company = response['data'].get('company', '')  # ООО ИП и т.п
    loan_name = response['data'].get('loan_name', '')  # Название компании
    interest_rate = response['data'].get('interest_rate', '')  # ставка %
    term = response['data'].get('term', '') # Срок в днях
    interest_rate = round(float(interest_rate) * 100, 2)
    rating_mapping = {
        'AAA+': 1,
        'AAA': 2,
        'AA+': 3,
        'AA': 4,
        'A+': 5,
        'A': 6,
        'BBB+': 7,
        'BBB': 8,
        'BB+': 9,
        'BB': 10,
        'B+': 11,
        'B': 12,
        'CCC+': 13,
        'CCC': 14,
        'CC+': 15,
        'CC': 16,
        'C+': 17,
        'C': 18
    }

    # Получение рейтинга в буквах из response
    rating = response['data'].get('rating', '')  # Рейтинг

    # Преобразование рейтинга в числовое значение
    numeric_rating = rating_mapping.get(rating, None)
    await commands.secondary_add_primary_placement(company=company,
                                         rating=str(numeric_rating),
                                         amount=str(amount),
                                         interest_rate=str(interest_rate),
                                         term_in_days=str(term),
                                         id_company=int(num))


async def secondary_get_two_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/details', cookies=cookies, headers=headers).json()
    # Извлечение значений из раздела "details"
    details = response['data'].get('details', {})
    address = details.get('address', '')  # Адрес
    inn_details = details.get('inn', '')  # ИНН организации
    ogrn = details.get('ogrn', '')  # ОГРН организации
    primaryCatergory = details.get('primaryCatergory', '')  # Категория компании
    profile = details.get('profile', '')  # Ссылка на профиль
    registrationDate = details.get('registrationDate', '')  # Дата регистрации
    site = details.get('site', '') # Сайт компании
    revenueForPastYear = details.get('revenueForPastYear', '') # Выручка за год
    profitForPastYear = details.get('profitForPastYear', '') # Прибыль за год

    # Извлечение значений из раздела "management"
    management_info = []  # Создаем пустой список для хранения информации о человеках
    management = response['data'].get('management', {})  # Получаем раздел "management" или пустой словарь, если его нет


    # Перебираем каждого человека в разделе "management"
    if isinstance(management, dict):
        name = management.get('name', '')  # ФИО человека
        inn_management = management.get('inn', '')  # ИНН человека
        # position = management.get('position', '')  # Должность
        full_text = f'{name}, {inn_management}'
        management_info.append(full_text)


    for user in response['data']['founders']:
        name = user.get('name', '')  # ФИО человека
        inn_management = user.get('inn', '')  # ИНН человека
        share = user.get('share', '')  # Должность (По дефолту является участником. Это процент)
        if share is not None:
            try:
                share_float = float(share)
                full_text = f'{name}, {inn_management}'
            except Exception:
                full_text = f'{name}, {inn_management}'
        else:
            full_text = f'{name}, {inn_management}'

        management_info.append(full_text)
    companies_data_json = "\n".join(management_info)
    await commands.secondary_add_secondary_placement(id_company=num,
                                           address=str(address),
                                         inn_company=str(inn_details),
                                         ogrn=str(ogrn),
                                         primaryCatergory=primaryCatergory,
                                         contr_focus_link=str(profile),
                                         registration_date=str(registrationDate),
                                         site_link=str(site),
                                         revenue_for_year=str(revenueForPastYear),
                                         profit_for_year=str(profitForPastYear),
                                         user_list=companies_data_json)


async def secondary_get_three_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/analytics', cookies=cookies, headers=headers).json()
    # Извлечение значений из arbitration_cases
    plaintiff_all_time = response['data']['arbitration_cases'][0]['stats']['all'].get('amount',
                                                                                      '')  # истец за все время
    defendant_all_time = response['data']['arbitration_cases'][1]['stats']['all'].get('amount',
                                                                                      '')  # защита на все время

    plaintiff_one_year = response['data']['arbitration_cases'][0]['stats']['one_year'].get('amount',
                                                                                           '')  # истец за 1 год
    defendant_one_year = response['data']['arbitration_cases'][1]['stats']['one_year'].get('amount',
                                                                                           '')  # защита за 1 год

    plaintiff_three_years = response['data']['arbitration_cases'][0]['stats']['three_years'].get('amount',
                                                                                                 '')  # истец за 3 года
    defendant_three_years = response['data']['arbitration_cases'][1]['stats']['three_years'].get('amount',
                                                                                                 '')  # защита за 3 года

    # Извлечение значений из enforcement
    enforcement_last_year_total_amount = response['data']['enforcement'][0].get('total_amount',
                                                                                '')  # исполнительные производства за 1 год
    enforcement_all_time_total_amount = response['data']['enforcement'][1].get('total_amount',
                                                                               '')  # исполнительные производства за все время

    # Извлечение значений из taxes_fees
    fees_pfr = response['data']['taxes_fees'].get('fees_pfr', '')  # Взносы ПФР
    total_payed = response['data']['taxes_fees'].get('total_payed', '')  # Всего уплачено
    vat = response['data']['taxes_fees'].get('vat', '')  # НДС
    transport_tax = response['data']['taxes_fees'].get('transport_tax', '')  # Транспортный налог

    # Извлечение значений из year_finances
    balance = response['data']['year_finances'].get('balance', '')  # Баланс
    earnings = response['data']['year_finances'].get('earnings', '')  # Выручка
    profit = response['data']['year_finances'].get('profit', '')  # Профит

    JetLend = response['data']['loans'][0].get('amount', '') # джет ленд
    JetLend_next = response['data']['loans'][1].get('amount', '') # другие

    member_amount = response['data']['gov_contracts'].get('member_amount', '') # Гос.Контракт (участник)
    contract_amount = response['data']['gov_contracts'].get('contract_amount', '') # Гос.Контракт (Контракт заключен)

    await commands.secondary_add_third_step(id_company=num,
                                  plantiff_all_time=str(plaintiff_all_time),
                            plantiff_one_year=str(plaintiff_one_year),
                            plantiff_three_years=str(plaintiff_three_years),
                            defendant_all_time=str(defendant_all_time),
                            defendant_one_year=str(defendant_one_year),
                            defendant_three_years=str(defendant_three_years),
                            enforcement_all_time_total_amount=str(enforcement_all_time_total_amount),
                            enforcement_last_year_total_amount=str(enforcement_last_year_total_amount),
                            pfr=str(fees_pfr),
                            total_payed=str(total_payed),
                            vat=str(vat),
                            transport_tax=str(transport_tax),
                            balance=str(balance),
                            earnings=str(earnings),
                            profit=str(profit),
                            jetlend=str(JetLend),
                            other=str(JetLend_next),
                            gos_contract_member=str(member_amount),
                            gos_contract_concluded=str(contract_amount))


async def secondary_get_four_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/loans', cookies=cookies, headers=headers).json()
    # Создаем пустой список для хранения данных о компаниях
    companies_data = []
    sum_amount = 0.0
    # Перебираем каждую компанию и извлекаем необходимые данные
    for loan in response["loans"]:
        amount = loan.get("amount", "")  # Сумма

        sum_amount += float(amount)
        interest_rate = loan.get("interest_rate", "")  # Ставка
        interest_rate = round(float(interest_rate) * 100, 2)

        date = loan.get("date", "")  # Срок
        date = date.split('T')[0]
        rating_mapping = {
            'AAA+': 1,
            'AAA': 2,
            'AA+': 3,
            'AA': 4,
            'A+': 5,
            'A': 6,
            'BBB+': 7,
            'BBB': 8,
            'BB+': 9,
            'BB': 10,
            'B+': 11,
            'B': 12,
            'CCC+': 13,
            'CCC': 14,
            'CC+': 15,
            'CC': 16,
            'C+': 17,
            'C': 18
        }

        # Получение рейтинга в буквах из response
        rating = loan.get('rating', '')  # Рейтинг

        # Преобразование рейтинга в числовое значение
        numeric_rating = rating_mapping.get(rating, None)
        full_text = f'Сумма {amount} Ставка {interest_rate}% Дата {date} Рейтинг {numeric_rating}'
        # Добавляем данные о компании в список
        companies_data.append((full_text))
    companies_data_json = "\n".join(companies_data)
    await commands.secondary_add_fourth_step(id_company=num,
                                            all_issues=companies_data_json,
                                            sum_amount=str(sum_amount))


async def secondary_get_six_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/events', cookies=cookies, headers=headers).json()

    # Создаем пустой список для хранения событий
    events_list = []

    # Перебираем каждое событие и извлекаем необходимые данные (title, date)
    for event in response["events"]:
        title = event.get("title", "")  # Название события
        date = event.get("date", "")  # Дата
        date = date.split('T')[0]
        full_text = f'{title} {date}'

        # Добавляем событие в список в формате (title, date)
        events_list.append((full_text))
    companies_data_json = "\n".join(events_list)
    await commands.secondary_add_fifth_step(id_company=num,
                                  events=companies_data_json)

########################################################################################################################

async def main():
    cookies = {
        '_jl_uid': 'vETZ4WUILvEgftokBER4Ag==',
        '_gcl_au': '1.1.1801966748.1695035050',
        'referrer': 'https://client.work-zilla.com/',
        '_ym_uid': '1695035051576708091',
        '_ym_d': '1695035051',
        'tmr_lvid': '79a9abd783270f5e68cbc6f0ba57bfa2',
        'tmr_lvidTS': '1695035055405',
        '_tt_enable_cookie': '1',
        '_ttp': 'rALbsDXw_v8KYn8xszNzyrPqCrx',
        'jl_features': 'headerFeatures%3Dheader_1_counter%3BfeedbacksFeature%3Ddefault%3BpopUpInvestorFeature%3Ddefault',
        '_gid': 'GA1.2.244274248.1697817596',
        '_ym_visorc': 'b',
        '_ym_isad': '1',
        '_clck': 'flvtcj|2|fg0|0|1373',
        'csrftoken': 'YdMujkr5zKr25QfI5KzAHfwdYC0pGg3O',
        'sessionid': '7fhol55ac5e230ill0mtm43cfnx65nry',
        '_ga_NR0DV46HQK': 'GS1.1.1697817596.31.1.1697817673.50.0.0',
        '_ga': 'GA1.2.97225234.1695035049',
        'tmr_detect': '1%7C1697817673555',
        '_clsk': '1qy797u|1697817888574|10|1|i.clarity.ms/collect',
    }

    headers = {
        'authority': 'jetlend.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=utf-8',
        'referer': 'https://jetlend.ru/invest/v3/company/16578/loans',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    while True:
        try:
            response = requests.get('https://jetlend.ru/invest/api/requests/waiting', cookies=cookies,
                                    headers=headers).json()
        except Exception as ex:
            print(f'Запрос не прошел: {ex}')
            continue
        ids_company_list = []
        for num in response['requests']:
            ids_company_list.append(num['id'])

        ################## получаем список компаний, которые есть с БД, но нет в списке и удаляем ######################
        ids_to_delete = []

        db_ids = await commands.get_all_company_ids()

        for db_id in db_ids:
            if db_id not in ids_company_list:
                ids_to_delete.append(db_id)

        for id_to_delete in ids_to_delete:
            await commands.delete_company_by_id(id_to_delete)
        ################################################################################################################

        for num in ids_company_list:
            # Проверяем, есть ли id в БД
            if not await commands.select_id_company(num):
                # Если id отсутствует, то добавляем его и получаем информацию
                result = await add_company_and_get_info(num, headers, cookies)
                if result:
                    print(f'Рынок первичных размещений | Добавляю в БД компанию с id {num}')

        # Пауза на 10 секунд перед следующей проверкой
        time.sleep(10)


async def add_company_and_get_info(company_id, headers, cookies):
    try:
        await get_first_info(company_id, headers, cookies)
        await get_two_info(company_id, headers, cookies)
        await get_three_info(company_id, headers, cookies)
        await get_four_info(company_id, headers, cookies)
        await get_six_info(company_id, headers, cookies)
        print(f'Рынок первичных размещений | Компания {company_id} успешно добавлена.')
        return True  # Успешно добавлено
    except Exception as ex:
        print(f'Рынок первичных размещений | Ошибка со стороны сервера \n{ex}')
        return False  # Произошла ошибка

async def get_first_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/info', cookies=cookies, headers=headers).json()
    # Извлечение значений
    amount = response['data'].get('amount', '')  # Сумма
    company = response['data'].get('company', '')  # ООО ИП и т.п
    loan_name = response['data'].get('loan_name', '')  # Название компании
    interest_rate = response['data'].get('interest_rate', '')  # ставка %
    term = response['data'].get('term', '') # Срок в днях
    interest_rate = round(float(interest_rate) * 100, 2)
    rating_mapping = {
        'AAA+': 1,
        'AAA': 2,
        'AA+': 3,
        'AA': 4,
        'A+': 5,
        'A': 6,
        'BBB+': 7,
        'BBB': 8,
        'BB+': 9,
        'BB': 10,
        'B+': 11,
        'B': 12,
        'CCC+': 13,
        'CCC': 14,
        'CC+': 15,
        'CC': 16,
        'C+': 17,
        'C': 18
    }

    # Получение рейтинга в буквах из response
    rating = response['data'].get('rating', '')  # Рейтинг

    # Преобразование рейтинга в числовое значение
    numeric_rating = rating_mapping.get(rating, None)
    await commands.add_primary_placement(company=company,
                                         rating=str(numeric_rating),

                                         amount=str(amount),
                                         interest_rate=str(interest_rate),
                                         term_in_days=str(term),
                                         id_company=int(num))


async def get_two_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/details', cookies=cookies, headers=headers).json()
    # Извлечение значений из раздела "details"
    details = response['data'].get('details', {})
    address = details.get('address', '')  # Адрес
    inn_details = details.get('inn', '')  # ИНН организации
    ogrn = details.get('ogrn', '')  # ОГРН организации
    primaryCatergory = details.get('primaryCatergory', '')  # Категория компании
    profile = details.get('profile', '')  # Ссылка на профиль
    registrationDate = details.get('registrationDate', '')  # Дата регистрации
    site = details.get('site', '') # Сайт компании
    revenueForPastYear = details.get('revenueForPastYear', '') # Выручка за год
    profitForPastYear = details.get('profitForPastYear', '') # Прибыль за год

    # Извлечение значений из раздела "management"
    management_info = []  # Создаем пустой список для хранения информации о человеках
    management = response['data'].get('management', {})  # Получаем раздел "management" или пустой словарь, если его нет


    # Перебираем каждого человека в разделе "management"
    if isinstance(management, dict):
        name = management.get('name', '')  # ФИО человека
        inn_management = management.get('inn', '')  # ИНН человека
        # position = management.get('position', '')  # Должность
        full_text = f'{name}, {inn_management}'
        management_info.append((full_text))

    for user in response['data']['founders']:
        name = user.get('name', '')  # ФИО человека
        inn_management = user.get('inn', '')  # ИНН человека
        share = user.get('share', '')  # Должность (По дефолту является участником. Это процент)
        if share is not None:
            try:
                share_float = float(share)
                full_text = f'{name}, {inn_management}'
            except Exception:
                full_text = f'{name}, {inn_management}'
        else:
            full_text = f'{name}, {inn_management}'
        management_info.append((full_text))
    companies_data_json = "\n".join(management_info)
    await commands.add_secondary_placement(id_company=num,
                                           address=str(address),
                                         inn_company=str(inn_details),
                                         ogrn=str(ogrn),
                                         primaryCatergory=primaryCatergory,
                                         contr_focus_link=str(profile),
                                         registration_date=str(registrationDate),
                                         site_link=str(site),
                                         revenue_for_year=str(revenueForPastYear),
                                         profit_for_year=str(profitForPastYear),
                                         user_list=companies_data_json)


async def get_three_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/analytics', cookies=cookies, headers=headers).json()
    # Извлечение значений из arbitration_cases
    plaintiff_all_time = response['data']['arbitration_cases'][0]['stats']['all'].get('amount',
                                                                                      '')  # истец за все время
    defendant_all_time = response['data']['arbitration_cases'][1]['stats']['all'].get('amount',
                                                                                      '')  # защита на все время

    plaintiff_one_year = response['data']['arbitration_cases'][0]['stats']['one_year'].get('amount',
                                                                                           '')  # истец за 1 год
    defendant_one_year = response['data']['arbitration_cases'][1]['stats']['one_year'].get('amount',
                                                                                           '')  # защита за 1 год

    plaintiff_three_years = response['data']['arbitration_cases'][0]['stats']['three_years'].get('amount',
                                                                                                 '')  # истец за 3 года
    defendant_three_years = response['data']['arbitration_cases'][1]['stats']['three_years'].get('amount',
                                                                                                 '')  # защита за 3 года

    # Извлечение значений из enforcement
    enforcement_last_year_total_amount = response['data']['enforcement'][0].get('total_amount',
                                                                                '')  # исполнительные производства за 1 год
    enforcement_all_time_total_amount = response['data']['enforcement'][1].get('total_amount',
                                                                               '')  # исполнительные производства за все время

    # Извлечение значений из taxes_fees
    fees_pfr = response['data']['taxes_fees'].get('fees_pfr', '')  # Взносы ПФР
    total_payed = response['data']['taxes_fees'].get('total_payed', '')  # Всего уплачено
    vat = response['data']['taxes_fees'].get('vat', '')  # НДС
    transport_tax = response['data']['taxes_fees'].get('transport_tax', '')  # Транспортный налог

    # Извлечение значений из year_finances
    balance = response['data']['year_finances'].get('balance', '')  # Баланс
    earnings = response['data']['year_finances'].get('earnings', '')  # Выручка
    profit = response['data']['year_finances'].get('profit', '')  # Профит

    JetLend = response['data']['loans'][0].get('amount', '') # джет ленд
    JetLend_next = response['data']['loans'][1].get('amount', '') # другие

    member_amount = response['data']['gov_contracts'].get('member_amount', '') # Гос.Контракт (участник)
    contract_amount = response['data']['gov_contracts'].get('contract_amount', '') # Гос.Контракт (Контракт заключен)

    await commands.add_third_step(id_company=num,
                                  plantiff_all_time=str(plaintiff_all_time),
                            plantiff_one_year=str(plaintiff_one_year),
                            plantiff_three_years=str(plaintiff_three_years),
                            defendant_all_time=str(defendant_all_time),
                            defendant_one_year=str(defendant_one_year),
                            defendant_three_years=str(defendant_three_years),
                            enforcement_all_time_total_amount=str(enforcement_all_time_total_amount),
                            enforcement_last_year_total_amount=str(enforcement_last_year_total_amount),
                            pfr=str(fees_pfr),
                            total_payed=str(total_payed),
                            vat=str(vat),
                            transport_tax=str(transport_tax),
                            balance=str(balance),
                            earnings=str(earnings),
                            profit=str(profit),
                            jetlend=str(JetLend),
                            other=str(JetLend_next),
                            gos_contract_member=str(member_amount),
                            gos_contract_concluded=str(contract_amount))


async def get_four_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/loans', cookies=cookies, headers=headers).json()
    # Создаем пустой список для хранения данных о компаниях
    companies_data = []
    sum_amount = 0.0
    # Перебираем каждую компанию и извлекаем необходимые данные
    for loan in response["loans"]:
        amount = loan.get("amount", "")  # Сумма
        sum_amount += float(amount)
        interest_rate = loan.get("interest_rate", "")  # Ставка
        interest_rate = round(float(interest_rate) * 100, 2)

        date = loan.get("date", "")  # Срок
        date = date.split('T')[0]
        rating_mapping = {
            'AAA+': 1,
            'AAA': 2,
            'AA+': 3,
            'AA': 4,
            'A+': 5,
            'A': 6,
            'BBB+': 7,
            'BBB': 8,
            'BB+': 9,
            'BB': 10,
            'B+': 11,
            'B': 12,
            'CCC+': 13,
            'CCC': 14,
            'CC+': 15,
            'CC': 16,
            'C+': 17,
            'C': 18
        }

        # Получение рейтинга в буквах из response
        rating = loan.get('rating', '')  # Рейтинг

        # Преобразование рейтинга в числовое значение
        numeric_rating = rating_mapping.get(rating, None)
        full_text = f'Сумма {amount} Ставка {interest_rate}% Дата {date} Рейтинг {numeric_rating}'
        # Добавляем данные о компании в список
        companies_data.append((full_text))
    companies_data_json = "\n".join(companies_data)
    await commands.add_fourth_step(id_company=num,
                                   all_issues=companies_data_json,
                                   sum_amount=str(sum_amount))


async def get_six_info(num, headers, cookies):
    response = requests.get(f'https://jetlend.ru/invest/api/requests/{num}/events', cookies=cookies, headers=headers).json()

    # Создаем пустой список для хранения событий
    events_list = []

    # Перебираем каждое событие и извлекаем необходимые данные (title, date)
    for event in response["events"]:
        title = event.get("title", "")  # Название события
        date = event.get("date", "")  # Дата
        date = date.split('T')[0]
        full_text = f'{title} {date}'

        # Добавляем событие в список в формате (title, date)
        events_list.append((full_text))
    companies_data_json = "\n".join(events_list)
    await commands.add_fifth_step(id_company=num,
                                  events=companies_data_json)
########################################################################################################################
if __name__ == '__main__':
    async def loader():
        loop = asyncio.get_event_loop()
        await commands.init_db(),
        await commands.create_tables(),
        await asyncio.gather(
            main(),
            secondary_main()
        )

    asyncio.run(loader())