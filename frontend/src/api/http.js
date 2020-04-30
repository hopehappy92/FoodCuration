import axios from "axios";

export default axios.create({
  // baseURL: "http://localhost:8080/",
  baseURL: "http://127.0.0.1:8000/",
//   baseURL: "https://i02d106.p.ssafy.io:8765/",
  // headers: {
  // "Content-type": "application/json",
  // "Authorization": "jwt " + localStorage.getItem("token")
  // }
});