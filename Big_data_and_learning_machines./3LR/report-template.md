# Отчет ЛР03: Overfitting, Validation and Hyperparameter Tuning

**Студент:** Смирнов Михаил  
**Группа:** ИВТ 3 курс, 1 группа, 1 подгруппа

## Цель
Изучение переобучения, честной валидации и подбора гиперпараметров.

## Данные
Датасеты из ЛР01: cardiovascular_risk, credit_risk

## Методы
- Сравнение train/val метрик
- Выбор feature set по validation F1
- Validation curves
- GridSearchCV
- Финальное сравнение на test

## Результаты

### Generalization gap (cardio, F1)
| Feature set | LR train | LR val | LR gap | RF train | RF val | RF gap |
|-------------|----------|--------|--------|----------|--------|--------|
| full | 0.58 | 0.52 | 0.06 | 0.99 | 0.50 | 0.49 |
| set_A | 0.56 | 0.53 | 0.03 | 0.99 | 0.51 | 0.48 |

### Выбранные feature sets
- cardio LR: set_A (val F1: 0.53)
- cardio RF: set_A (val F1: 0.51)
- credit LR: set_A (val F1: 0.49)
- credit RF: set_A (val F1: 0.47)

### Финальное сравнение на test
| Модель | Baseline F1 | Tuned F1 | Baseline AUC | Tuned AUC |
|--------|-------------|----------|--------------|-----------|
| LR | 0.52 | 0.52 | 0.52 | 0.52 |
| RF | 0.49 | 0.50 | 0.50 | 0.50 |

## Выводы
1. RandomForest сильно переобучается (gap ~0.49)
2. LogisticRegression показывает меньший generalization gap
3. Сокращенный набор признаков немного улучшает валидационные метрики
4. Подбор гиперпараметров не дал значительного улучшения на синтетических данных
5. Честная процедура с отдельным test подтверждает стабильность результатов

## Артефакты
- outputs/generalization_audit.csv
- outputs/model_feature_set_decisions.csv
- outputs/validation_curve_results.csv
- outputs/gridsearch_results_top.csv
- outputs/baseline_vs_tuned_test_results.csv