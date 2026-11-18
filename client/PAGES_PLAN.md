# План реалізації сторінок клієнта

Джерело: дизайн-канвас (3 групи екранів + дизайн-система), поточна архітектура клієнта, API сервера.

## 0. Вихідні умови

**Вже є:** Vue 3 + Vite, PrimeVue 5 з пресетом `hr-preset.ts` (cobalt/stone, dark через `.app-dark`), Pinia, TanStack Query, `useTheme`, `shared/ui` (`StatusTag`, `ScoreBar`, `AiStatus`, `AiSummary`), порожні папки `features/auth/*`, `layouts/`, `pages/private/`, `shared/api/`, `shared/utils/`, один роут `/` → `HomePage` (демо компонентів).

**Архітектурні правила (тримаємось їх у всіх кроках):**
- `pages/*` — тонкі: збирають фічі й лейаут, без бізнес-логіки і без викликів API напряму.
- `features/<name>/{api,components,composables,stores,types}` — уся логіка домену. API-функції та query-хуки лежать у `api/`, фічі не імпортують одна одну (спільне виносимо в `shared`).
- `shared/*` не знає про домени. `layouts/*` знають лише про shell і навігацію.
- Server state — TanStack Query, client state (сесія, UI) — Pinia. Форми — локальний стан у компонентах/композаблах.
- Усі лейбли, коментарі й імена в коді — англійською (як у [English in code](../.claude/projects/-home-nikitos4443-HR-APP/memory/feedback-english-in-code.md)); українські тексти з дизайну перекладаємо в англійські.
- Дизайн-токени беремо тільки з пресета/PrimeVue, жодних нових hex у компонентах. Material Symbols з дизайну замінюємо на PrimeIcons (як у вже зроблених `shared/ui`).

## Карта екранів → роути

| Екран у дизайні | Роут | Доступ | Page-файл |
|---|---|---|---|
| Лендінг | `/` | public | `pages/public/LandingPage.vue` |
| Вхід / Реєстрація | `/auth` | guest-only | `pages/public/AuthPage.vue` |
| Публічна вакансія | `/vacancies/:publicId` | public | `pages/public/PublicVacancyPage.vue` |
| Подання заявки | `/vacancies/:publicId/apply` | public | `pages/public/ApplyPage.vue` |
| AI-асистент | `/vacancies/:publicId/chat` | public | `pages/public/ChatPage.vue` |
| Скринінг (відео/текст) | `/screening/:token` | public (token) | `pages/public/ScreeningPage.vue` |
| Фінал/стани скринінгу | `/screening/:token/done` + стани на тій самій сторінці | public (token) | `pages/public/ScreeningEndPage.vue` |
| Вакансії | `/app/vacancies` | auth | `pages/private/VacanciesPage.vue` |
| Створення/редагування | `/app/vacancies/new`, `/app/vacancies/:id/edit` | auth | `pages/private/VacancyFormPage.vue` |
| Деталі вакансії · Кандидати | `/app/vacancies/:id` (+ drawer `?candidate=:applicationId`) | auth | `pages/private/VacancyDetailPage.vue` |
| Профіль компанії | `/app/company` | `company_admin` | `pages/private/CompanyPage.vue` |
| Команда | `/app/team` | `company_admin` | `pages/private/TeamPage.vue` |
| 403 / 404 | `/forbidden`, `/:pathMatch(.*)*` | any | `pages/public/ForbiddenPage.vue`, `NotFoundPage.vue` |

> Припущення: публічний ідентифікатор у посиланні — `publicId` (в дизайні `hrapp.ua/vacancies/a4f2c1`). Якщо сервер поки віддає числовий `id` — використаємо його, замінити пізніше буде одним рядком у `features/vacancies/api`.

## Блокери з боку сервера (потрібно узгодити до відповідних кроків)

Зараз є: `/auth`, `/auth/token`, CRUD `/users`, `/companies`, `/vacancies`, `/flow/*` (presigned resume, screening token, video upload url, text answer), Socket.IO чат (`chat_start`, `msg_event`).

