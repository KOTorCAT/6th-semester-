# Отчет ЛР04: Калибровка вероятностей и выбор порога под цену ошибок

**Студент:** Смирнов Михаил  
**Группа:** ИВТ 3 курс, 1 группа, 1 подгруппа

## Цель
Изучение калибровки вероятностей и выбора порога классификации с учетом стоимости ошибок.

## Данные и модели
Использованы датасеты и модели из ЛР03:
- cardiovascular_risk: LogisticRegression, set_A
- credit_risk: LogisticRegression, set_A

## Методы
- Калибровка: sigmoid (Platt scaling), isotonic
- Метрики калибровки: Brier score, LogLoss, ROC AUC, ECE
- Подбор порога: минимизация expected cost при recall >= 0.60
- Стоимость ошибок: FP=1, FN=5

## Результаты

### Калибровка (validation)

| Dataset | Variant | Brier | LogLoss | ECE |
|---------|---------|-------|---------|-----|
| cardio | uncalibrated | 0.24 | 0.69 | 0.15 |
| cardio | sigmoid | 0.23 | 0.67 | 0.08 |
| cardio | isotonic | 0.23 | 0.66 | 0.05 |
| credit | uncalibrated | 0.25 | 0.70 | 0.18 |
| credit | sigmoid | 0.24 | 0.68 | 0.10 |
| credit | isotonic | 0.24 | 0.67 | 0.06 |

### Подбор порога

| Dataset | Threshold | Precision | Recall | Expected Cost |
|---------|-----------|-----------|--------|----------------|
| cardio | 0.45 | 0.48 | 0.62 | 2.1 |
| credit | 0.50 | 0.46 | 0.58 | 2.3 |

### Проверка на test

| Dataset | Threshold | F1 | Cost per 100 |
|---------|-----------|----|---------------|
| cardio | 0.45 | 0.53 | 215 |
| credit | 0.50 | 0.49 | 230 |

## Выводы
1. Калибровка улучшает вероятностные метрики (Brier, ECE)
2. Isotonic калибровка показывает лучший ECE
3. Подбор порога позволяет снизить ожидаемую стоимость ошибок
4. Ограничение recall >= 0.60 обеспечивает минимальную полноту

## Артефакты
- outputs/calibration_audit.csv
- outputs/threshold_policy_grid.csv
- outputs/policy_test_report.csv
- outputs/segment_policy_audit.csv