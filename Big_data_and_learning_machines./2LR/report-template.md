# Отчет ЛР02: Model Interpretability

**Студент:** Смирнов Михаил  
**Группа:** ИВТ 3 курс, 1 группа, 1 подгруппа

## Цель
Изучение методов интерпретации моделей.

## Методы
- Native и permutation важности
- Partial dependence plots
- Perturbation анализ ошибок

## Результаты
Топ-признак для cardio: thalach
FP: 35, FN: 33 из 150 тестовых

## Артефакты
- outputs/global_importance_comparison.csv
- outputs/partial_dependence_summary.csv
- outputs/error_case_explanations.csv

## Выводы
Методы интерпретации подтверждают важность признаков из ЛР01.
Анализ ошибок показывает примерно равное количество FP и FN.