Немає (потрібно для дизайну):
1. **Список заявок вакансії** + фільтри/сортування/агрегати за статусом, деталі заявки (AI-огляд резюме, відповіді скринінгу, транскрипція, хронологія) → кроки 4.
2. **Дії над заявкою**: invite to screening / shortlist / reject, bulk → крок 4.
3. **Питання скринінгу вакансії** (CRUD або вкладено у vacancy) і їх видача за токеном (`GET /flow/screening/{token}` зараз віддає лише `application_id/vacancy_id/status`) → кроки 3, 7.
4. **Публічне читання вакансії** без JWT → крок 5.
5. **Повторний запуск AI-відбору** та статус AI-відбору у вакансії → крок 3.
6. Поточний користувач (`GET /auth/me` або декод JWT на клієнті — `id/sub/role` вже в токені) → крок 1.

Для кроків 1–3 і 5–6 можна починати одразу; кроки 4 і 7 на старті йдуть на моках (MSW-подібний шар у `features/*/api/*.mock.ts`, див. крок 0).

---

## Крок 0. Фундамент (до першої сторінки)

Мета: HTTP-шар, конфіг, спільні UI-примітиви, що повторюються на кількох екранах.

| Файл | Призначення |
|---|---|
| `src/shared/config/env.ts` | Типізований доступ до `import.meta.env` (`VITE_API_URL`, `VITE_SOCKET_URL`). |
| `env.d.ts` (правка) | Типи `ImportMetaEnv`. |
| `.env.example` | Приклад змінних оточення. |
| `src/shared/api/http.ts` | `fetch`-обгортка: base URL, JSON, підстановка `Authorization: Bearer`, нормалізація помилок. |
| `src/shared/api/errors.ts` | `ApiError` (status, detail), хелпери `isUnauthorized/isForbidden/isNotFound`. |
| `src/shared/api/query-keys.ts` | Фабрики ключів TanStack Query на домен. |
| `src/shared/api/index.ts` | Публічний експорт шару. |
| `src/shared/api/token-storage.ts` | Читання/запис токена (localStorage з try/catch, як у `useTheme`). |
| `src/app/providers/primevue.ts` (правка) | Підключити `ToastService`, `ConfirmationService`. |
| `src/app/App.vue` (правка) | Змонтувати глобальні `<Toast />` і `<ConfirmDialog />`. |
| `src/shared/ui/page-header/PageHeader.vue` | Заголовок сторінки + підзаголовок + слот дій (повторюється на всіх приватних екранах). |
| `src/shared/ui/empty-state/EmptyState.vue` | Іконка/заголовок/опис/CTA — стан «порожньо». |
| `src/shared/ui/error-state/ErrorState.vue` | Помилка завантаження з кнопкою «Retry», варіанти 403/404 через пропс. |
| `src/shared/ui/form-field/FormField.vue` | Label + required-зірочка + hint + error message для будь-якого PrimeVue-контролу. |
| `src/shared/ui/app-logo/AppLogo.vue` | Логотип «HR App» (лендінг, auth, sidebar). |
| `src/shared/ui/avatar-initials/AvatarInitials.vue` | Аватар з ініціалів (кандидати, користувач, компанія). |
| `src/shared/ui/table-skeleton/TableSkeleton.vue` | Скелетон рядків таблиці. |
| `src/shared/ui/index.ts` (правка) | Експорт нових компонентів. |
| `src/shared/utils/format.ts` | `formatSalaryRange`, `formatDate`, `formatDuration`, `initials`. |
| `src/shared/utils/clipboard.ts` | `copyToClipboard` для «Copy link». |
| `src/pages/dev/UiKitPage.vue` | Переїжджає в `pages/dev/UiKitPage.vue` на `/dev/ui` (лише в dev), `/` стає лендінгом. |

Залежність для форм (рішення нижче): `@primevue/forms` + `zod`.

## Крок 1. Автентифікація, лейаути, роутинг, гарди

Мета: працюючий вхід/реєстрація, shell застосунку, захист роутів по ролях.

**Feature `features/auth`**

