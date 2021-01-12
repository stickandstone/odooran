package main

import (
    "log"
    "os"
    "io/ioutil"
    "github.com/go-telegram-bot-api/telegram-bot-api"
)

var numericKeyboard = tgbotapi.NewReplyKeyboard(
    tgbotapi.NewKeyboardButtonRow(
        tgbotapi.NewKeyboardButton("1"),
        tgbotapi.NewKeyboardButton("2"),
        tgbotapi.NewKeyboardButton("3"),
    ),
    tgbotapi.NewKeyboardButtonRow(
        tgbotapi.NewKeyboardButton("4"),
        tgbotapi.NewKeyboardButton("5"),
        tgbotapi.NewKeyboardButton("6"),
    ),
)

func main() {
    file, err := ioutil.ReadFile("secret.txt")
    if err != nil {
        log.Panic(err)
    }

    secret := string(file)
    log.Printf(secret)

    bot, err := tgbotapi.NewBotAPI(os.Getenv(secret))
    if err != nil {
        log.Panic(err)
    }

    bot.Debug = true

    log.Printf("Authorized on account %s", bot.Self.UserName)

    u := tgbotapi.NewUpdate(0)
    u.Timeout = 60

    updates, err := bot.GetUpdatesChan(u)
    if err != nil {
        log.Panic(err)
    }

    for update := range updates {
        if update.Message == nil { // ignore non-Message updates
            continue
        }

        msg := tgbotapi.NewMessage(update.Message.Chat.ID, update.Message.Text)

        switch update.Message.Text {
        case "open":
            msg.ReplyMarkup = numericKeyboard
        case "close":
            msg.ReplyMarkup = tgbotapi.NewRemoveKeyboard(true)
        }

        if _, err := bot.Send(msg); err != nil {
            log.Panic(err)
        }
    }
}