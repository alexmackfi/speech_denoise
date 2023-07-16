Веб-сервис для удаления шума из записанной речи. Позволяет записать аудио, скачать его и отредактировать.
Чтобы запустить сервер выполните следующие команды:
1) git clone https://github.com/alexmackfi/speech_denoise.git
2) cd speech_denoise
3) source venv/Scripts/activate
4) pip install -r requirements.txt 
5) python wsgi.py
<b>
Также запустить сервис можно при помощи технологии Docker:</b><br><br>
Склонируйте репозиторий на свой ПК следующей командой: <br>
<code> git clone https://github.com/alexmackfi/speech_denoise.git </code> <br>
Перейдите в папку с проектом:<br>
<code> cd speech_denoise </code><br>
Выполните следующую последовательность команд: <br>
<code> docker build -t tort . </code><br>
<code> docker run -d -p 8000:8000 tort </code> <br>
Перейдите по ссылке http://localhost:8000 <br>
Если у вас операционная система Windows, то необходимо изменить содержание Dockerfile, раскомментировать строки содержащие в себе значение <b>5000</b> и закомментировать строки содержащие <b>8000</b>:<br>
Тогда команды изменятся соответственно:<br>
<code> docker run -d -p 5000:5000 tort </code> <br>
Перейдите по ссылке http://localhost:5000 <br><br>

Обучение моделей, описание проведенных экспериментов и презентация проекта находятся в папке trainig <br>
   
