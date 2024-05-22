from bot.bot import dp, bot
import database.orm as orm


# Запуск бота
if __name__ == '__main__':
    orm.create_tables()
    orm.insert_test_data()
    dp.run_polling(bot)
