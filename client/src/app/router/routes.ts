import type { RouteRecordRaw } from 'vue-router'

const devRoutes: RouteRecordRaw[] = import.meta.env.DEV
  ? [{ path: '/dev/ui', name: 'dev-ui', component: () => import('@/pages/dev/UiKitPage.vue') }]
  : []

export const routes: RouteRecordRaw[] = [
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    meta: { guestOnly: true },
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
        component: () => import('@/pages/private/VacanciesPage.vue'),
      },
      {
        path: 'vacancies/new',
        name: 'vacancy-new',
        component: () => import('@/pages/private/VacancyFormPage.vue'),
      },
      {
        path: 'vacancies/:id(\\d+)',
        name: 'vacancy-detail',
        component: () => import('@/pages/private/VacancyDetailPage.vue'),
      },
      {
        path: 'vacancies/:id(\\d+)/edit',
        name: 'vacancy-edit',
        component: () => import('@/pages/private/VacancyFormPage.vue'),
      },
      {
        path: 'company',
        name: 'company',
        meta: { roles: ['company_admin'] },
        component: () => import('@/pages/private/CompanyPage.vue'),
      },
      {
        path: 'team',
        name: 'team',
        meta: { roles: ['company_admin'] },
        component: () => import('@/pages/private/TeamPage.vue'),
      },
    ],
  },

  {
    path: '/',
    component: () => import('@/layouts/PublicLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('@/pages/public/LandingPage.vue') },
      {
        path: 'vacancies/:vacancyId(\\d+)',
        name: 'public-vacancy',
        component: () => import('@/pages/public/PublicVacancyPage.vue'),
      },
      {
        path: 'vacancies/:vacancyId(\\d+)/apply',
        name: 'apply',
        component: () => import('@/pages/public/ApplyPage.vue'),
      },
      {
        path: 'forbidden',
        name: 'forbidden',
        component: () => import('@/pages/public/ForbiddenPage.vue'),
      },
      ...devRoutes,
      {
        path: ':pathMatch(.*)*',
        name: 'not-found',
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
        component: () => import('@/pages/public/ChatPage.vue'),
      },
      {
        path: 'screening/:token',
        name: 'screening',
        component: () => import('@/pages/public/ScreeningPage.vue'),
      },
      {
        path: 'screening/:token/done',
        name: 'screening-done',
        component: () => import('@/pages/public/ScreeningEndPage.vue'),
      },
    ],
  },
]
