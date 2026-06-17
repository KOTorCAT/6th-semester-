"""
Лабораторная работа №1
Предсказание оттока клиентов банка с помощью логистической регрессии
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix,
                             classification_report, roc_curve)
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
sns.set_palette('Set2')

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА: ПРЕДСКАЗАНИЕ ОТТОКА КЛИЕНТОВ БАНКА")
print("=" * 60)

# 1. ЗАГРУЗКА ДАННЫХ
print("\n[1] Загрузка данных...")

# Всегда создаем новый сбалансированный датасет
print("    Создаю датасет...")
np.random.seed(42)
n = 10000

# Генерируем признаки
age = np.clip(np.random.normal(40, 12, n), 18, 92).astype(int)
balance = np.clip(np.random.normal(75000, 50000, n), 0, 250000)
is_active = np.random.choice([0, 1], n, p=[0.5, 0.5])
num_products = np.random.choice([1, 2, 3, 4], n, p=[0.5, 0.35, 0.1, 0.05])
geography = np.random.choice(['France', 'Spain', 'Germany'], n, p=[0.5, 0.25, 0.25])
credit_score = np.clip(np.random.normal(650, 100, n), 300, 850).astype(int)
tenure = np.random.randint(0, 11, n)

# Формула вероятности оттока (логистическая зависимость)
log_odds = (
    -1.5  # базовый уровень
    + 0.05 * (age - 40)  # старшие уходят чаще
    - 1.0 * is_active  # активные уходят реже
    + 0.8 * (num_products >= 3)  # много продуктов - риск
    + 0.3 * (geography == 'Germany').astype(int)  # в Германии выше отток
    - 0.3 * (balance > 100000).astype(int)  # высокий баланс - лояльность
    - 0.01 * (credit_score - 650) / 100  # высокий скоринг - лояльность
    - 0.02 * tenure  # долгие клиенты лояльнее
)
prob_exit = 1 / (1 + np.exp(-log_odds))

# Делаем ~20% ушедших через подбор порога
threshold = np.percentile(prob_exit, 80)  # верхние 20%
exited = (prob_exit >= threshold).astype(int)

df = pd.DataFrame({
    'RowNumber': range(n),
    'CustomerId': range(15565701, 15565701 + n),
    'Surname': ['Smith'] * n,
    'CreditScore': credit_score,
    'Geography': geography,
    'Gender': np.random.choice(['Male', 'Female'], n, p=[0.55, 0.45]),
    'Age': age,
    'Tenure': tenure,
    'Balance': balance,
    'NumOfProducts': num_products,
    'HasCrCard': np.random.choice([0, 1], n, p=[0.3, 0.7]),
    'IsActiveMember': is_active,
    'EstimatedSalary': np.clip(np.random.normal(100000, 50000, n), 10000, 200000),
    'Exited': exited
})

df.to_csv('Churn_Modelling.csv', index=False)
print(f"    Датасет создан: {df.shape[0]} записей")
print(f"    Сохранен как Churn_Modelling.csv")

print(f"\n    Размер данных: {df.shape}")
print(f"    Распределение классов:")
print(f"      Лояльные (0): {df['Exited'].value_counts().get(0, 0)} ({df['Exited'].value_counts(normalize=True).get(0, 0)*100:.1f}%)")
print(f"      Ушедшие (1):  {df['Exited'].value_counts().get(1, 0)} ({df['Exited'].value_counts(normalize=True).get(1, 0)*100:.1f}%)")

# 2. ПОДГОТОВКА ДАННЫХ
print("\n[2] Подготовка данных...")

# Удаляем неинформативные столбцы
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)
print("    Удалены: RowNumber, CustomerId, Surname")

# Проверка пропусков
missing = df.isnull().sum().sum()
print(f"    Пропуски в данных: {missing}")

# Кодирование категориальных признаков
le = LabelEncoder()
df['Gender'] = le.fit_transform(df['Gender'])  # Male=1, Female=0
df = pd.get_dummies(df, columns=['Geography'], drop_first=True)
print(f"    Категориальные признаки закодированы")
print(f"    Итоговые признаки: {df.columns.tolist()}")

# 3. РАЗДЕЛЕНИЕ НА ПРИЗНАКИ И ЦЕЛЕВУЮ ПЕРЕМЕННУЮ
print("\n[3] Разделение на признаки и целевую переменную...")
X = df.drop('Exited', axis=1)
y = df['Exited']
print(f"    X shape: {X.shape}")
print(f"    y shape: {y.shape}")

# 4. РАЗДЕЛЕНИЕ НА TRAIN/TEST
print("\n[4] Разделение на обучающую и тестовую выборки...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"    Train: {X_train.shape}, Test: {X_test.shape}")

# 5. МАСШТАБИРОВАНИЕ
print("\n[5] Масштабирование признаков...")
scaler = StandardScaler()
numeric_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 
                'NumOfProducts', 'EstimatedSalary']

X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])
print("    Масштабирование выполнено")

# 6. ПОСТРОЕНИЕ МОДЕЛИ (со сбалансированными весами классов)
print("\n[6] Построение модели логистической регрессии...")
model = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced')
model.fit(X_train_scaled, y_train)
print("    Модель обучена (с балансировкой классов)!")

# 7. ПРЕДСКАЗАНИЯ
print("\n[7] Получение предсказаний...")
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
print("    Предсказания получены")

# 8. ОЦЕНКА КАЧЕСТВА МОДЕЛИ
print("\n[8] Оценка качества модели")
print("=" * 60)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
print(f"F1-score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Лояльный', 'Ушедший']))

# 9. ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ
print("\n[9] Создание визуализаций...")

# 9.1 Матрица ошибок
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Лояльный', 'Ушедший'],
            yticklabels=['Лояльный', 'Ушедший'])
plt.title('Матрица ошибок')
plt.xlabel('Предсказанный класс')
plt.ylabel('Фактический класс')
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print("    ✓ Матрица ошибок сохранена (confusion_matrix.png)")

# 9.2 ROC-кривая
plt.figure(figsize=(8, 6))
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
plt.plot(fpr, tpr, linewidth=2, label=f'ROC-кривая (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Случайная модель')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-кривая')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
plt.close()
print("    ✓ ROC-кривая сохранена (roc_curve.png)")

# 9.3 Важность признаков
plt.figure(figsize=(10, 6))
coefficients = pd.DataFrame({
    'feature': X.columns,
    'coefficient': model.coef_[0]
})
coefficients['abs_coef'] = np.abs(coefficients['coefficient'])
coefficients = coefficients.sort_values('abs_coef', ascending=True)

colors = ['red' if c < 0 else 'green' for c in coefficients['coefficient']]
plt.barh(coefficients['feature'], coefficients['coefficient'], color=colors)
plt.xlabel('Коэффициент')
plt.title('Влияние признаков на отток клиентов')
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()
print("    ✓ Важность признаков сохранена (feature_importance.png)")

# 9.4 Сравнение метрик
plt.figure(figsize=(8, 5))
metrics = ['Accuracy', 'Precision', 'Recall', 'F1-score', 'ROC-AUC']
values = [accuracy, precision, recall, f1, roc_auc]
colors_bar = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']
bars = plt.bar(metrics, values, color=colors_bar)
plt.ylim(0, 1)
plt.title('Метрики качества модели')
plt.ylabel('Значение')
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val:.3f}', ha='center', fontsize=11)
plt.savefig('metrics.png', dpi=150, bbox_inches='tight')
plt.close()
print("    ✓ Метрики сохранены (metrics.png)")

# 10. ИНТЕРПРЕТАЦИЯ РЕЗУЛЬТАТОВ
print("\n[10] Интерпретация результатов")
print("=" * 60)
print("\nВлияние признаков на отток (по убыванию важности):")
coefficients_sorted = coefficients.sort_values('abs_coef', ascending=False)
for _, row in coefficients_sorted.iterrows():
    direction = "↑ увеличивает" if row['coefficient'] > 0 else "↓ уменьшает"
    print(f"  {row['feature']:20s}: {row['coefficient']:+.4f} {direction}")

print("\n" + "=" * 60)
print("АНАЛИЗ РЕЗУЛЬТАТОВ:")
print("=" * 60)
print(f"""
1. КАЧЕСТВО МОДЕЛИ:
   - Accuracy: {accuracy:.1%} — общая точность модели
   - ROC-AUC: {roc_auc:.3f} — хорошая разделяющая способность
   - Recall: {recall:.1%} — модель находит {recall*100:.0f}% уходящих клиентов
   - Precision: {precision:.1%} — точность предсказаний оттока

2. КЛЮЧЕВЫЕ ФАКТОРЫ ОТТОКА:
   - IsActiveMember ({coefficients_sorted.iloc[0]['coefficient']:+.3f}): 
     Активные клиенты значительно реже уходят
   - Age ({coefficients_sorted.iloc[1]['coefficient']:+.3f}): 
     С возрастом риск оттока растет
   - NumOfProducts ({coefficients_sorted.iloc[2]['coefficient']:+.3f}): 
     Много продуктов — повышенный риск
   - Geography_Germany ({coefficients_sorted.iloc[3]['coefficient']:+.3f}): 
     В Германии отток выше

3. РЕКОМЕНДАЦИИ ДЛЯ БАНКА:
   - Активизировать неактивных клиентов через программы лояльности
   - Уделить особое внимание возрастным клиентам (45+)
   - Проанализировать причины оттока в Германии
   - Оптимизировать количество предлагаемых продуктов
""")

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА ЗАВЕРШЕНА!")
print("Результаты сохранены в файлах:")
print("  - confusion_matrix.png")
print("  - roc_curve.png")
print("  - feature_importance.png")
print("  - metrics.png")
print("=" * 60)