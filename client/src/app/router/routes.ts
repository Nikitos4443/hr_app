import type { RouteRecordRaw } from 'vue-router'

const devRoutes: RouteRecordRaw[] = import.meta.env.DEV
  ? [
      {
        path: '/dev/ui',
        name: 'dev-ui',
        meta: { title: 'UI kit' },
        component: () => import('@/pages/dev/UiKitPage.vue'),
      },
    ]
  : []

export const routes: RouteRecordRaw[] = [
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    meta: { guestOnly: true, title: 'Sign in' },
    children: [{ path: '', name: 'auth', component: () => import('@/pages/public/AuthPage.vue') }],
  },

  {
    path: '/app',
    component: () => import('@/layouts/AppShellLayout.vue'),
    meta: { requiresAuth: true },
    redirect: { name: 'vacancies' },
    children: [
      {
        path: 'vacancies',
        name: 'vacancies',
        meta: { title: 'Vacancies' },
        component: () => import('@/pages/private/VacanciesPage.vue'),
      },
      {
        path: 'vacancies/new',
        name: 'vacancy-new',
        meta: { title: 'New vacancy' },
        component: () => import('@/pages/private/VacancyFormPage.vue'),
      },
      {
        path: 'vacancies/:id(\\d+)',
        name: 'vacancy-detail',
        meta: { title: 'Vacancy' },
        component: () => import('@/pages/private/VacancyDetailPage.vue'),
      },
      {
        path: 'vacancies/:id(\\d+)/edit',
        name: 'vacancy-edit',
        meta: { title: 'Edit vacancy' },
        component: () => import('@/pages/private/VacancyFormPage.vue'),
      },
      {
        path: 'company',
        name: 'company',
        meta: { roles: ['company_admin'], title: 'Company' },
        component: () => import('@/pages/private/CompanyPage.vue'),
      },
      {
        path: 'team',
        name: 'team',
        meta: { roles: ['company_admin'], title: 'Team' },
        component: () => import('@/pages/private/TeamPage.vue'),
      },
    ],
  },

  {
    path: '/',
    component: () => import('@/layouts/PublicLayout.vue'),
    children: [
      {
        path: '',
        name: 'home',
        meta: { title: '' },
        component: () => import('@/pages/public/LandingPage.vue'),
      },
      {
        path: 'vacancies/:vacancyId(\\d+)',
        name: 'public-vacancy',
        meta: { title: 'Vacancy' },
        component: () => import('@/pages/public/PublicVacancyPage.vue'),
      },
      {
        path: 'vacancies/:vacancyId(\\d+)/apply',
        name: 'apply',
        meta: { title: 'Apply' },
        component: () => import('@/pages/public/ApplyPage.vue'),
      },
      {
        path: 'forbidden',
        name: 'forbidden',
        meta: { title: 'Access denied' },
        component: () => import('@/pages/public/ForbiddenPage.vue'),
      },
      ...devRoutes,
      {
        path: ':pathMatch(.*)*',
        name: 'not-found',
        meta: { title: 'Page not found' },
        component: () => import('@/pages/public/NotFoundPage.vue'),
      },
    ],
  },

  {
    path: '/',
    component: () => import('@/layouts/CandidateLayout.vue'),
    children: [
      {
        path: 'vacancies/:vacancyId(\\d+)/chat',
        name: 'chat',
        meta: { title: 'Chat' },
        component: () => import('@/pages/public/ChatPage.vue'),
      },
      {
        path: 'screening/:token',
        name: 'screening',
        meta: { title: 'Screening' },
        component: () => import('@/pages/public/ScreeningPage.vue'),
      },
      {
        path: 'screening/:token/done',
        name: 'screening-done',
        meta: { title: 'Screening complete' },
        component: () => import('@/pages/public/ScreeningEndPage.vue'),
      },
    ],
  },
]
