# Импорты
from gino import Gino
import asyncio

# Создание объекта Gino
db = Gino()

# Настройки подключения к PostgreSQL
DATABASE_URL = 'postgresql://postgres:eugen123@localhost/jetlend'

# Модель "Рынка первичных размещений" ##################################################################################
class Primary_Placement_Market(db.Model):
    __tablename__ = 'Primary_Placement_Markets'
    # Первый заход
    id = db.Column(db.Integer(), primary_key=True, doc="Идентификатор")
    company = db.Column(db.String, doc="Название компании")  # Название компании
    rating = db.Column(db.String, doc="Рейтинг компании")  # Рейтинг компании
    amount = db.Column(db.String, doc="Сумма")  # Сумма
    interest_rate = db.Column(db.String, doc="Ставка в %")  # Ставка в %
    term_in_days = db.Column(db.String, doc="Срок в днях")  # Срок в днях
    id_company = db.Column(db.Integer, doc="ID компании на сайте")  # id компании на сайте, откуда берем.

    # Второй заход
    address = db.Column(db.String, doc="Адрес организации")  # Адресс организации
    inn_company = db.Column(db.String, doc="ИНН организации")  # ИНН организации
    ogrn = db.Column(db.String, doc="ОГРН организации")  # ОГРН организации
    primaryCatergory = db.Column(db.String, doc="Категория компании")  # Категория компании
    contr_focus_link = db.Column(db.String, doc="Ссылка на КонтрФокус")  # КонтрФокус Ссылка
    registration_date = db.Column(db.String, doc="Дата регистрации")  # Дата регистрации
    site_link = db.Column(db.String, doc="Ссылка на сайт компании")  # Ссылка на сайт компании
    revenue_for_year = db.Column(db.String, doc="Выручка за год")  # Выручка за год
    profit_for_year = db.Column(db.String, doc="Прибыль за год")  # Прибыль за год
    user_list = db.Column(db.String, doc="Список участников: ФИО, ИНН, Роль в компании")  # Список участников: ФИО, ИНН, Роль в компании

    # Третий заход
    plantiff_all_time = db.Column(db.String, doc="Истец за все время")  # Истец за все время
    plantiff_one_year = db.Column(db.String, doc="Истец за один год")  # Истец за один год
    plantiff_three_years = db.Column(db.String, doc="Истец за три года")  # Истец за три года
    defendant_all_time = db.Column(db.String, doc="Защита за все время")  # Защита за все время
    defendant_one_year = db.Column(db.String, doc="Защита за один год")  # Защита за один год
    defendant_three_years = db.Column(db.String, doc="Защита за три года")  # Защита за три года
    enforcement_last_year_total_amount = db.Column(db.String,
                                                   doc="Исполнительные производства за 1 год")  # Исполнительные производства за 1 год
    enforcement_all_time_total_amount = db.Column(db.String,
                                                  doc="Исполнительные производства за все время")  # Исполнительные производства за все время
    pfr = db.Column(db.String, doc="Взносы ПФР")  # Взносы ПФР
    vat = db.Column(db.String, doc="НДС")  # НДС
    total_payed = db.Column(db.String, doc="Всего уплачено")  # Всего уплачено
    transport_tax = db.Column(db.String, doc="Транспортный налог")  # Транспортный налог
    balance = db.Column(db.String, doc="Баланс")  # Баланс
    earnings = db.Column(db.String, doc="Выручка")  # Выручка
    profit = db.Column(db.String, doc="Чистая прибыль")  # Чистая прибыль
    jetlend = db.Column(db.String, doc="Джет Ленд")  # Джет Ленд
    other = db.Column(db.String, doc="Другие")  # Другие
    gos_contract_member = db.Column(db.String, doc="Гос.Контракт - Участник")  # Гос.Контракт - Участник
    gos_contract_concluded = db.Column(db.String, doc="Гос.Контракт - Заключен")  # Гос.Контракт - Заключен

    # Четвертый заход
    all_issues = db.Column(db.String, doc="Все выпуски: Сумма, ставка, дата")  # Все выпуски: Сумма, ставка, дата
    sum_amount = db.Column(db.String, doc="Сумма займов") # Сумма займов.

    # Пятый заход
    events = db.Column(db.String, doc="Список событий: Название, дата")  # Список событий: Название, дата

async def select_id_company(id_company: int):
    id_company = await Primary_Placement_Market.query.where(Primary_Placement_Market.id_company == id_company).gino.first()
    return id_company

async def get_all_company_ids():
    query = Primary_Placement_Market.query.distinct(Primary_Placement_Market.id_company)
    result = await query.gino.all()
    return [row.id_company for row in result] if result else []

# Функция для первого захода
async def add_primary_placement(company, rating, amount, interest_rate, term_in_days, id_company):
    await Primary_Placement_Market.create(
        company=company,
        rating=rating,
        amount=amount,
        interest_rate=interest_rate,
        term_in_days=term_in_days,
        id_company=id_company
    )

