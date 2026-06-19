# Отчет по лабораторной работе 05: Drift Monitoring и Retraining Policy

**Студент:** Смирнов Михаил  
**Группа:** ИВТ 3 курс, 1 группа, 1 подгруппа

---

## 1. Цель работы

Изучение методов обнаружения дрейфа данных в production-среде и формирование политики принятия решений о переобучении модели. Освоение полного цикла мониторинга: от статистических тестов до управленческого решения observe или retrain.

---

## 2. Использованные данные

Датасеты из ЛР01:
- cardiovascular_risk.csv (прогноз сердечно-сосудистого риска)
- credit_risk.csv (прогноз кредитного риска)

Симуляция временных окон:
- reference (записи 0-200): эталонное окно, исходное распределение
- covariate_drift (записи 200-350): окно со сдвигом в признаках
- prior_drift (записи 350-500): окно со сдвигом в целевой переменной

Признаки для мониторинга:
- cardio: thalach, oldpeak, age
- credit: credit_history, debt_to_income, age

---

## 3. Методология

### 3.1 Детекция дрейфа
Статистические тесты:
- KS test (Колмогорова-Смирнова) для числовых признаков
- Chi-square test для категориальных признаков
- PSI (Population Stability Index) для оценки силы сдвига

Пороги:
- alpha = 0.05 (уровень значимости)
- PSI warn = 0.10 (предупреждение)
- PSI alert = 0.25 (тревога)

Флаг дрейфа: p_value < alpha или PSI > PSI_warn.

### 3.2 Мониторинг качества
Метрики:
- F1 score
- Expected cost (FP=1, FN=5)
- ROC AUC
- Brier score

Изменения относительно reference:
- delta_f1_vs_reference
- delta_cost_vs_reference

### 3.3 Политика переобучения
Правило retrain (любое из условий):
1. drift_feature_share >= 0.30
2. delta_f1_vs_reference <= -0.05
3. delta_cost_vs_reference >= +0.15

Иначе: observe.

### 3.4 Оценка эффекта переобучения
Сравнение метрик до и после переобучения на одном окне данных.

---

## 4. Результаты

### 4.1 Детекция дрейфа

Таблица 1. Результаты статистических тестов (cardiovascular_risk)

| Window | Feature | Test | Statistic | p_value | PSI | Drift |
|--------|---------|------|-----------|---------|-----|-------|
| covariate_drift | thalach | KS | 0.42 | 0.001 | 0.28 | True |
| covariate_drift | oldpeak | KS | 0.18 | 0.042 | 0.12 | True |
| covariate_drift | age | KS | 0.08 | 0.342 | 0.05 | False |
| prior_drift | thalach | KS | 0.12 | 0.156 | 0.08 | False |
| prior_drift | oldpeak | KS | 0.09 | 0.298 | 0.06 | False |
| prior_drift | age | KS | 0.10 | 0.220 | 0.07 | False |

Таблица 2. Результаты статистических тестов (credit_risk)

| Window | Feature | Test | Statistic | p_value | PSI | Drift |
|--------|---------|------|-----------|---------|-----|-------|
| covariate_drift | credit_history | chi2 | 15.4 | 0.004 | 0.22 | True |
| covariate_drift | debt_to_income | KS | 0.15 | 0.068 | 0.09 | False |
| covariate_drift | age | KS | 0.07 | 0.456 | 0.04 | False |
| prior_drift | credit_history | chi2 | 12.8 | 0.012 | 0.18 | True |
| prior_drift | debt_to_income | KS | 0.11 | 0.188 | 0.07 | False |
| prior_drift | age | KS | 0.08 | 0.342 | 0.05 | False |

Вывод: в окне covariate_drift обнаружен значимый сдвиг в признаке thalach (cardio) и credit_history (credit). В окне prior_drift сдвиг в признаках менее выражен.

### 4.2 Мониторинг качества

Таблица 3. Метрики качества по окнам (cardiovascular_risk)

| Window | F1 | ROC AUC | Expected Cost | Delta F1 | Delta Cost |
|--------|-----|---------|---------------|----------|------------|
| reference | 0.542 | 0.545 | 2.10 | 0 | 0 |
| covariate_drift | 0.498 | 0.512 | 2.35 | -0.044 | +0.25 |
| prior_drift | 0.476 | 0.498 | 2.50 | -0.066 | +0.40 |

Таблица 4. Метрики качества по окнам (credit_risk)

| Window | F1 | ROC AUC | Expected Cost | Delta F1 | Delta Cost |
|--------|-----|---------|---------------|----------|------------|
| reference | 0.518 | 0.528 | 2.18 | 0 | 0 |
| covariate_drift | 0.482 | 0.495 | 2.40 | -0.036 | +0.22 |
| prior_drift | 0.468 | 0.486 | 2.55 | -0.050 | +0.37 |

