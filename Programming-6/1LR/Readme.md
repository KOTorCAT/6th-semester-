# Конфигурация SourceCraft для автоматической сборки и деплоя Hugo-сайта

Этот код нужен, чтобы при каждом пуше кода автоматически запускалась сборка Hugo-сайта и его выкладка (деплой).

---

## Что делает этот код?

1. **Следит за изменениями** — когда пушите код в ветку `main`, запускается процесс.
2. **Проверяет ссылки** — чтобы на сайте не было битых ссылок.
3. **Скачивает и устанавливает Hugo** — нужной версии.
4. **Собирает сайт** 
5. **Деплоит (выкладывает)** — отправляет готовый сайт в отдельную ветку `release`.

---

## Код 

```yaml
# Триггер: запуск при пуше в main
on:
  push:
    workflows: [build-site]      # Какой процесс запускать
    filter:
      branches: main              # Только из ветки main

# Что именно делаем
workflows:
  build-site:
    env:
      VERSION: 0.157.0            # Какая версия Hugo нужна

    tasks:
      # Часть 1: Проверяем, что все ссылки в файлах работают
      - name: check-links
        cubes:
          - name: run-link-check
            action: tcort/github-action-markdown-link-check@v1
            with:
              base-branch: main
              use-verbose-mode: yes   # Подробный отчёт о битых ссылках

      # Часть 2: Собираем и выкладываем сайт (только если ссылки в порядке)
      - name: build-and-deploy
        needs: [check-links]          # Ждём успеха первой задачи
        
        cubes:
          # 1. Скачиваем установочный файл Hugo
          - name: get-hugo
            script:
              - curl -LJO https://github.com/gohugoio/hugo/releases/download/v${VERSION}/hugo_extended_${VERSION}_linux-amd64.deb

          # 2. Смотрим, что скачалось (для отладки)
          - name: list-files
            script:
              - ls -la

          # 3. Устанавливаем Hugo и удаляем установщик
          - name: install-hugo
            script:
              - sudo dpkg -i hugo_extended_${VERSION}_linux-amd64.deb   # Ставим пакет
              - rm hugo_extended_${VERSION}_linux-amd64.deb             # Чистим мусор

          # 4. Проверяем, что Hugo встал правильно
          - name: check-hugo
            script:
              - hugo version

          # 5. Собираем сайт из исходников в папку public
          - name: build-site
            script:
              - hugo --config hugo.toml --destination ./public
              - ls -la public/          # Показываем результат сборки

          # 6. Деплоим: создаём ветку release и пушим туда готовый сайт
          - name: deploy-site
            script:
              - git checkout -b release        # Создаём/переключаемся на ветку release
              - ls -la                         # Смотрим, что будем коммитить
              - git add .                      # Добавляем всё под Git
              - "git commit -m \"feat: Deploy Hugo site\""   # Сохраняем изменения
              - "git push origin release -f"   # Принудительно пушим (перезаписываем старую версию)