| Файл | Призначення |
|---|---|
| `types/auth.ts` | `UserRole`, `AuthUser`, `LoginPayload`, `RegisterPayload`, `TokenResponse`. |
| `api/auth.api.ts` | `login` (form-urlencoded на `/auth/token`), `register` (`POST /auth`). |
| `api/auth.queries.ts` | `useLoginMutation`, `useRegisterMutation`. |
| `stores/session.store.ts` | Pinia: токен, поточний користувач (декод JWT: `id`, `sub`, `role`), `isAuthenticated`, `hasRole`, `logout`. |
| `composables/useAuthForm.ts` | Режим вхід/реєстрація, схема валідації (username ≥ 3, lowercase, пароль), submit + обробка помилок. |
| `components/LoginForm.vue` | Форма входу, алерт «invalid credentials», loading-кнопка. |
| `components/RegisterForm.vue` | Форма реєстрації, інлайн-помилки, disabled-кнопка до валідності. |
| `components/AuthTabs.vue` | Перемикач Login / Sign up. |
| `components/UserMenu.vue` | Аватар, ім'я, бейдж ролі, меню з logout (використовує тема-перемикач). |

**Layouts**

| Файл | Призначення |
|---|---|
| `layouts/PublicLayout.vue` | Хедер (лого, theme toggle, «Sign in») + `<slot/>` — лендінг, публічна вакансія, apply. |
| `layouts/AuthLayout.vue` | Центрована колонка з лого — `/auth`. |
| `layouts/AppShellLayout.vue` | Sidebar + topbar + `<RouterView/>` для `/app/*`. |
| `layouts/CandidateLayout.vue` | Мінімальний хедер без сайдбара для скринінгу/чату (без акаунта кандидата). |
| `layouts/components/SideNav.vue` | Навігація (Vacancies / Company / Team), приховує пункти за роллю, бейдж лічильника. |
| `layouts/components/TopBar.vue` | Назва компанії, `ThemeToggle`, `UserMenu`. |
| `shared/ui/theme-toggle/ThemeToggle.vue` | Кнопка на базі `useTheme` (зараз дубльована в демо-сторінці). |

**Router**

| Файл | Призначення |
|---|---|
| `app/router/index.ts` (правка) | Створення роутера, підключення guards. |
| `app/router/routes.ts` | Декларація всіх роутів з lazy-імпортами сторінок і `meta` (`layout`, `requiresAuth`, `roles`, `guestOnly`). |
| `app/router/guards.ts` | `beforeEach`: редірект неавторизованих на `/auth?redirect=…`, guest-only, перевірка ролі → `/forbidden`. |
| `app/router/meta.d.ts` | Типізація `RouteMeta`. |
| `app/App.vue` (правка) | Вибір layout за `route.meta.layout`. |

**Pages**

| Файл | Призначення |
|---|---|
| `pages/public/AuthPage.vue` | `AuthLayout` + `AuthTabs` + форми, redirect після входу. |
| `pages/public/ForbiddenPage.vue` | 403 через `ErrorState`. |
| `pages/public/NotFoundPage.vue` | 404 через `ErrorState`. |

Перевірка кроку: вхід → `/app/vacancies` (поки заглушка), прямий перехід без токена → `/auth`, `hr` на `/app/company` → `/forbidden`.

## Крок 2. Профіль компанії і команда

**Feature `features/companies`**

| Файл | Призначення |
|---|---|
| `types/company.ts` | `Company`, `UpdateCompanyPayload`. |
| `api/companies.api.ts` | `getCompany`, `updateCompany`. |
| `api/companies.queries.ts` | `useCompanyQuery`, `useUpdateCompanyMutation` (інвалідація + toast). |
| `composables/useCompanyForm.ts` | Схема (name required, website — повний URL), dirty-стан, reset. |
| `components/CompanyForm.vue` | Форма з дизайну: name, description, website, Save/Cancel. |
| `components/CompanyPreviewCard.vue` | Блок «Як бачать кандидати». |

**Feature `features/users`**

| Файл | Призначення |
|---|---|
| `types/user.ts` | `User`, `CreateHrPayload`. |
| `api/users.api.ts` | `listUsers`, `createUser`, `deleteUser`. |
| `api/users.queries.ts` | Query/mutation-хуки. |
| `components/UsersTable.vue` | Таблиця користувачів (аватар, роль, дата, дії). |
| `components/CreateHrDialog.vue` | Діалог «Add HR» (username/password). |
| `composables/useDeleteUser.ts` | `ConfirmDialog` «Delete user?» + мутація. |

