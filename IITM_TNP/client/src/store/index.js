import { createStore } from 'vuex';
import userStore from "./modules/userStore";
import postStore from './modules/postStore';
import interviewStore from "./modules/interviewStore"

export default createStore({
    modules: {
        userStore: userStore,
        postStore: postStore,
        interviewStore: interviewStore
    }
})
