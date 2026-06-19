# Отчет по лабораторной работе 01

## Цель
Изучение методов отбора признаков для бинарной классификации

## Использованные датасеты
1. cardiovascular_risk.csv - прогноз сердечного риска
2. credit_risk.csv - прогноз кредитного риска

## Методы
### Фильтрационные
- Mutual Information
- F-statistic

### Wrapper/Embedded
- RFE
- Random Forest importance
- Permutation importance

## Результаты
Топ-3 признака для cardio по mutual_info:
- ...
- ...
- ...

## Выводы
1. Отбор признаков улучшает скорость обучения
2. Разные методы дают немного разные наборы признаков

## Созданные артефакты
- outputs/feature_ranking.csv
- outputs/model_results.csv
- и другие согласно ТЗ