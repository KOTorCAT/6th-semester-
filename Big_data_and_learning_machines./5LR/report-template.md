# Отчет ЛР05: Drift Monitoring и Retraining Policy

**Студент:** Смирнов Михаил  
**Группа:** ИВТ 3 курс, 1 группа, 1 подгруппа

## Цель
Изучение методов обнаружения дрейфа данных и формирование политики переобучения моделей.

## Данные
Датасеты: cardiovascular_risk, credit_risk
Окна: reference (0-200), covariate_drift (200-350), prior_drift (350-500)

## Пороги
- alpha = 0.05
- PSI warn = 0.10
- F1 drop для retrain = 0.05
- Cost increase для retrain = 0.15

## Результаты

### Детекция дрифта
Обнаружен дрифт в окнах covariate_drift и prior_drift.
Наибольший PSI: thalach (0.28), credit_history (0.22).

### Мониторинг качества
| Окно | F1 | Delta F1 | Expected Cost | Delta Cost |
|------|-----|----------|---------------|------------|
| reference | 0.54 | 0 | 2.10 | 0 |
| covariate_drift | 0.50 | -0.04 | 2.35 | +0.25 |
| prior_drift | 0.48 | -0.06 | 2.50 | +0.40 |

### Принятые решения
| Окно | Доля дрифта | Delta F1 | Delta Cost | Решение | Причина |
|------|-------------|----------|------------|---------|---------|
| covariate_drift | 0.40 | -0.04 | +0.25 | retrain | drift_share, cost_increase |
| prior_drift | 0.35 | -0.06 | +0.40 | retrain | drift_share, f1_drop, cost_increase |

### Сравнение до и после переобучения
| Сценарий | Фаза | F1 | Expected Cost |
|----------|------|-----|---------------|
| covariate_drift | before | 0.50 | 2.35 |
| covariate_drift | after | 0.53 | 2.15 |
| prior_drift | before | 0.48 | 2.50 |
| prior_drift | after | 0.52 | 2.20 |

## Выводы
1. Дрейф обнаружен в обоих тестовых окнах
2. Переобучение улучшило F1 на 0.03-0.04 и снизило стоимость ошибок на 0.20-0.30
3. Правило retrain сработало корректно для обоих сценариев

## Артефакты
- outputs/drift_detection_audit.csv
- outputs/monitoring_quality_audit.csv
- outputs/retraining_policy_decisions.csv
- outputs/post_retrain_comparison.csv