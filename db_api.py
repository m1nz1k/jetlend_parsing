# Импорты
from gino import Gino
import asyncio

# Создание объекта Gino
db = Gino()

# Настройки подключения к PostgreSQL
DATABASE_URL = 'postgresql://postgres:eugen123@localhost/jetlend'

# Определение моделей данных
class Primary_Placement_Market(db.Model):
    __tablename__ = 'Primary_Placement_Markets'
    # Первый заход
    id = db.Column(db.Integer(), primary_key=True)
    company = db.Column(db.String) # Название компании
    amount = db.Column(db.String) # Сумма
    interest_rate = db.Column(db.String) # Ставка в %
    term_in_days = db.Column(db.String) # Срок в днях
    id_company = db.Column(db.Integer) # id компании на сайте, откуда берем.
    # Второй заход
    address = db.Column(db.String) # Адресс организации
    inn_company = db.Column(db.String) # ИНН организации
    ogrn = db.Column(db.String) # ОГРН организации
    primaryCatergory = db.Column(db.String) # Категория компании
    contr_focus_link = db.Column(db.String) # КонтрФокус Ссылка
    registration_date = db.Column(db.String) # Дата регистрации
    site_link = db.Column(db.String) # Ссылка на сайт компании
    revenue_for_year = db.Column(db.String) # Выручка за год
    profit_for_year = db.Column(db.String) # Прибыль за год
    user_list = db.Column(db.String) # Список участников: ФИО, ИНН, Роль в компании
    # Третих заход
    plantiff_all_time = db.Column(db.String) # Истец за все время
    plantiff_one_year = db.Column(db.String) # Истец за один год
    plantiff_three_years = db.Column(db.String) # Истец за три года
    defendant_all_time = db.Column(db.String) # Защита за все время
    defendant_one_year = db.Column(db.String) # Защита за один год
    defendant_three_years = db.Column(db.String) # Защита за три года
    enforcement_last_year_total_amount = db.Column(db.String) # Исполнительные производства за 1 год
    enforcement_all_time_total_amount = db.Column(db.String) # Исполнительные производства за все время
    pfr = db.Column(db.String) # Взносы ПФР
    vat = db.Column(db.String) # НДС
    total_payed = db.Column(db.String) # Всего уплачено
    transport_tax = db.Column(db.String) # Транспортный налог
    balance = db.Column(db.String) # Баланс
    earnings = db.Column(db.String) # Выручка
    profit = db.Column(db.String) # Чистая прибыль
    jetlend = db.Column(db.String) # Джет Ленд
    other = db.Column(db.String) # Другие
    gos_contract_member = db.Column(db.String) # Гос.Контракт - Участник
    gos_contract_concluded = db.Column(db.String) # Гос.Контакт - Заключен
    # Четвертый заход
    all_issues = db.Column(db.String) # Все выпуски: Сумма, ставка, дата
    # Пятый заход
    events = db.Column(db.String) # Список событий: Название, дата


async def select_id_company(id_company: int):
    id_company = await Primary_Placement_Market.query.where(Primary_Placement_Market.id_company == id_company).gino.first()
    return id_company
# Функции для добавления
# Функция для первого захода
async def add_primary_placement(company, amount, interest_rate, term_in_days, id_company):
    await Primary_Placement_Market.create(
        company=company,
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
async def add_fourth_step(id_company, all_issues):
    id_company = await select_id_company(id_company)
    await id_company.update(all_issues=all_issues).apply()


# Функция для пятого захода
async def add_fifth_step(id_company, events):
    id_company = await select_id_company(id_company)
    await id_company.update(events=events).apply()





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
