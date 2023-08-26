import { createStore } from 'vuex';
import userStore from "./modules/userStore";
import postStore from './modules/postStore';

export default createStore({
    modules: {
        userStore: userStore,
        postStore: postStore,
    }
})
