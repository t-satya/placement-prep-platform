import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue';
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import PostView from "../views/PostView.vue";
import QuestionsView from "../views/Admin/QuestionsView.vue";
import InterviewsView from "../views/InterviewsView.vue";
import PracticeTestsView from "../views/Admin/PracticeTestsView.vue"
import StudentPracticeTestView from "../views/PracticeTestsStudentView.vue"
import TestView from "../views/TestView.vue"
import StudentTestView from "../views/StudentTestView.vue"
import AdminRegister from "../views/Admin/AdminRegisterView.vue"
import store from "../store";
import axios from 'axios';
import { VERIFY_TOKEN_URL_BACKEND } from "../utils/constants.js";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/posts',
      name: 'posts',
      component: PostView,
      meta: {
        isRequiredAuth: true,
      }
    },
    {
      path:"/admin/practice_tests",
      name:'practice_tests',
      component: PracticeTestsView,
      meta:{
        isRequiredAuth: true,
        admissibleRoles: ["admin", "super admin"]
      }
    },
    {
      path:"/practice",
      name:'student_practice_tests',
      component:StudentPracticeTestView ,
      meta:{
        isRequiredAuth: true,
      }
    },
    {
      path: '/admin/questions',
      name: 'admin_questions',
      component: QuestionsView,
      meta: {
        isRequiredAuth: true,
        admissibleRoles: ["admin", "super admin"]
      }
    },
    {
      path: '/admin/register',
      name: 'admin_register',
      component: AdminRegister,
      meta: {
        isRequiredAuth: true,
        admissibleRoles: ["super admin"]
      }
    },
    {
      path:"/interview",
      name: "interview",
      component: InterviewsView,
      meta: {
        isRequiredAuth: true,
      }
    },
    {
      path:"/test/:id",
      props: true,
      name: "testview",
      component: TestView,
      meta: {
        isRequiredAuth: true,
      }
    },
    {
      path:"/student_test/:id",
      props: true,
      name: "studenttestview",
      component: StudentTestView,
      meta: {
        isRequiredAuth: true,
      }
    }
  ]
})



router.beforeEach((to, from, next) => {
  const isRequiredAuth = to?.meta?.isRequiredAuth
  const admissibleRoles = to?.meta?.admissibleRoles

  const token = localStorage.getItem("jwt_token");
  if (isRequiredAuth) {
    if (token) {
      const options = {
        headers: {
          "Authorization": "Bearer " + token
        }
      }
      axios.get(VERIFY_TOKEN_URL_BACKEND, options).then((res) => {
        store.dispatch("loginUser", { data: { name: res.data.name, role: res.data.role } });

        if (admissibleRoles) {
          if (admissibleRoles.length != 0 && admissibleRoles.includes(res.data.role)) {
            next();
          }
          else {
            store.dispatch("logoutUser")
            next("/login?error_msg=Unauthorised");
          }
        }
        else next();
      })
        .catch((err) => {
          console.log(err)
          store.dispatch("setLoadingStatus", { data: { loading: false } })
          next("/login?error_msg=Please login");
        })
    }
    else {
      store.dispatch("setLoadingStatus", { data: { loading: false } })
      next("/login?error_msg=Please login");
    }
  }
  else next();
})

export default router