# Функция для второго захода
async def add_secondary_placement(id_company, address, inn_company, ogrn, primaryCatergory, contr_focus_link, registration_date, site_link, revenue_for_year, profit_for_year, user_list):
    id_company = await select_id_company(id_company)
    await id_company.update(address=address,


                                        inn_company=inn_company,
                                        ogrn=ogrn,
                                        primaryCatergory=primaryCatergory,
                                        contr_focus_link=contr_focus_link,
                                        registration_date=registration_date,
                                        site_link=site_link,
                                        revenue_for_year=revenue_for_year,
                                        profit_for_year=profit_for_year,
                                        user_list=user_list).apply()


# Функция для третьего захода
async def add_third_step(id_company, plantiff_all_time, plantiff_one_year, plantiff_three_years, defendant_all_time, defendant_one_year, defendant_three_years, enforcement_last_year_total_amount, enforcement_all_time_total_amount, pfr, vat, total_payed, transport_tax, balance, earnings, profit, jetlend, other, gos_contract_member, gos_contract_concluded):
    id_company = await select_id_company(id_company)
    await id_company.update(plantiff_all_time=plantiff_all_time,
                                        plantiff_one_year=plantiff_one_year,
                                        plantiff_three_years=plantiff_three_years,
                                        defendant_all_time=defendant_all_time,
                                        defendant_one_year=defendant_one_year,
                                        defendant_three_years=defendant_three_years,
                                        enforcement_last_year_total_amount=enforcement_last_year_total_amount,
                                        enforcement_all_time_total_amount=enforcement_all_time_total_amount,
                                        pfr=pfr,
                                        vat=vat,
                                        total_payed=total_payed,
                                        transport_tax=transport_tax,
                                        balance=balance,
                                        earnings=earnings,
                                        profit=profit,
                                        jetlend=jetlend,
                                        other=other,
                                        gos_contract_member=gos_contract_member,
                                        gos_contract_concluded=gos_contract_concluded).apply()


# Функция для четвертого захода
async def add_fourth_step(id_company, all_issues, sum_amount):
    id_company = await select_id_company(id_company)
    await id_company.update(all_issues=all_issues, sum_amount=sum_amount).apply()


# Функция для пятого захода
async def add_fifth_step(id_company, events):
    id_company = await select_id_company(id_company)
    await id_company.update(events=events).apply()

########################################################################################################################

# Модель "Вторичного рынкка"

class Secondary_Market(db.Model):
    __tablename__ = 'Secondary_Markets'
    # Первый заход
    id = db.Column(db.Integer(), primary_key=True, doc="Идентификатор")
    company = db.Column(db.String, doc="Название компании")  # Название компании
    rating = db.Column(db.String, doc="Рейтинг компании")  # Рейтинг компании
    amount = db.Column(db.String, doc="Сумма")  # Сумма
    interest_rate = db.Column(db.String, doc="Ставка в %")  # Ставка в %
    term_in_days = db.Column(db.String, doc="Срок в днях")  # Срок в днях
    id_company = db.Column(db.Integer, doc="ID компании на сайте")  # id компании на сайте, откуда берем.

    # Второй заход
    address = db.Column(db.String, doc="Адрес организации")  # Адресс организации
    inn_company = db.Column(db.String, doc="ИНН организации")  # ИНН организации
    ogrn = db.Column(db.String, doc="ОГРН организации")  # ОГРН организации
    primaryCatergory = db.Column(db.String, doc="Категория компании")  # Категория компании
    contr_focus_link = db.Column(db.String, doc="Ссылка на КонтрФокус")  # КонтрФокус Ссылка
    registration_date = db.Column(db.String, doc="Дата регистрации")  # Дата регистрации
    site_link = db.Column(db.String, doc="Ссылка на сайт компании")  # Ссылка на сайт компании
    revenue_for_year = db.Column(db.String, doc="Выручка за год")  # Выручка за год
    profit_for_year = db.Column(db.String, doc="Прибыль за год")  # Прибыль за год
    user_list = db.Column(db.String, doc="Список участников: ФИО, ИНН, Роль в компании")  # Список участников: ФИО, ИНН, Роль в компании

    # Третий заход
    plantiff_all_time = db.Column(db.String, doc="Истец за все время")  # Истец за все время
    plantiff_one_year = db.Column(db.String, doc="Истец за один год")  # Истец за один год
    plantiff_three_years = db.Column(db.String, doc="Истец за три года")  # Истец за три года
    defendant_all_time = db.Column(db.String, doc="Защита за все время")  # Защита за все время
    defendant_one_year = db.Column(db.String, doc="Защита за один год")  # Защита за один год
    defendant_three_years = db.Column(db.String, doc="Защита за три года")  # Защита за три года
    enforcement_last_year_total_amount = db.Column(db.String,
                                                   doc="Исполнительные производства за 1 год")  # Исполнительные производства за 1 год
    enforcement_all_time_total_amount = db.Column(db.String,
                                                  doc="Исполнительные производства за все время")  # Исполнительные производства за все время
    pfr = db.Column(db.String, doc="Взносы ПФР")  # Взносы ПФР
    vat = db.Column(db.String, doc="НДС")  # НДС
    total_payed = db.Column(db.String, doc="Всего уплачено")  # Всего уплачено
    transport_tax = db.Column(db.String, doc="Транспортный налог")  # Транспортный налог
    balance = db.Column(db.String, doc="Баланс")  # Баланс
    earnings = db.Column(db.String, doc="Выручка")  # Выручка
    profit = db.Column(db.String, doc="Чистая прибыль")  # Чистая прибыль
    jetlend = db.Column(db.String, doc="Джет Ленд")  # Джет Ленд
    other = db.Column(db.String, doc="Другие")  # Другие
    gos_contract_member = db.Column(db.String, doc="Гос.Контракт - Участник")  # Гос.Контракт - Участник
    gos_contract_concluded = db.Column(db.String, doc="Гос.Контракт - Заключен")  # Гос.Контракт - Заключен

    # Четвертый заход
    all_issues = db.Column(db.String, doc="Все выпуски: Сумма, ставка, дата")  # Все выпуски: Сумма, ставка, дата
    sum_amount = db.Column(db.String, doc="Сумма займов")  # Сумма займов.

    # Пятый заход
    events = db.Column(db.String, doc="Список событий: Название, дата")  # Список событий: Название, дата

