import axios from 'axios';
import { useStore } from 'vuex';
import { BASE_URL_POSTS } from '../../utils/constants';
import { BASE_URL_REPLIES } from '../../utils/constants';

const state = {
  posts: [],
};

const getters = {
  get_all_posts(state){
    return state.posts
  }
};

const mutations = {
  setPosts(state, posts) {
    state.posts = posts;
  },
};

const actions = {
  
  async fetchPosts({ commit }) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    console.log(headers)
    try {
      const response = await axios.get(BASE_URL_POSTS,{ headers });
      const sortedPosts = response.data.all_posts.map(post => {
        if (post.replies.length > 0) {
          // Sort replies by timestamp
          post.replies.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  
          // Use the latest reply's timestamp
          post.timestamp = post.replies[0].timestamp;
        }
  
        return post;
      });
  
      // Sort posts by the new timestamp
      sortedPosts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  
    commit('setPosts', sortedPosts);
    console.log(sortedPosts)
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  },

  async createPost({ dispatch }, payload) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`,
    "Content-Type":"application/json"
  }

    try {
      await axios.post(`${BASE_URL_POSTS}`,payload,{ headers }); 
      dispatch('fetchPosts');
    } catch (error) {
      console.error('Error creating post:', error);
    }
  },
  async editPost({ dispatch }, data) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`,
                    "Content-Type":"application/json"}
    const payload={"description":data.postData,"tags":data.tags}
    try {
      await axios.put(`${BASE_URL_POSTS}/${data.postid}`,payload,{ headers }); 
      dispatch('fetchPosts'); 
    } catch (error) {
      console.error('Error editing post:', error);
    }
  },
  async deletePost({ dispatch }, postid) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`}
    try {
      await axios.delete(`${BASE_URL_POSTS}/${postid}`,{headers}); 
      dispatch('fetchPosts'); 
    } catch (error) {
      console.error('Error deleting post:', error);
    }
  },
  async createReply({ dispatch }, payload) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`,
    "Content-Type":"application/json"
  }

    try {
      await axios.post(`${BASE_URL_REPLIES}`,payload,{ headers }); 
      dispatch('fetchPosts');
    } catch (error) {
      console.error('Error creating reply:', error);
    }
  },
  async editReply({ dispatch }, data) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`,
    "Content-Type":"application/json"
  }
  const payload = {"description":data.description}
    try {
      await axios.put(`${BASE_URL_REPLIES}/${data.reply_id}`,payload,{ headers }); 
      dispatch('fetchPosts');
    } catch (error) {
      console.error('Error editing reply:', error);
    }
  },
  async deleteReply({ dispatch }, data) {
    const token = localStorage.getItem("jwt_token")
    const headers = {Authorization: `Bearer ${token}`
  }
    try {
      await axios.delete(`${BASE_URL_REPLIES}/${data}`,{ headers }); 
      dispatch('fetchPosts');
    } catch (error) {
      console.error('Error deleting reply:', error);
    }
  },
};

const postStore = {
  state,
  getters,
  mutations,
  actions
};


export default postStore
