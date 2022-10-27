# Екатеринбургэнергосбыт интеграция Home Assistant

Не официальный плагин для интеграции с "Екатеринбургэнергосбыт" (https://www.eens.ru/). 
Забирает данные по счетчикам и задолженности с сайта и отображает их в виде сенсора, может передавать показания. Не используется Личный кабинет, нужен только номер счета. Работает по аналогии подачи показаний с главной страницы сайта (https://www.eens.ru/pokazania).

> # Внимание!
> После отправки показаний данные обновляются не сразу! Это особенность системы учета "Екатеринбургэнергосбыт", данные обновляются в течении нескольких часов (иногда быстрее).

В поле `Дата отправки` будет стоять дата и время  последней успешной отправки данных (не сохраняется при перезепусках Home Assistant). Данные можно отправить и получить в любой момент по нажатию соответсвующих кнопок в интерфейсе.


## Установка Home Assistant Core

1. Скопируйте папку `custom_components/ekenergosbyt` в папку конфигурации Home Assistant `custom_components/ekenergosbyt` (если папка `custom_components` не существует, создайте её)
1. Перезпустите Home Assistant
1. В разделе `Настройки` -> `Устройства и службы` -> `Интегации` нажмите нопку `Добавить интеграцию`
1. В списке найдете `EkaterinburgEnergoSbyt`


## Карточка Lovelaсe ##

<img src="https://raw.githubusercontent.com/archekb/ha-ekenergosbyt/master/images/card.png" alt="Карточка Lovelaсe">


```
type: entities
entities:
  - entity: sensor.ekenergosbyt_{номер вашего счета}_zadolzhenost
    name: Задолженость
  - entity: sensor.ekenergosbyt_{номер вашего счета}_den
    name: День
  - entity: sensor.ekenergosbyt_{номер вашего счета}_noch
    name: Ночь
  - entity: sensor.ekenergosbyt_{номер вашего счета}_predstavitel
    name: Представитель
  - entity: sensor.ekenergosbyt_{номер вашего счета}_telefon
    name: Телефон
  - entity: sensor.ekenergosbyt_{номер вашего счета}_data_obnovleniia
    name: Дата обновления
  - entity: button.ekenergosbyt_{номер вашего счета}_obnovit_dannye
    name: Обновить данные
  - entity: number.ekenergosbyt_{номер вашего счета}_den
    name: День
  - entity: number.ekenergosbyt_{номер вашего счета}_noch
    name: Ночь
  - entity: sensor.ekenergosbyt_{номер вашего счета}_data_otpravki
    name: Дата отправки
  - entity: button.ekenergosbyt_{номер вашего счета}_otpravit_pokazaniia
    name: Отправить показания
title: Екатеринбургэнерго
```

Для автоматической отправки показаний просто создайте автоматизацию которая будет запускаться определенного числа и нажимать кнопку `Отправить показания`.