type: Python api.
framework: Fast API.
database: sqlite.

1) Восстановить виртуальное окружение из файла requiroments.txt
2) Установить сервер MinIO (Я использовал для windows, но думаю сильно не должно отличаться)
   Сылка на руководство: https://docs.min.io/docs/minio-client-quickstart-guide
3) Запустить сервер MinIO.
    (На windows: cd d:/dir_project/.
                 minio.exe server "D:/dir_project/minio_photos".
    )
4) Запустить отладочный сервер uvicorn. Он должен установиться из requiroments.txt.
    (На виндовс: cd d:/dir_project/. (Там где находится manage.py файл).
                 uvicorn manage:app -- reload.
    )
5) Открыть в браузере адрес: "http://localhost:8000/docs"
6) Насладиться увиденным ().

PS. Если MinIo будет ругаться или не работать, то скорее всего требуется создать новые access_key и secret_key.
    Для этого требуется перейти по адресу, который MinIO предоставит и войти под именем "minioadmin" и паролем "minioadmin"
    и создать access_key и secret_key и внести изменения в main/settings.py file
    

Тесты реализовать не успел; Извините)


03.07  02:04:
   реализованы тесты для authentication/models.py и authentication/schemas.py

03.07 20:00
   реализованы тесты (+-) для authentication/backends.py
