import { createStore } from 'vuex';
import userStore from "./modules/userStore";
import postStore from './modules/postStore';
import interviewStore from "./modules/interviewStore"
import questionStore from './modules/questionStore';
import practice_testStore from './modules/practiceTestsStore';

export default createStore({
    modules: {
        userStore: userStore,
        postStore: postStore,
        interviewStore: interviewStore,
        questionStore: questionStore,
        practice_testStore: practice_testStore
    }
})
