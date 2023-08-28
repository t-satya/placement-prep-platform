// Initial State of the store
const state = () => ({
    questions: []
})

const getters = {
    get_questions(state) {
        return state.questions;
    }
}

const mutations = {
    addQuestion(state, data) {
        state.questions = [...state.questions, ...data.question]
    },
    updateQuestion(state, data) {
        const index = data.index;
        const ques = data.question;

        console.log(index)

        state.questions[index] = ques;
    },
    deleteQuestion(state, data) {
        const indexToRemove = data.index;
        if (indexToRemove >= 0 && indexToRemove < state.questions.length) {
            state.questions.splice(indexToRemove, 1);
        }
    }
}

const actions = {
    addQuestionAction({ commit }, { data }) {
        commit('addQuestion', data);
    },
    deleteQuestionAction({ commit }, { data }) {
        commit('deleteQuestion', data);
    },
    updateQuestionAction({ commit }, { data }) {
        commit("updateQuestion", data);
    }
}


const questionStore = {
    state,
    getters,
    mutations,
    actions
};

export default questionStore;
