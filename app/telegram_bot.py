import telegram

telegram_token = '5163512485:AAHTeG3o9xGSbHFvKGAYoE36UmBvvmZTJYE'
chat_id = 1554809170
bot = telegram.Bot(token=telegram_token)
# updates = bot.getUpdates()

def sendMessage(items):
    print("sendmessage : {}".format(items))
    bot.sendMessage(chat_id=chat_id, text="새로운 상품")
    
    for img_url in items:
        bot.sendPhoto(chat_id=chat_id, photo=img_url, caption="텍스트")
    
    
    
    # photo_list = []
    # # 이미지 여러장 묶어서 보내기
    # for i in range(len(images)):
    #     photo_list.append(telegram.InputMediaPhoto(open(i, "rb")))
    # bot.sendMediaGroup(chat_id=id, media=photo_list)
    


# if __name__ == '__main__':
#     sendMessage(new_items)
    