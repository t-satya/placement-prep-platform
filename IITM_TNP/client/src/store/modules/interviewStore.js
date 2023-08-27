import axios from 'axios';
import { BASE_URL_INTERVIEWS} from '../../utils/constants';
import { useStore } from "vuex"


const store = useStore()
const state = {
  interviews: [],
};

const getters = {
  get_all_interviews(state){
    return state.interviews
  }
};

const mutations = {
  setInterviews(state, interviews) {
    state.interviews = interviews;
  },
};

const actions = {
  
  async fetchInterviews({ commit }) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    console.log(headers)
    try {
      const response = await axios.get(BASE_URL_INTERVIEWS,{ headers });      
      commit('setInterviews',response.data.interviews );
    } catch (error) {
      console.error('Error fetching Interviews:', error);
    }
  },

  async addInterview({dispatch},data){
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    
    try {
      await axios.post(BASE_URL_INTERVIEWS,data,{ headers });
      dispatch("fetchInterviews");      
    } catch (error) {
      console.error('Error adding Interview:', error);
    }
  },

async editInterview({dispatch},data){
  const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    try {
      await axios.put(BASE_URL_INTERVIEWS,data,{ headers });
      dispatch("fetchInterviews");      
    } catch (error) {
      console.error('Error editing Interview:', error);
      alert(error.response.data.msg)
    }
},

async deleteInterview({dispatch},data){
  const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    try {
      await axios.delete(`${BASE_URL_INTERVIEWS}/${data}`,{ headers });
      dispatch("fetchInterviews");      
    } catch (error) {
      console.error('Error deleting Interview:', error);
      alert(error.response.data.msg)
    }
  }
};

const interviewStore = {
  state,
  getters,
  mutations,
  actions
};


export default interviewStore
