import router from "@/router";


// Initial State of the store
const state = () => ({
    // loggedIn: localStorage.getItem("jwt_token") ? true : false,
    loggedIn: false,
    // log: 
    role: "",
    name: "",
    loading: true
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
    }
}

// Mutations
const mutations = {
    login(state, data) {
        state.loggedIn = true;
        state.name = data.name;
        state.role = data.role;
        state.loading = false;
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
    }


}

const userStore = {
    state,
    getters,
    mutations,
    actions
};

export default userStore;
