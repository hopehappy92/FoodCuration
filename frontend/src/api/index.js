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
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.post(`${apiUrl}/store_reviews`, params, {headers})
  },
  setUserCategory(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.post(`${apiUrl}/set_user_category`, params, {
      headers
    })
  },
  getUserBasedRecommand() {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.get(`${apiUrl}/user_based_cf`, {
      headers
    })
  },
  getTrendChartData() {
    return http.get(`${apiUrl}/trend_by_tob`)
  },
  getChainChartData() {
    return http.get(`${apiUrl}/compare_with_chain`)
  },
  getLocationChartData() {
    return http.get(`${apiUrl}/district_by_age_time`)
  },
  getRecommendStore(params) {
    return http.get(`${apiUrl}/recommend_by_store_id/${params}`)
  },
  getGenerationChartData(params) {
    return http.get(`${apiUrl}/generation_consumption`)
  },
  adminDeleteStore(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.delete(`${apiUrl}/stores/${params}`, {headers})
  },
  adminDeleteReview(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.delete(`${apiUrl}/store_reviews/${params}`, {headers})
  },
  getAllRecommand(params) {
    return http.post(`${apiUrl}/recommend_by_current_location`, params)
  },
  tokencheck(params) {
    return http.post(`${apiUrl}/token/verify/`, params)
  },
  getUsers(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.get(`${apiUrl}/all_user`, {headers})
  },
  deleteUser(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.put(`${apiUrl}/delete_user`, params, {headers})
  },
  changeUserStaff(params) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    return http.put(`${apiUrl}/change_user`, params, {headers})
  }
}