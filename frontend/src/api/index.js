// import axios from "axios";
import https from "./http"

const apiUrl = "/api";
const regiUrl = "/rest-auth";

export default {
  getStores(params) {
    return https.get(`${apiUrl}/stores`, {
      params
    });
  },
  getUserReview(params) {
    // console.log("api index ", params.user_id)
    return https.get(`${apiUrl}/user_reviews`, {
      params
    });
  },
  register(params) {
    // console.log(params)
    return https.post(`${apiUrl}${regiUrl}/registration/`, params)
  },
  login(params) {
    return https.post(`${apiUrl}/login/`, params)
  },
  reviewDelete(params) {
    return https.delete(`${apiUrl}/user_reviews/${params}`)
  },
  reviewUpdate(params) {
    // console.log(params)
    return https.put(`${apiUrl}/user_reviews/${params["id"]}`, params)
  },
  getStoresByLocation(params) {
    return https.post(`${apiUrl}/search_store`, params)
  },
  editReview(params) {
    return https.put(`${apiUrl}/store_reviews/${params.id}`, params)
  },
  getStoreReview(params) {
    return https.get(`${apiUrl}/get_store_reviews_by_store_id/${params}`, params)
  },
  writeReview(params) {
    return https.post(`https://i02d106.p.ssafy.io:8765/api/store_reviews`, params)
  },
  setUserCategory(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return https.post(`${apiUrl}/set_user_category`, params, {headers})
  },
  getUserBasedRecommand() {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return https.get(`${apiUrl}/user_based_cf`, {headers})
  }
};