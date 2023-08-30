import router from "@/router";
import { BASE_URL_USER_DATA } from "../../utils/constants.js";
import axios from 'axios';
import { useStore } from "vuex"

const store = useStore()

// Initial State of the store
const state = () => ({
    // loggedIn: localStorage.getItem("jwt_token") ? true : false,
    loggedIn: false,
    // log: 
    role: "",
    name: "",
    loading: true,
    user_id:"",
    user_data:{}
})

// Getters
const getters = {
    jwt_token(state) {
        if (state.loggedIn === true) {
            return localStorage.getItem("jwt_token");
        } else {
            return null;
        }
    },
    get_login_status(state) {
        return state.loggedIn;
    },
    get_loading_status(state) {
        return state.loading;
    },
    get_role(state) {
        return state.role
    },
    get_user_id(state){
        return state.user_id
    },
    get_user_data(state){
        return state.user_data;
    }
}

// Mutations
const mutations = {
    login(state, data) {
        state.loggedIn = true;
        state.name = data.name;
        state.role = data.role;
        state.loading = false;
        state.user_id = data.user_id
        if (data.access_token) localStorage.setItem("jwt_token", data.access_token);

    },
    logout(state) {
        state.loggedIn = false;
        localStorage.removeItem("jwt_token");
    },
    updateRole(state, newRole) {
        state.role = newRole;
    },
    setLoading(state, data) {
        state.loading = data.loading;
    },
    setUserData(state,data){
        state.user_data=data;
    }

}

// Actions
const actions = {
    logoutUser({ commit }) {
        commit("logout");
        router.push('/');
    },
    loginUser({ commit }, { data }) {
        commit('login', data);
    },
    setLoadingStatus({ commit }, { data }) {
        commit('setLoading', data)
    },
    async fetchUserData({ commit },user_id) {
        const token = localStorage.getItem("jwt_token")
        const headers = {Authorization: `Bearer ${token}`}
        try {
          const response = await axios.get(`${BASE_URL_USER_DATA}/${user_id}`,{ headers });  
          commit('setUserData',response.data.user );
          console.log(response.data)
        } catch (error) {
          console.error('Error fetching UserData:', error);
        }
      },
      async updateUserData({ dispatch },data,user_id) {
        const token = localStorage.getItem("jwt_token")
        const headers = {Authorization: `Bearer ${token}`}
        try {
          const response = await axios.put(`${BASE_URL_USER_DATA}`,data,{ headers });  
        } catch (error) {
          console.error('Error updating UserData:', error);
        }
      },
    


}

const userStore = {
    state,
    getters,
    mutations,
    actions
};

export default userStore;
