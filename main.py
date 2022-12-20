from aiogram import Bot, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import executor

import sqlalchemy as db

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, update

from sqlalchemy.orm import sessionmaker

from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token='5417443700:AAEcYj6ag1VUGiXeq2ZrK9h_w2Brx_5lwiA')
dp = Dispatcher(bot, storage=MemoryStorage())

engine = db.create_engine('sqlite+pysqlite:///dungeons.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine, future=True, expire_on_commit=False)
session = Session()


# Создание персонажа со всеми итемами и возможность получить статистику, надеть-снять броню etc - 2 балла
# Взаимодействие с городом - 2 балл (магазин-покупка-продажа, восстановление)


class Persons(Base):
    __tablename__ = 'persons'

    UserID = Column(Integer, name='UserId', primary_key=True)
    Nickname = Column(String)
    Level = Column(Integer)
    HP = Column(Integer)
    CurHP = Column(Integer)
    Money = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    XP = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    LocationID = Column(String)
    TgID = Column(String)


class Items(Base):
    __tablename__ = 'items'

    ItemID = Column(Integer, name='ItemID', primary_key=True)
    Name = Column(String)
    Cost = Column(Integer)
    CostToSale = Column(Integer)
    ItemType = Column(String)
    HP = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    ReqLevel = Column(Integer)

    def __init__(self, ItemId, Name, Cost, CostToSale, ItemType, HP, Attack, MagicAttack, Armour, MagicArmour,
                 ReqLevel):
        self.ItemID = ItemId
        self.Name = Name
        self.Cost = Cost
        self.CostToSale = CostToSale
        self.ItemType = ItemType
        self.HP = HP
        self.Attack = Attack
        self.MagicAttack = MagicAttack
        self.Armour = Armour
        self.MagicArmour = MagicArmour
        self.ReqLevel = ReqLevel

    def __repr__(self):
        return f"{self.Name}: {self.Cost} деняк, {self.CostToSale} деняк на продаже\n{self.HP} к здоровью, {self.Attack} к аттаке, {self.MagicAttack} к магической аттаке, {self.Armour} к броне, {self.MagicArmour} к магической броне\nДля покупки нужен {self.ReqLevel} уровень"


class ItemsByPerson(Base):
    __tablename__ = 'items_by_person'

    UserID = Column(Integer, name='UserId', primary_key=True)
    ItemID = Column(Integer, name='ItemID')
    Quantity = Column(Integer)
    NowWearing = Column(Integer)

    def __repr__(self):
        text_about_wearing = ""
        if self.NowWearing == 1:
            text_about_wearing = ", надето"

        return f'{self.ItemID}: {self.Quantity} штук' + text_about_wearing


Base.metadata.create_all(engine)


# i1 = Items(1, 'нож', 100, 70, 'weapons', 3, 5, 5, 1, 2, 1)
# i2 = Items(2, 'меч', 200, 100, 'weapons', 3, 5, 5, 1, 2, 1)
# i3 = Items(3, 'ружье', 300, 150, 'weapons', 3, 5, 5, 1, 2, 5)
#
# i4 = Items(4, 'деревянная броня', 100, 70, 'armor', 3, 5, 5, 1, 2, 1)
# i5 = Items(5, 'стальная броня', 200, 180, 'armor', 3, 5, 5, 1, 2, 1)
# i6 = Items(6, 'изумрудная броня', 300, 155, 'armor', 3, 5, 5, 1, 2, 3)
#
# i7 = Items(7, 'деревянный шлем', 100, 70, 'helmet', 3, 5, 5, 1, 2, 1)
# i8 = Items(8, 'стальной шлем', 200, 130, 'helmet', 3, 5, 5, 1, 2, 1)
# i9 = Items(9, 'изумрудный шлем', 300, 55, 'helmet', 3, 5, 5, 1, 2, 2)
#
# i10 = Items(10, 'обычные ботинки', 100, 80, 'boots', 3, 5, 5, 1, 2, 1)
# i11 = Items(11, 'крутые ботинки', 200, 150, 'boots', 3, 5, 5, 1, 2, 1)
# i12 = Items(12, 'уникальные ботинки', 300, 200, 'boots', 3, 5, 5, 1, 2, 2)
#
# i13 = Items(13, 'обычные наручи', 100, 70, 'bracers', 3, 5, 5, 1, 2, 1)
# i14 = Items(14, 'крутые наручи', 200, 140, 'bracers', 3, 5, 5, 1, 2, 1)
# i15 = Items(15, 'уникальные наручи', 300, 180, 'bracers', 3, 5, 5, 1, 2, 3)
#
# i16 = Items(16, 'зелье здоровья', 100, 70, 'potion', 3, 5, 5, 1, 2, 1)  # тут переделать значения
# i17 = Items(17, 'зелье аттаки', 200, 150, 'potion', 3, 5, 5, 1, 2, 1)
# i18 = Items(18, 'зелье брони', 300, 250, 'potion', 3, 5, 5, 1, 2, 4)
#
# session.add(i1)
# session.add(i2)
# session.add(i3)
# session.add(i4)
# session.add(i5)
# session.add(i6)
# session.add(i7)
# session.add(i8)
# session.add(i9)
# session.add(i10)
# session.add(i11)
# session.add(i12)
# session.add(i13)
# session.add(i14)
# session.add(i15)
# session.add(i16)
# session.add(i17)
# session.add(i18)
#
# session.commit()

# Класс для персонажа
class Person(StatesGroup):
    UserId = State()
    Nickname = State()
    # Level = State()   default
    HP = State()
    # CurHP = State()   default
    # Money = State()   default
    Attack = State()
    MagicAttack = State()
    # XP = State()    default
    Armour = State()
    MagicArmour = State()
    TgID = State()
    # LocationID = State()   default


@dp.message_handler(commands=['start'], state="*")
async def start(message):
    await Person.UserId.set()
    create = KeyboardButton("Создать персонажа")
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(create)
    await message.answer("Привет! Это клевая игра про подземелья. Давай для начала создадим твоего персонажа",
                         reply_markup=buttons)


# Заполнение айди
@dp.message_handler(state=Person.UserId)
async def make_person(message, state):
    await message.answer("Введи никнейм")
    await Person.next()


# Заполнение никнейма
@dp.message_handler(state=Person.Nickname)
async def fill_nickname(message, state):
    async with state.proxy() as data:
        data['Nickname'] = message.text
    await message.answer('Отлично! Теперь выбери HP - здоровье персонажа. Выбирай число от 20 до 50')
    await Person.next()


# Заполнение здоровья
@dp.message_handler(state=Person.HP)
async def fill_hp(message, state):
    async with state.proxy() as data:
        data['HP'] = message.text
    await message.answer('Отлично! Теперь выбери уровень аттаки персонажа. Выбирай число от 20 до 50')
    await Person.next()


# Заполнение аттаки
@dp.message_handler(state=Person.Attack)
async def fill_attack(message, state):
    async with state.proxy() as data:
        data['Attack'] = message.text
    await message.answer('Отлично! Теперь выбери уровень магической аттаки. Выбирай число от 20 до 50')
    await Person.next()


# Заполнение магической аттаки
@dp.message_handler(state=Person.MagicAttack)
async def fill_magic_attack(message, state):
    async with state.proxy() as data:
        data['MagicAttack'] = message.text
    await message.answer('Отлично! Какое будет значение базовой брони персонажа? Выбири число от 20 до 50')
    await Person.next()


# Заполнение базовой брони персонажа
@dp.message_handler(state=Person.Armour)
async def fill_armour(message, state):
    async with state.proxy() as data:
        data['Armour'] = message.text
    await message.answer('Отлично! Какое будет значение магической брони персонажа? Выбири число от 20 до 50')
    await Person.next()


# Заполнение базовой магической брони персонажа
@dp.message_handler(state=Person.MagicArmour)
async def fill_magic_armour(message, state):
    async with state.proxy() as data:
        data['MagicArmour'] = message.text
        data['TgID'] = message.from_user.id

        new_track = Persons(Nickname=data['Nickname'],
                            Level=1,
                            HP=data['HP'],
                            CurHP=100,
                            Money=500,
                            Attack=data['Attack'],
                            MagicAttack=data['MagicAttack'],
                            XP=0,
                            Armour=data['Armour'],
                            MagicArmour=data['MagicArmour'],
                            LocationID="City",
                            TgID=data['TgID'])

        session.add(new_track)
        session.commit()

    await message.answer('Отлично! Мы закончили заполнять персонажа')
    await state.finish()


@dp.message_handler(commands=['get_statistics'], state='*')
async def get_statistics(message):
    results = session.query(Persons).all()
    await message.answer(
        f'Вот твой персонаж:\nНик: {results[0].Nickname}\nУровень: {results[0].Level}\nЗдоровье: {results[0].HP}\nТекущее здоровье: {results[0].CurHP}\nДеньги: {results[0].Money}\nАттака: {results[0].Attack}\nМагическая аттака: {results[0].MagicAttack}\nОпыт: {results[0].XP}\nБроня: {results[0].Armour}\nМагическая броня: {results[0].MagicArmour}\nЛокация: {results[0].LocationID}')


@dp.message_handler(commands=['go_city'], state='*')
async def go_city(message):
    await message.answer('Ты в городе!')

    user = session.execute(
        select(Persons).where(Persons.TgID == str(message.from_user.id))
    )

    user = user.first()['Persons']
    user.CurHP = user.HP
    session.commit()


@dp.message_handler(commands=['my_inventory'], state='*')
async def go_shop(message):
    results = session.execute(f'select ItemID from items_by_person where UserID = {message.chat.id} and NowWearing = 1').fetchall()

    weapons_exist = False
    armor_exist = False
    helmet_exist = False
    boots_exist = False
    bracers_exist = False

    for item in results:
        session.execute(f'select ItemType from items where ItemID = {item[0]}')
        if session.fetchall()[0][0] == 'weapons':
            weapons_exist = True
        if session.fetchall()[0][0] == 'armor':
            armor_exist = True
        if session.fetchall()[0][0] == 'helmet':
            helmet_exist = True
        if session.fetchall()[0][0] == 'boots':
            boots_exist = True
        if session.fetchall()[0][0] == 'bracers':
            bracers_exist = True

    if weapons_exist:
        weapons = KeyboardButton("Снять оружие")
    else:
        weapons = KeyboardButton("Надеть оружие")

    if armor_exist:
        armor = KeyboardButton("Снять броню")
    else:
        armor = KeyboardButton("Надеть броню")

    if helmet_exist:
        helmet = KeyboardButton("Снять шлем")
    else:
        helmet = KeyboardButton("Надеть шлем")

    if boots_exist:
        boots = KeyboardButton("Снять ботинки")
    else:
        boots = KeyboardButton("Надеть ботинки")

    if bracers_exist:
        bracers = KeyboardButton("Снять наручи")
    else:
        bracers = KeyboardButton("Надеть наручи")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(weapons, armor, helmet, boots, bracers)

    results = session.query(ItemsByPerson).where(ItemsByPerson.UserID == str(message.from_user.id))
    in_inventory = ''
    for r in results:
        in_inventory += str(r)
        in_inventory += '\n'

    await message.answer('Вот твой инвентарь: \n\n' + in_inventory, reply_markup=buttons)


@dp.message_handler(commands=['go_shop'], state='*')
async def go_shop(message):
    get_items = KeyboardButton("Посмотреть товары")
    buy_items = KeyboardButton("Купить товары")
    sell_items = KeyboardButton("Продать товары")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(get_items, buy_items, sell_items)

    await message.answer('Ты в магазине! Что хочешь сделать здесь?', reply_markup=buttons)


@dp.message_handler(lambda message: message.text == "Посмотреть товары", state="*")
async def get_items(message):
    results = session.query(Items).all()
    text = ''
    for r in results:
        text += str(r)
        text += '\n\n'
    await message.answer(text)


class Actions(StatesGroup):
    Sell = State()
    Buy = State()


@dp.message_handler(lambda message: message.text == "Продать товары", state="*")
async def get_items(message):
    await Actions.Sell.set()
    await message.answer("Введи уникальный номер товара, который хочешь продать. Чтобы узнать его, загляни в инвентарь")


UserID = Column(Integer, name='UserId', primary_key=True)
ItemID = Column(Integer, name='ItemID')
Quantity = Column(Integer)
NowWearing = Column(Integer)


@dp.message_handler(state=Actions.Sell)
async def sell(message, state):
    sell_item_id = str(message.text)

    items = session.query(ItemsByPerson).filter_by(ItemID=sell_item_id).filter_by(UserID=message.from_user.id).first()

    new_track = ItemsByPerson(UserID=str(message.from_user.id),
                              ItemID=sell_item_id,
                              Quantity=items.quantity - 1,
                              NowWearing=0)

    session.add(new_track)
    session.commit()

    item = session.execute(
        select(Items).where(Items.ItemID == sell_item_id)
    )
    item = item.first()['Items']
    money = item.CostToSale

    user = session.execute(
        select(Persons).where(Persons.UserID == str(message.from_user.id))
    )
    user = user.first()['Persons']
    user.Money += money
    session.commit()


@dp.message_handler(lambda message: message.text == "Купить товары", state="*")
async def get_items(message):
    await Actions.Buy.set()
    await message.answer("Введи уникальный номер товара, который хочешь купить. Чтобы узнать его, загляни в магазин")


@dp.message_handler(state=Actions.Buy)
async def buy(message, state):
    buy_item_id = message.text
    user_id = message.from_user.id

    items = session.query(ItemsByPerson).filter_by(ItemID=buy_item_id).filter_by(UserID=message.from_user.id).first()

    if items is None:
        new_track = ItemsByPerson(UserID=message.from_user.id,
                                  ItemID=int(buy_item_id),
                                  Quantity=1,
                                  NowWearing=0)
        session.add(new_track)
        session.commit()
    else:
        new_track = ItemsByPerson(UserID=message.from_user.id,
                                  ItemID=int(buy_item_id),
                                  Quantity=items.Quantity + 1,
                                  NowWearing=0)

        session.add(new_track)
        session.commit()

    items = session.query(Items).filter_by(ItemID=buy_item_id).first()
    money = items[0].Cost

    user = session.execute(
        select(Persons).where(Persons.UserID == str(message.from_user.id))
    )
    user = user.first()['Persons']
    user.Money -= money
    session.commit()


if __name__ == "__main__":
    executor.start_polling(dp)
