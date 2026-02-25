## Опис проєкту
У межах проєкту виконано аналіз відкритого набору даних у сфері охорони здоровʼя України —
активних декларацій пацієнтів з лікарями. Проєкт реалізовано з використанням
Git-орієнтованого workflow з feature-гілками, Pull Request та поетапним злиттям у гілку `main`.

## Джерело даних
Портал відкритих даних України:  
https://data.gov.ua/

Набір даних:  
https://data.gov.ua/dataset/a8228262-5576-4a14-beb8-789573573546

## Структура проєкту
- `src/data_load.py` — модуль завантаження відкритих даних
- `src/data_quality_analysis.py` — перевірка якості даних
- `src/data_research.py` — дослідження даних та побудова моделі
- `src/visualization.py` — візуалізація результатів
- `data/raw/` — сирі дані (виключені з Git)
- `reports/data_quality_report.txt` — результати перевірки якості даних
- `reports/data_research/` — результати аналізу та моделювання
- `reports/figures/` — графіки та візуалізації

## Опис виконаних модулів

### Data Load
Реалізовано скрипт для автоматичного завантаження CSV-файлу з порталу data.gov.ua
та збереження його у директорію `data/raw`. Сирі дані виключені з репозиторію
за допомогою файлу `.gitignore`.

### Data Quality Analysis
Виконано перевірку якості даних, зокрема:
- аналіз пропущених значень;
- пошук дублікатів;
- перевірка типів даних.

Результати перевірки збережено у текстовий звіт у папці `reports/`.

### Data Research
Проведено аналітичне дослідження розподілу активних декларацій:
- за віком пацієнтів;
- за статтю;
- за регіонами.

Отримано відповіді на поставлені питання аналізу:
1. Визначено вікову групу з найбільшим гендерним розривом у кількості декларацій.
2. Проаналізовано зміну кількості декларацій зі зростанням віку пацієнтів.
3. Визначено регіони з найбільшою концентрацією декларацій для окремих вікових груп.

Результати збережено у CSV та TXT файли у папці `reports/data_research`.

### Modeling
Також реалізовано модель **Random Forest Regressor** для прогнозування кількості 
активних декларацій (`count_declarations`) за ознаками: `area`, `person_gender`, `person_age`.

Якість моделі оцінено за метриками MAE та R². Отримані значення свідчать про
обмежену прогнозну здатність моделі, що пояснюється відсутністю додаткових
пояснювальних факторів у наборі даних.

### Visualization
Реалізовано модуль візуалізації, який формує графіки:
- розподіл декларацій за віком;
- гендерний розрив за віковими групами;
- топ регіонів за кількістю декларацій для окремих вікових груп.

Графіки збережено у форматі PNG у папці `reports/figures`.

## Робота з Git

Лабораторна виконувалася з використанням системи контролю версій Git
та платформи GitHub. Розробка велась із застосуванням feature-орієнтованого
workflow, де кожен етап проєкту реалізовувався в окремій гілці.

На початковому етапі було створено базову структуру проєкту в гілці `main`
та налаштовано файл `.gitignore`. Після цього для реалізації окремих модулів
створювалися такі feature-гілки:
- `feature/data_load` — для додавання скрипта завантаження відкритих даних;
- `feature/data_quality_analysis` — для реалізації перевірки якості даних;
- `feature/data_research` — для аналітичного дослідження даних та побудови моделі;
- `feature/visualization` — для створення графіків та візуалізації результатів.

Кожна feature-гілка після завершення розробки зливалася у гілку `main`
через Pull Request на GitHub. Для кожного Pull Request було додано опис
виконаних змін, що дозволяло відслідковувати історію
розвитку проєкту та контролювати якість змін.

Окремо було змодельовано ситуацію з merge-конфліктом. Для цього було створено
дві гілки (`feature/conflict_a` та `feature/conflict_b`), у яких паралельно
змінювався файл `README.md`. Конфлікт було розвʼязано шляхом аналізу 
відмінностей між двома версіями однієї секції файлу, видаленням конфліктів та 
формування узгодженого фінального варіанту тексту. Результат розвʼязання конфлікту
зафіксовано окремим комітом у гілці `main`.

Після завершення розробки всіх модулів було додано файл `CHANGELOG.md`,
а також створено Git-тег `v0.1.0`, який позначає перший стабільний реліз проєкту. 
Історія комітів та злиттів відображає поетапну розробку та
використання можливостей Git для керування змінами.

## Git history

$ git log --oneline --graph --decorate --all
* 077fa22 (HEAD -> main, tag: v0.1.0) Add CHANGELOG for v0.1.0
* ef99b78 Add CHANGELOG for v0.1.0
| * 7e596ef (origin/feature/visualization, feature/visualization) Add data visualization module
|/
*   5ffe834 (origin/main) Resolve merge conflict in README.md
|\
| * bdbe895 (origin/feature/conflict_b, feature/conflict_b) Update README questions(B)
* |   b93c6bb Merge pull request #4 from vorobmaks/feature/conflict_a
|\ \
| |/
|/|
| * f0f3623 (origin/feature/conflict_a, feature/conflict_a) Update README questions(A)
|/
*   8be033b Merge pull request #3 from vorobmaks/feature/data_research
|\
| * 0eb74f1 (origin/feature/data_research, feature/data_research) Add data research and Random Forest model
* |   5c99c1b Merge pull request #2 from vorobmaks/feature/data_quality_analysis
|\ \
| |/
|/|
| * 32192e7 (origin/feature/data_quality_analysis, feature/data_quality_analysis) Add data quality analysis and report
|/
*   66d2b43 Merge pull request #1 from vorobmaks/feature/data_load
|\
| * 96161a4 (origin/feature/data_load, feature/data_load) Add data loading script
|/
* c3292ec Update README and .gitignore
* fe4b83c first commit