**Pages:** `pages/private/CompanyPage.vue`, `pages/private/TeamPage.vue` (обидві — `roles: ['company_admin']`).

## Крок 3. Вакансії: список і форма

**Feature `features/vacancies`**

| Файл | Призначення |
|---|---|
| `types/vacancy.ts` | `Vacancy`, `VacancyStatus`, `EmploymentType`, `AiSelectionStatus`, `VacancyFormValues`, `ScreeningQuestion`. |
| `api/vacancies.api.ts` | `list/get/create/update/delete`. |
| `api/vacancies.queries.ts` | `useVacanciesQuery(filters)`, `useVacancyQuery(id)`, мутації + toast. |
| `composables/useVacancyFilters.ts` | Фільтри/пагінація/сорт у `route.query` (шарингові URL). |
| `composables/useVacancyForm.ts` | Схема (salary min ≤ max, question duration ≥ 10), dirty-guard `onBeforeRouteLeave`, мапінг form ↔ API. |
| `composables/useQuestionList.ts` | Додавання/видалення/переставляння питань скринінгу. |
| `composables/useStringList.ts` | Спільна логіка списків «Responsibilities / Requirements / Nice to have». |
| `components/VacanciesTable.vue` | Таблиця (DataTable): назва+локація, тип, зарплата, дедлайн, `StatusTag`, `AiStatus`, лічильник, дії. |
| `components/VacancyFilters.vue` | Пошук + 3 селекти + Reset. |
| `components/VacancyRowActions.vue` | Edit + меню (copy link, close, delete з confirm). |
| `components/form/VacancyBasicsSection.vue` | Секція «Basics». |
| `components/form/SalarySection.vue` | Секція зарплатної вилки + помилка діапазону. |
| `components/form/DescriptionSection.vue` | Опис. |
| `components/form/BulletListsSection.vue` | Три списки з drag-перестановкою. |
| `components/form/DeadlineStatusSection.vue` | Дедлайн, часовий пояс, статус. |
| `components/form/ScreeningQuestionsSection.vue` | Список питань (video/text, max duration). |
| `components/form/ScreeningQuestionItem.vue` | Одне питання. |
| `components/form/FormActionBar.vue` | Sticky-панель «unsaved changes / Cancel / Save». |

**Pages:** `pages/private/VacanciesPage.vue` (таблиця + skeleton + empty + error), `pages/private/VacancyFormPage.vue` (create/edit за роутом).

> Drag-and-drop: або `vuedraggable-next`/`@vueuse/integrations` (sortable), або лише кнопки up/down з дизайну на першому етапі — рекомендую кнопки (є в дизайні) і drag додати пізніше.

## Крок 4. Деталі вакансії: кандидати і картка кандидата

Залежить від серверних пунктів 1–2.

**Feature `features/applications`**

| Файл | Призначення |
|---|---|
| `types/application.ts` | `Application`, `ApplicationStatus`, `ScreeningStatus`, `ResumeAnalysis`, `ScreeningAnswer`, `TimelineEvent`. |
| `api/applications.api.ts` | `listByVacancy`, `getApplication`, `invite`, `shortlist`, `reject` (+ bulk). |
| `api/applications.queries.ts` | Хуки з оптимістичним оновленням статусу. |
| `composables/useApplicationFilters.ts` | Таби статусів, пошук, сорт — у `route.query`. |
| `composables/useBulkSelection.ts` | Вибір рядків + bulk-дії. |
| `composables/useCandidateDrawer.ts` | Відкриття/закриття drawer через `?candidate=`. |
| `components/ApplicationsTable.vue` | Ранг, кандидат, резюме-бал (`ScoreBar`), скринінг, статус, AI-підсумок. |
| `components/StatusTabs.vue` | «All · 42 / Pending / Invited / Shortlisted / Rejected». |
| `components/BulkActionBar.vue` | «3 selected: Invite / Shortlist / Reject». |
| `components/CandidateDrawer.vue` | Контейнер Drawer, завантаження деталей, skeleton. |
| `components/candidate/CandidateHeader.vue` | Аватар, email, статуси, ранг, дії. |
| `components/candidate/ResumeAnalysisCard.vue` | Загальна оцінка, критерії, strengths / follow-ups (`AiSummary`). |
| `components/candidate/ResumeFileRow.vue` | Файл резюме: preview/download. |
| `components/candidate/ScreeningAnswers.vue` | Відповіді по питаннях (відео-плеєр / текст). |
| `components/candidate/TranscriptBlock.vue` | Транскрипція з розгортанням. |
| `components/candidate/ApplicationTimeline.vue` | Хронологія. |
| `composables/useRejectCandidate.ts` | `ConfirmDialog` «Reject candidate?». |