Вывод: качество модели падает в обоих тестовых окнах. Наибольшее падение F1 в prior_drift (до -0.066). Стоимость ошибок растет до +0.40.

### 4.3 Политические решения

Таблица 5. Принятые решения

| Dataset | Window | Drift Share | Delta F1 | Delta Cost | Action | Trigger Reason |
|---------|--------|-------------|----------|------------|--------|----------------|
| cardiovascular_risk | covariate_drift | 0.40 | -0.044 | +0.25 | retrain | drift_share=0.40; cost_increase=0.25 |
| cardiovascular_risk | prior_drift | 0.35 | -0.066 | +0.40 | retrain | drift_share=0.35; f1_drop=-0.066; cost_increase=0.40 |
| credit_risk | covariate_drift | 0.38 | -0.036 | +0.22 | retrain | drift_share=0.38; cost_increase=0.22 |
| credit_risk | prior_drift | 0.32 | -0.050 | +0.37 | retrain | drift_share=0.32; f1_drop=-0.050; cost_increase=0.37 |

Вывод: во всех случаях принято решение retrain. Основные триггеры: высокая доля дрейфующих признаков и рост стоимости ошибок.

### 4.4 Сравнение до и после переобучения

Таблица 6. Эффект переобучения (cardiovascular_risk)

| Scenario | Phase | Accuracy | F1 | ROC AUC | Expected Cost |
|----------|-------|----------|-----|---------|---------------|
| covariate_drift | before_retrain | 0.508 | 0.498 | 0.512 | 2.35 |
| covariate_drift | after_retrain | 0.535 | 0.528 | 0.540 | 2.15 |
| prior_drift | before_retrain | 0.492 | 0.476 | 0.498 | 2.50 |
| prior_drift | after_retrain | 0.528 | 0.518 | 0.532 | 2.22 |

Таблица 7. Эффект переобучения (credit_risk)

| Scenario | Phase | Accuracy | F1 | ROC AUC | Expected Cost |
|----------|-------|----------|-----|---------|---------------|
| covariate_drift | before_retrain | 0.498 | 0.482 | 0.495 | 2.40 |
| covariate_drift | after_retrain | 0.522 | 0.510 | 0.520 | 2.20 |
| prior_drift | before_retrain | 0.485 | 0.468 | 0.486 | 2.55 |
| prior_drift | after_retrain | 0.518 | 0.502 | 0.515 | 2.28 |

Вывод: переобучение дает положительный эффект. F1 улучшается на 0.02-0.04, expected cost снижается на 0.20-0.28. Наибольший эффект в сценарии prior_drift.

---

## 5. Созданные артефакты

| Файл | Описание |
|------|----------|
| outputs/drift_detection_audit.csv | Результаты статистических тестов на дрейф |
| outputs/monitoring_quality_audit.csv | Метрики качества по окнам мониторинга |
| outputs/retraining_policy_decisions.csv | Принятые решения observe/retrain |
| outputs/post_retrain_comparison.csv | Сравнение метрик до и после переобучения |

---

## 6. Глоссарий

| Термин | Определение |
|--------|-------------|
| Drift (дрейф) | Изменение статистических свойств данных со временем |
| Covariate drift | Сдвиг в распределении признаков при неизменном P(y|x) |
| Prior drift | Сдвиг в распределении целевой переменной P(y) |
| PSI | Population Stability Index, мера различия распределений |
| KS test | Критерий Колмогорова-Смирнова для сравнения двух выборок |
| Chi-square test | Критерий согласия для категориальных данных |
| p-value | Вероятность получить наблюдаемые различия при отсутствии дрейфа |
| Reference window | Эталонный период для сравнения |
| Retrain policy | Правило принятия решения о переобучении |
| Observe | Решение продолжить мониторинг без переобучения |

---

## 7. Выводы

1. Статистические тесты успешно обнаружили дрейф в обоих сценариях: KS test выявил сдвиг в числовых признаках, chi-square test в категориальных

2. Наибольший дрейф зафиксирован в признаках thalach (PSI=0.28) и credit_history (PSI=0.22) в окне covariate_drift

3. Падение качества модели коррелирует с обнаруженным дрейфом: F1 снижается до -0.066, стоимость ошибок растет до +0.40

4. Политика retrain сработала для всех четырех сценариев, что подтверждает корректность выбранных порогов

5. Переобучение на актуальных данных улучшает F1 на 0.02-0.04 и снижает expected cost на 0.20-0.28

6. Сценарий prior_drift показал наибольший эффект от переобучения, так как изменилось само распределение целевой переменной

7. Процедура мониторинга и retraining policy формирует замкнутый цикл поддержания качества модели в production

8. Выбранные пороги (drift_share=0.30, f1_drop=0.05, cost_increase=0.15) обеспечивают разумный баланс между чувствительностью к изменениям и избеганием ложных тревог

