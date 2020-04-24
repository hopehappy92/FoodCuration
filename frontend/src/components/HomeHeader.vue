<template>
  <div id="home_form">
    <div id="home_header">
      <div id="home_header_header">
        <div id="home_header_header_logo">
          <img id="home_header_header_logo_img" src="../../public/images/logo.png" alt="Logo">
        </div>
        <div id="home_header_header_tab">
          <div v-if="islogined == false">
            <ul class="nav_inner_right">
              <li>
                <login>
                  <button slot="click" class="nav_menu">로그인</button>
                </login>
              </li>
              <li>
                <button class="nav_menu" @click="goRegi()">회원가입</button>
              </li>
            </ul>
          </div>
          <div v-else>
            <ul class="nav_inner_right">
              <li>
                <button class="nav_menu" @click="dologout()">로그아웃</button>
              </li>
              <li>
                <button class="nav_menu" @click="goMypage()">마이페이지</button>
              </li>
              <li v-if="isStaff == true">
                <button class="nav_menu" @click="goAdmin()">관리자페이지</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div id="home_header_search">
        <form id="home_header_search_form" action="/search">
          <div id="home_header_search_input_before" />
          <input
            id="home_header_search_input"
            v-model="storeName"
            type="text"
            placeholder="식당명"
            @keyup.prevent="enterKey(storeName)"
          >
          <button id="home_header_search_btn" @click.prevent="goSearchPage(storeName)">
            <b>검색</b>
          </button>
          <div id="home_header_search_input_after" />
        </form>
      </div>
    </div>
    <div id="home_body">
      <div>asfdf</div>
    </div>
  </div>
</template>

<script>
import Login from "../components/Login";
import { mapState, mapActions, mapMutations } from "vuex";
import router from "../router";

export default {
  components: {
    Login
  },
  data() {
    return {
      storeName: "",
      // isStaff: false
    };
  },
  computed: {
    ...mapState({
      islogined: state => state.data.isloggined,
      isStaff: state => state.data.isStaff
    })
  },
  mounted() {
    this.checkLogin();
    // console.log(this.isStaff)
  },
  methods: {
    ...mapActions("data", ["checkLogin"]),
    ...mapActions("data", ["logout"]),
    ...mapMutations("data", ["searchFromNav"]),
    goRegi() {
      router.push("/register");
    },
    goMypage() {
      const location = "/mypage/" + localStorage.getItem("pk");
      router.push(location);
    },
    dologout() {
      this.logout();
    },
    goSearchPage(storeName) {
      this.searchFromNav(storeName);
      router.push("/search");
    },
    enterKey(storeName) {
      if (window.event.keyCode == 13) {
        this.goSearchPage(storeName);
      }
    },
    goAdmin() {
      router.push("/adminpage")
    }
  },
  
};
</script>

<style scoped>
#home_header {
  width: 100%;
  background-image: url("../../public/images/home_bg.jpg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 250px;
  position: absolute;
  top: 0;
  /* text-align: center; */
}
#home_header_header {
  width: 100%;
  display: flex;
  color: white;
  padding: 20px;
}
#home_header_header_logo {
  flex: 1;
}
#home_header_header_logo_img {
  width: 150px;
  position: absolute;
  top: 0px;
  left: 0px;
}
#home_header_search {
  width: 100%;
  text-align: center;
  /* margin-top: 20px; */
}
#home_header_search_input_before {
  display: inline-block;
  background-color: white;
  width: 30px;
  height: 50px;
  border-top-left-radius: 50px;
  border-bottom-left-radius: 50px;
  transform: translateY(40%);
}
#home_header_search_input {
  background-color: white;
  line-height: 50px;
  width: 20vw;
  font-size: 20px;
  transform: translateY(4%);
}
#home_header_search_btn {
  background-color: white;
  height: 50px;
  width: 70px;
  font-size: 20px;
  transform: translateY(4%);
}
#home_header_search_input_after {
  display: inline-block;
  background-color: white;
  width: 30px;
  height: 50px;
  transform: translateY(40%);
  border-top-right-radius: 50px;
  border-bottom-right-radius: 50px;
}
.nav_inner_right {
  display: flex;
  list-style: none;
  padding-right: 24px;
}
.nav_inner_right > li {
  display: flex;
  align-items: center;
  padding: 12px 8px;
}
.nav_inner_right > li > div {
  display: flex;
  align-items: center;
}
.nav_inner_right > li > div > div > button {
  color: white;
  text-decoration-style: none;
}
.nav_inner_right > li > button {
  color: white;
}

@media screen and (max-width: 600px) {
  #home_header {
    height: 100px;
  }
  #home_header_search {
    margin-top: 10px;
  }
  #home_header_search_input_before {
    height: 40px;
  }
  #home_header_search_input {
    line-height: 40px;
    width: 45vw;
    font-size: 17px;
  }
  #home_header_search_btn {
    height: 40px;
    width: 60px;
    font-size: 17px;
    transform: translateY(6%);
  }
  #home_header_search_input_after {
    height: 40px;
  }
  .nav_inner_right {
    padding-right: 0px;
  }
}
</style>