**Vacancy-частина**

| Файл | Призначення |
|---|---|
| `features/vacancies/components/VacancyDetailHeader.vue` | Заголовок, статуси, метадані, «Copy link», «Edit». |
| `features/vacancies/components/VacancyTabs.vue` | Overview / Candidates / Screening questions / Settings (роутовані вкладки). |
| `features/vacancies/components/VacancyOverviewTab.vue` | Огляд вакансії. |
| `features/vacancies/components/VacancyQuestionsTab.vue` | Read-only питання скринінгу. |
| `features/vacancies/composables/useRetryAiSelection.ts` | «Repeat selection» при AI-помилці. |

**Page:** `pages/private/VacancyDetailPage.vue` (вкладка Candidates + drawer).

## Крок 5. Публічна вакансія і подання заявки

Залежить від серверного пункту 4.

| Файл | Призначення |
|---|---|
| `features/vacancies/api/public-vacancy.api.ts` | `getPublicVacancy(publicId)` без JWT. |
| `features/vacancies/api/public-vacancy.queries.ts` | `usePublicVacancyQuery`. |
| `features/vacancies/components/public/PublicVacancyView.vue` | Опис, списки, зарплата, дедлайн, компанія. |
| `features/vacancies/components/public/VacancyClosedBanner.vue` | Стан «вакансію закрито». |
| `features/applications/api/apply.api.ts` | `POST /flow/resume-get-presigned-post-url` + прямий upload на S3. |
| `features/applications/composables/useResumeUpload.ts` | Валідація файлу (PDF, розмір), прогрес, стани idle/selected/uploading/success/error. |
| `features/applications/composables/useApplyForm.ts` | Email + файл, схема, submit. |
| `features/applications/components/ApplyForm.vue` | Форма з дизайну. |
| `features/applications/components/ResumeDropzone.vue` | Вибір/перетягування PDF. |
| `features/applications/components/ApplySuccess.vue` | «Thanks for applying!». |
| `shared/utils/s3-upload.ts` | Хелпер для presigned POST (повторно використає крок 7 для відео). |
| `pages/public/PublicVacancyPage.vue` | Сторінка вакансії + CTA Apply / Ask assistant. |
| `pages/public/ApplyPage.vue` | Подання заявки. |

## Крок 6. AI-асистент (чат)

Нова залежність: `socket.io-client`.

| Файл | Призначення |
|---|---|
| `features/ai-chat/types/chat.ts` | `ChatMessage`, `ChatStatus`. |
| `features/ai-chat/api/chat.socket.ts` | Створення сокета, події `chat_start`, `msg_event`, `bot_typing`, `bot_message`, `chat_error`. |
| `features/ai-chat/composables/useAiChat.ts` | Життєвий цикл з'єднання, список повідомлень, typing, помилки, відправка. |
| `features/ai-chat/components/ChatWindow.vue` | Контейнер з автоскролом. |
| `features/ai-chat/components/ChatMessageBubble.vue` | Бабл користувача/бота. |
| `features/ai-chat/components/ChatInput.vue` | Поле вводу + відправка по Enter. |
| `features/ai-chat/components/TypingIndicator.vue` | «Assistant is typing…». |
| `features/ai-chat/components/ChatGreeting.vue` | Привітання + підказки питань. |
| `features/ai-chat/components/ChatErrorBanner.vue` | Помилка та off-topic стан з retry. |
| `pages/public/ChatPage.vue` | `CandidateLayout` + `ChatWindow`. |

## Крок 7. Скринінг кандидата (відео/текст) і фінальні стани

Залежить від серверного пункту 3 (питання за токеном).

