import axios from "axios";

export default axios.create({
  // baseURL: "http://localhost:8080/",
<<<<<<< HEAD
//   baseURL: "http://127.0.0.1:8000/",
=======
  // baseURL: "http://127.0.0.1:8000/",
>>>>>>> b82f60ce587a3ba06967fff2f236ee56bfc4c420
  baseURL: "http://i02d106.p.ssafy.io:8765/",
  headers: {
    // "Content-type": "application/json",
    // "Authorization": "jwt " + localStorage.getItem("token")
  }
});