async def secondary_select_id_company(id_company: int):
    id_company = await Secondary_Market.query.where(Secondary_Market.id_company == id_company).gino.first()
    return id_company

async def secondary_get_all_company_ids():
    query = Secondary_Market.query.distinct(Secondary_Market.id_company)
    result = await query.gino.all()
    return [row.id_company for row in result] if result else []

# Функция для первого захода
async def secondary_add_primary_placement(company, rating, amount, interest_rate, term_in_days, id_company):
    await Secondary_Market.create(
        company=company,
        rating=rating,
        amount=amount,
        interest_rate=interest_rate,
        term_in_days=term_in_days,
        id_company=id_company
    )

# Функция для второго захода
async def secondary_add_secondary_placement(id_company, address, inn_company, ogrn, primaryCatergory, contr_focus_link, registration_date, site_link, revenue_for_year, profit_for_year, user_list):
    id_company = await secondary_select_id_company(id_company)
    await id_company.update(address=address,
                                        inn_company=inn_company,
                                        ogrn=ogrn,
                                        primaryCatergory=primaryCatergory,
                                        contr_focus_link=contr_focus_link,
                                        registration_date=registration_date,
                                        site_link=site_link,
                                        revenue_for_year=revenue_for_year,
                                        profit_for_year=profit_for_year,
                                        user_list=user_list).apply()


# Функция для третьего захода
async def secondary_add_third_step(id_company, plantiff_all_time, plantiff_one_year, plantiff_three_years, defendant_all_time, defendant_one_year, defendant_three_years, enforcement_last_year_total_amount, enforcement_all_time_total_amount, pfr, vat, total_payed, transport_tax, balance, earnings, profit, jetlend, other, gos_contract_member, gos_contract_concluded):
    id_company = await secondary_select_id_company(id_company)
    await id_company.update(plantiff_all_time=plantiff_all_time,
                                        plantiff_one_year=plantiff_one_year,
                                        plantiff_three_years=plantiff_three_years,
                                        defendant_all_time=defendant_all_time,
                                        defendant_one_year=defendant_one_year,
                                        defendant_three_years=defendant_three_years,
                                        enforcement_last_year_total_amount=enforcement_last_year_total_amount,
                                        enforcement_all_time_total_amount=enforcement_all_time_total_amount,
                                        pfr=pfr,
                                        vat=vat,
                                        total_payed=total_payed,
                                        transport_tax=transport_tax,
                                        balance=balance,
                                        earnings=earnings,
                                        profit=profit,
                                        jetlend=jetlend,
                                        other=other,
                                        gos_contract_member=gos_contract_member,
                                        gos_contract_concluded=gos_contract_concluded).apply()


# Функция для четвертого захода
async def secondary_add_fourth_step(id_company, all_issues, sum_amount):
    id_company = await secondary_select_id_company(id_company)
    await id_company.update(all_issues=all_issues, sum_amount=sum_amount).apply()


# Функция для пятого захода
async def secondary_add_fifth_step(id_company, events):
    id_company = await secondary_select_id_company(id_company)
    await id_company.update(events=events).apply()
########################################################################################################################




# Асинхронная инициализация базы данных
async def init_db():
    await db.set_bind(DATABASE_URL)

# Асинхронное создание таблиц
async def create_tables():
    await db.gino.create_all()



if __name__ == '__main__':
    async def main():
        loop = asyncio.get_event_loop()
        await init_db()
        await create_tables()

    asyncio.run(main())
