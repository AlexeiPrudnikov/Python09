from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import ComplexMath
calcData = [[0, 0], [0, 0]]
file = open('token', 'r', encoding='utf-8')
token = file.readline()
file.close()
bot = Bot(token)
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
def info(update, context):
    infoText = f'/icnum - ввод комплексного числа \n'
    infoText += f'Например: /icnum 1 2 -> это введено число 1 + 2j\n\n'
    infoText += f'/saved - показывает сохраненные числа\n\n'
    infoText += f'/calc  - производит вычисление (при неправильном вводе производится сложение\n'
    infoText += f'Например: /calc * -> перемножает числа'
    context.bot.send_message(update.effective_chat.id, infoText)

def icnum(update, context):
    arg = context.args
    if len(arg) >= 2:
        cnumber = [int(arg[0]), int(arg[1])]
    elif len(arg) == 1:
        cnumber = [int(arg[0]), int(arg[1])]
    else:
        cnumber = [0, 0]
    if len(calcData) >= 2:
        del calcData[0]
    calcData.append(cnumber)
    context.bot.send_message(update.effective_chat.id, f'Число {complex(cnumber[0],cnumber[1])} добавлено в условие')
def calc(update, context):
    arg = context.args
    operation = '+'
    if len(arg) >= 1:
        if arg[0] in ('+', '-', '*', '/'):
            operation = arg[0]
    if operation == '+':
        result = ComplexMath.CSumm(complex(calcData[0][0],calcData[0][1]), complex(calcData[1][0],calcData[1][1]))
    elif operation == '-':
        result = ComplexMath.CSub(complex(calcData[0][0],calcData[0][1]), complex(calcData[1][0],calcData[1][1]))
    elif operation == '/':
        result = ComplexMath.CDiv(complex(calcData[0][0],calcData[0][1]), complex(calcData[1][0],calcData[1][1]))
    elif operation == '*':
        result = ComplexMath.CMult(complex(calcData[0][0],calcData[0][1]), complex(calcData[1][0],calcData[1][1]))

    context.bot.send_message(update.effective_chat.id, f'Результат опрерации {operation} => {result}')


def message(update, context):
    text = update.message.text
    if text.lower() == 'привет':
        context.bot.send_message(update.effective_chat.id, 'И тебе привет..')
    else:
        context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')
def savedData(update, context):
    answer = f'Первое число: {complex(calcData[0][0], calcData[0][1])} \n'
    answer += f'Второе число: {complex(calcData[1][0], calcData[1][1])} \n'
    context.bot.send_message(update.effective_chat.id, answer)

def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, 'Ты несешь какую-то дичь...')


info_handler = CommandHandler('info', info)
input_handler = CommandHandler('icnum', icnum)
savedData_handler = CommandHandler('saved', savedData)
calc_handler = CommandHandler('calc', calc)
message_handler = MessageHandler(Filters.text, message)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(info_handler)
dispatcher.add_handler(input_handler)
dispatcher.add_handler(savedData_handler)
dispatcher.add_handler(calc_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(message_handler)


updater.start_polling()
updater.idle()

