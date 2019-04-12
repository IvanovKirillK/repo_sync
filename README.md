# repo_sync
## Описание
Скрипт для синхронизации репозиториев - нужен в случаях когда код в некоторые ветки в битбакете попадает через pull-request и должен попасть в gitlab для CI\CD/

Конфиг хранится в config .json

Во время работы скрипт обращается к API Bitbucket для получения последнего commit id по интересующему его проекту, делает тоже самое с гитлабом, если коммиты отличаются - используя гит делает gut pull, переходит на ветку которую надо синхронизировать, и делает git push (надо делать правильные настройки git - смотри ниже).

По завершению задачи пишет в InfluxDB.


## Подготовка к использованию:

1. Создаем проект в гитлабе.
1. Добавляем пользователя repo_sync/Password12! в проект
1. Клонируем репозиторий за которым надо следить на машине где установлен скрипт - git clone
1. Добавляем push url с указанием репозитория в который надо синхронизировать код - git remote set-url origin --push --add <slave repo>
1. Добавляем имя пользователя и пароль для доступа в гитлаб  - git config -e, правим строку в котрой указан адрес гитлаба 
1. Проверяем что все выглядит примерно вот так git remote -v
    
        git remote -v
        origin  <link1> (fetch)
        origin  <link2> (push)
    
1. Настраиваем крон

## Описание конфигурации

    {
      "log": { #секция настроек логирования
        "path": "./", #путь до лог файла
        "filename": "repo_sync.log", #имя логфайла
        "size_bytes": 10000, #размер лог файла
        "file_count" : 10 #кол-во лог файлов
      },
      "monitoring": { #секция натсроек мониторинга
        "enabled": "true", #включен мониторинг или нет
        "dbname": "", #имя базы в InfluxDB
        "dbhost": "", #адрес хоста где развернут InfluxDB
        "dbport": "", #порт базы данных InfluxDB
        "dbuser": "", #имя пользвоателя InfluxDB
        "dbpass": "", #пароль InfluxDB
        "measurement": "", #имя измерения в InfluxDB - лучше использовать sync
        "repo_name": "" #тег измерения в InfluxDB - нужну указывать проект\ветку
      },
      "master": { #секция описывает за какой веткой следить
        "vcs": "bitbucket", # тип vcs - доступны bitbucket и gitlab
        "path": "../name", #путь к диреткори в которую будет делать ся git clone
        "branch": "develop", # имя ветки за которой надо следить
        "repo": "", #ссылка для git clone 
        "url": "", # ссылка для подступа к API
        "params": {
          "until": "develop", #имя ветки за которой надо следить
          "limit": 0, #остается неизменным
          "start": 0 #остается неизменным
        },
        "auth": { # аутентификация
          "type": "basic", #тип аутентификации - пока поддерживается basic и token
          "login": "", #имя пользвоателя для API
          "password": "" #парольт для API
        }
      },
      "slave": { #секция описывает в какой репозиторий сливать 
        "vcs": "gitlab",  # тип vcs - доступны bitbucket и gitlab
        "repo": "", #ссылка для git push
        "url": "", # ссылка для подступа к API
        "params": {
          "name": "develop" # имя ветки в которую надо сливать
        },
        "auth": { # аутентификация
          "type": "token"  #тип аутентификации - пока поддерживается basic и token
        },
        "headers": {
          "PRIVATE-TOKEN": "" #токен для доступа к API
        }
      }
    }
