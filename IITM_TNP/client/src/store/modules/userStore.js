import router from "@/router";
// import verifyToken from "../../utils/verifyToken";


// Initial State of the store
const state = () => ({
    // loggedIn: localStorage.getItem("jwt_token") ? true : false,
    loggedIn: false,
    // log: 
    role: "student",
    name: "",
    loading: true,
    user_id:""
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
        if (data.access_token) {
            localStorage.setItem("jwt_token", data.access_token);
        }
    },
    logout(state) {
        state.loggedIn = false;
    },
    updateRole(state, newRole) {
        state.role = newRole;
    },
    setLoading(state, data) {
        state.loading = data.loading;
    }

}

// Actions
const actions = {
    logoutUser({ commit }) {
        commit("logout");
        router.push('/');
    },
    loginUser({ commit }, { data }) {
        console.log(data);
        commit('login', data);
    },
    setLoadingStatus({ commit }, { data }) {
        commit('setLoading', data)
    }


}

const userStore = {
    state,
    getters,
    mutations,
    actions
};

export default userStore;
