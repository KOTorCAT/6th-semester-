# Сайт на Hugo с автоматической публикацией через SourceCraft

Готовый сайт можно посмотреть здесь:
[https://tempesttttt.sourcecraft.site/lr1-misha/](https://tempesttttt.sourcecraft.site/lr1-misha/)

## О чём этот проект

Этот сайт сделан с помощью генератора статических сайтов Hugo.
Исходники хранятся в репозитории SourceCraft.
При каждом изменении кода сайт автоматически пересобирается и публикуется.

## Как это работает 

1. **Проверка оформления текстов.** Специальная программа смотрит все файлы с расширением `.md` и проверяет, что они написаны по правилам Markdown.
2. **Проверка ссылок.** Другая программа проходит по всем ссылкам внутри текстов и смотрит, не ведут ли они на несуществующие страницы.
3. **Сборка и публикация.** Если проверки прошли успешно, сервер скачивает Hugo, собирает из текстов готовые HTML-страницы и загружает их в ветку `release`. Платформа SourceCraft автоматически публикует эту ветку в интернет.


## Код 


```yaml

on:
  push:
    workflows: [build-site]
    filter:
      branches: main

# Здесь описано, что именно делать при пуше
workflows:
  build-site:
    env:
      VERSION: 0.157.0  # Какую версию Hugo будем использовать

    tasks:

      # Задача 1: проверить, правильно ли оформлены Markdown-файлы
      - name: markdown-lint
        cubes:
          - name: run-markdownlint
            script:
              - npm install -g markdownlint-cli  # Скачиваем программу для проверки
              - markdownlint "content/**/*.md" --ignore node_modules  # Запускаем проверку всех md-файлов в папке content

      # Задача 2: проверить, нет ли битых ссылок в текстах
      - name: link-check
        needs: [markdown-lint]  # Сначала должна отработать первая задача, потом эта
        cubes:
          - name: run-link-check
            script:
              - npm install -g markdown-link-check  # Скачиваем программу для проверки ссылок
              - find content -name "*.md" -exec npx markdown-link-check {} --quiet \;  # Ищем все md-файлы и проверяем ссылки внутри них

      # Задача 3: собрать сайт и выложить его в интернет
      - name: build-and-deploy
        needs: [link-check]  # Ждём, пока проверка ссылок закончится

        cubes:

          # Скачиваем Hugo — программу, которая собирает сайт
          - name: get-hugo
            script:
              - curl -LJO https://github.com/gohugoio/hugo/releases/download/v${VERSION}/hugo_extended_${VERSION}_linux-amd64.deb

          # Смотрим, какие файлы есть в проекте (для отладки)
          - name: list-files
            script:
              - ls -la

          # Устанавливаем Hugo на сервер, где всё выполняется
          - name: install-hugo
            script:
              - sudo dpkg -i hugo_extended_${VERSION}_linux-amd64.deb  # Запускаем установку
              - rm hugo_extended_${VERSION}_linux-amd64.deb  # Удаляем установочный файл, он больше не нужен

          # Проверяем, что Hugo установился нормально
          - name: check-hugo
            script:
              - hugo version

          # Собираем сайт: Hugo берёт все тексты и картинки и делает готовые HTML-страницы
          - name: build-site
            script:
              - hugo --config hugo.toml --destination ./public  # Сборка, результат кладём в папку public
              - ls -la public/  # Показываем, что получилось после сборки

          # Отправляем готовый сайт в ветку release
          # SourceCraft сам заметит изменения в этой ветке и опубликует сайт
          - name: deploy-site
            script:
              - git checkout -b release  # Переключаемся в ветку release (или создаём, если её нет)
              - ls -la  # Смотрим, какие файлы будут отправлены
              - git add .  # Добавляем все файлы для коммита
              - "git commit -m \"feat: Deploy Hugo site\""  # Сохраняем изменения с понятным сообщением
              - "git push origin release -f"  # Отправляем ветку release на сервер, заменяя старую версию
```
