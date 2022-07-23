# Kadastr

Индексирование Актов определения стоимости по статье 16 Федерального закона от 03.06.2016 г. №237-ФЗ "О государственной кадастровой оценке"

Для получения соответствия кадастрового номера названию файла необходимо выполнить команду

cat kadastr.csv | grep "00:00:0000000:0"

где 00:00:0000000:0 кадастровый  номер участка

Перед выполением этих действий необходимо выполнить команду:

./kadastr.py

предварительно установив разрешение на исполнение кода командой
chmod 0555 kadastr.py