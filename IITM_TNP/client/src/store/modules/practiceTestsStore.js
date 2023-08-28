import axios from 'axios';
import { BASE_URL_PRACTICE_TESTS} from '../../utils/constants';


const state = {
  practice_tests: [],
};

const getters = {
  get_all_practice_tests(state){
    return state.practice_tests
  }
};

const mutations = {
  setPracticeTests(state, practice_tests) {
    state.practice_tests = practice_tests;
  },
};

const actions = {
  
  async fetchPracticeTests({ commit }) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    console.log(headers)
    try {
      const response = await axios.get(BASE_URL_PRACTICE_TESTS,{ headers });      
      commit('setPracticeTests',response.data.practice_tests );
    } catch (error) {
      console.error('Error fetching PracticeTests:', error);
    }
  },

  async addPracticeTest({dispatch},data){
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    
    try {
      await axios.post(BASE_URL_PRACTICE_TESTS,data,{ headers });
      dispatch("fetchPracticeTests");      
    } catch (error) {
      console.error('Error adding PracticeTest:', error);
    }
  },

async editPracticeTest({dispatch},data){
  const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    try {
      await axios.put(BASE_URL_PRACTICE_TESTS,data,{ headers });
      dispatch("fetchPracticeTests");      
    } catch (error) {
      console.error('Error editing PracticeTest:', error);
      alert(error.response.data.msg)
    }
},

async deletePracticeTest({dispatch},data){
  const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    try {
      await axios.delete(`${BASE_URL_PRACTICE_TESTS}/${data}`,{ headers });
      dispatch("fetchPracticeTests");      
    } catch (error) {
      console.error('Error deleting PracticeTest:', error);
      alert(error.response.data.msg)
    }
  }
};

const practice_testStore = {
  state,
  getters,
  mutations,
  actions
};


export default practice_testStore
