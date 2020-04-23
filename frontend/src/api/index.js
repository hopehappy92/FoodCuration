// import axios from "axios";
import http from "./http"

const apiUrl = "/api";
const regiUrl = "/rest-auth";

export default {
  getStores(params) {
    return http.get(`${apiUrl}/stores`, {
      params
    });
  },
  getUserReview(params) {
    // console.log("api index ", params.user_id)
    return http.get(`${apiUrl}/user_reviews`, {
      params
    });
  },
  register(params) {
    // console.log(params)
    return http.post(`${apiUrl}${regiUrl}/registration/`, params)
  },
  login(params) {
    return http.post(`${apiUrl}/login/`, params)
  },
  reviewDelete(params) {
    return http.delete(`${apiUrl}/user_reviews/${params}`)
  },
  reviewUpdate(params) {
    // console.log(params)
    return http.put(`${apiUrl}/user_reviews/${params["id"]}`, params)
  },
  getStoresByLocation(params) {
    return http.post(`${apiUrl}/search_store`, params)
  },
  editReview(params) {
    return http.put(`${apiUrl}/store_reviews/${params.id}`, params)
  },
  getStoreReview(params) {
    return http.get(`${apiUrl}/get_store_reviews_by_store_id/${params}`, params)
  },
  writeReview(params) {
    return http.post(`http://i02d106.p.ssafy.io:8765/api/store_reviews`, params)
  },
  setUserCategory(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.post(`${apiUrl}/set_user_category`, params, {headers})
  },
  getUserBasedRecommand() {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.get(`${apiUrl}/user_based_cf`, {headers})
  },
  getTrendChartData() {
    return  http.get(`${apiUrl}/trend_by_tob`)
  },
  getChainChartData() {
    return http.get(`${apiUrl}/compare_with_chain`)
  }
};