| Файл | Призначення |
|---|---|
| `features/screening/types/screening.ts` | `ScreeningSession`, `ScreeningQuestion`, `AnswerState`, `TokenError`. |
| `features/screening/api/screening.api.ts` | `getScreening(token)`, `getVideoUploadUrl`, `saveTextAnswer`. |
| `features/screening/api/screening.queries.ts` | Query/mutation-хуки. |
| `features/screening/composables/useScreeningFlow.ts` | Поточне питання, перехід далі, прогрес «2 of 4», завершення. |
| `features/screening/composables/useVideoRecorder.ts` | `getUserMedia` + `MediaRecorder`: стани idle/denied/recording/review, ліміт тривалості, перезапис. |
| `features/screening/composables/useVideoUpload.ts` | Presigned URL + upload із прогресом. |
| `features/screening/composables/useCountdown.ts` | Таймер запису. |
| `features/screening/composables/useTokenState.ts` | Мапінг помилок сервера в стани: invalid/expired, already completed, under review, rejected. |
| `features/screening/components/ScreeningProgress.vue` | Степер/прогрес. |
| `features/screening/components/VideoAnswer.vue` | Контейнер відео-питання (оркеструє стани). |
| `features/screening/components/CameraPreview.vue` | Прев'ю камери/відтворення запису. |
| `features/screening/components/CameraDeniedState.vue` | Інструкція при забороні доступу. |
| `features/screening/components/RecordControls.vue` | Start / Stop / Retake / Submit. |
| `features/screening/components/TextAnswer.vue` | Текстове поле з лічильником (до 5000). |
| `features/screening/components/UploadingState.vue` | «Sending your answer…». |
| `features/screening/components/end/ScreeningDone.vue` | Фінал. |
| `features/screening/components/end/TokenInvalid.vue` | Посилання недійсне/прострочене. |
| `features/screening/components/end/AlreadyCompleted.vue` | Скринінг уже пройдено. |
| `features/screening/components/end/UnderReview.vue` | Заявка в розгляді. |
| `features/screening/components/end/PoliteRejection.vue` | Ввічлива відмова. |
| `pages/public/ScreeningPage.vue` | Оркестрація питань/станів токена. |
| `pages/public/ScreeningEndPage.vue` | Фінальні екрани (за станом). |

## Крок 8. Лендінг і фініш

| Файл | Призначення |
|---|---|
| `features/landing/components/HeroSection.vue` | Заголовок, опис, CTA. |
| `features/landing/components/HeroPreviewCard.vue` | Демо-картка з рейтингом (використовує `ScoreBar`, `AiStatus`, `AiSummary`). |
| `features/landing/components/HowItWorks.vue` | Три кроки (Resume → Screening → Ranking). |
| `pages/public/LandingPage.vue` | Збирає секції в `PublicLayout`. |
| `shared/ui/toast/useToastNotify.ts` | Типізована обгортка `success/error/info` над `useToast` (використовується у всіх мутаціях). |
| Фінальний прохід | Скелетони/порожні/помилкові стани на кожній сторінці, a11y (фокус, aria, клавіатура), перевірка dark mode, мобільні брейкпоінти (публічні сторінки обов'язково), `lint` + `type-check`. |

---

## Порядок виконання й коміти

Кожен крок — окрема гілка/PR (формат як у історії: `feat: …`).

1. Крок 0 → 2. Крок 1 → 3. Крок 2 → 4. Крок 3 → 5. Крок 5 → 6. Крок 6 → 7. Крок 4 (коли готовий API) → 8. Крок 7 → 9. Крок 8.

Публічні кроки (5–7) ідуть перед кроком 4, бо не блокуються бекендом так сильно, а кандидатський флоу — ядро продукту.

## Рішення, які потрібні від тебе

1. **Форми:** `@primevue/forms` + `zod` (рекомендую, нативно до PrimeVue) чи `vee-validate` + `zod`.
2. **Мови інтерфейсу:** дизайн українською, але за правилом проєкту лейбли в коді англійські — залишаємо англійською без i18n (рекомендую) чи одразу вводимо `vue-i18n` з uk/en.
3. **Бекенд для кроків 4 і 7:** чекаємо ендпоінти чи йдемо на моках із типами, що відповідають очікуваному контракту.
4. **Префікс приватних роутів:** `/app/*` (як у плані) чи без префікса (`/vacancies`), тоді публічна вакансія стає `/v/:publicId`.
