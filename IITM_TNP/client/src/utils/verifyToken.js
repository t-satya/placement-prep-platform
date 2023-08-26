// import axios from "axios";
// import { VERIFY_TOKEN_URL_BACKEND } from "./constants";
// import { useStore } from 'vuex';

// const store = useStore();


// export default function verifyToken() {
//     const token = localStorage.getItem("jwt_token");

//     if (token) {
//         const options = {
//             headers: {
//                 "Authorization": "Bearer " + token
//             }
//         }
//         axios.get(VERIFY_TOKEN_URL_BACKEND, options).then((res) => {
//             console.log(res)
//             store.dispatch("loginUser", { data: { name: res.data.name, role: res.data.role } })
//             return true;
//         })
//             .catch((err) => {
//                 return false;
//             })
//         return false;
//     }
//     else {
//         return false;
//     }

// }