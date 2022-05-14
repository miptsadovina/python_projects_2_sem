import random as rd
import pandas as pd
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

bot = Bot(token="5350156427:AAFNPTw6YiKw7oBfxIa5d5IS7KF_Y5NGJj4")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

type_of_film = 'None'
options = False
film = False
book = False
year_of_book = ''
author = False


movies_table = pd.read_csv('movies.csv')
books_table = pd.read_csv('Books.csv', on_bad_lines='skip')

def get_random_films(num_of_films):
    movies_genre = movies_table[movies_table['genres'] == type_of_film]
    answer = [0] * num_of_films
    for i in range(num_of_films):
        film = movies_genre.index[rd.randint(0, len(movies_genre.index) - 1)]
        while film in answer:
            place = rd.randint(0, len(movies_genre.index) - 1)
        answer[i] = film
    ans = ''
    for i in range(num_of_films):
        ans += (movies_genre['title'][answer[i]] + '\n')
    return ans

def get_random_books(num_of_books):
    if year_of_book == '1950-1980':
        books_year = books_table[(books_table['Year'] >= 1950) & (books_table['Year'] <= 1980)]
    elif year_of_book == '1981-1994':
        books_year = books_table[(books_table['Year'] >= 1981) & (books_table['Year'] <= 1994)]
    elif year_of_book == '1995-1999':
        books_year = books_table[(books_table['Year'] >= 1995) & (books_table['Year'] <= 1999)]
    elif year_of_book == '2000-2005':
        books_year = books_table[(books_table['Year'] >= 2000) & (books_table['Year'] <= 2005)]
    answer = [0] * num_of_books
    for i in range(num_of_books):
        book = books_year.index[rd.randint(0, len(books_year.index) - 1)]
        while book in answer:
            place = rd.randint(0, len(books_year.index) - 1)
        answer[i] = book
    ans = ''
    for i in range(num_of_books):
        ans += (books_year['Title'][answer[i]] + '\n')
    return ans

@dp.message_handler(commands="start")
async def start(message: types.Message):
    global type_of_film
    global options
    global year_of_book
    global film
    global book
    global author
    author = False
    film = False
    book = False
    type_of_film = ''
    year_of_book = ''
    options = False
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = ['film', 'book']
    keyboard.add(*button)
    await message.answer("Choose book or film", reply_markup=keyboard)


@dp.message_handler(Text(equals='film'))
async def choose_genre_of_film(message):
    global film
    film = True
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = ['Adventure', 'Comedy', 'Drama']
    button2 = ['Romance', 'Action', 'Thriller']
    button3 = ['Children', 'Documentary', 'Fantasy']
    keyboard.add(*button1)
    keyboard.add(*button2)
    keyboard.add(*button3)
    await message.answer("Сhoose a genre", reply_markup=keyboard)

@dp.message_handler(Text(equals='book'))
async def choose_year_or_author(message):
    global book
    book = True
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = ['Year', 'Author']
    keyboard.add(*button1)
    await message.answer("Do you want to choose a year or an author", reply_markup=keyboard)

@dp.message_handler(Text(equals='Year'))
async def choose_year_of_book(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = ['1950-1980', '1981-1994']
    button2 = ['1995-1999', '2000-2005']
    keyboard.add(*button1)
    keyboard.add(*button2)
    await message.answer("Сhoose a year", reply_markup=keyboard)

@dp.message_handler(Text(equals='Author'))
async def enter_the_author(message):
    global author
    author = True
    await message.answer("Enter the author")

@dp.message_handler()
async def make_random(message):
    global type_of_film
    global options
    global year_of_book
    global film
    global book
    global author
    if author:
        Author = message.text
        books_author = books_table[books_table['Author'] == Author]
        if len(books_author.index):
            index = books_author.index[rd.randint(0, len(books_author.index) - 1)]
            await message.answer(books_author['Title'][index])
        else:
            await message.answer("Sorry, but I didn't found this Author")
        await message.answer('If you want to choose other film or book enter /start')
    elif options == False:
        options = True
        if film:
            type_of_film = message.text
        elif book:
            year_of_book = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["1", "5", "10"]
        keyboard.add(*buttons)
        await message.answer("Choose how many options you want to get\n", reply_markup=keyboard)
    elif options:
        if film:
            num_of_films = int(message.text)
            ans = get_random_films(num_of_films)
            await message.answer(ans)
        elif book:
            num_of_books = int(message.text)
            ans = get_random_books(num_of_books)
            await message.answer(ans)
        await message.answer('If you want to choose other film or book enter /start')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)