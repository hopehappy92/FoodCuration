<template>
  <div>
    <div id="tabs">
      <div id="tab1" class="tab" @click="showStores()">
        stores
      </div>
      <div id="tab2" class="tab" @click="showReviews()">
        reviews
      </div>
      <div id="tab3" class="tab" @click="showUsers()">
        users
      </div>
      <div class="tab" @click="goHome()">
        돌아가기
      </div>
    </div>
    <div>
      <div v-if="storeFlag == true">
        <table>
          <tr>
            <th>
              ID
            </th>
            <th>
              NAME
            </th>
            <th>
              BRANCH
            </th>
            <th>
              TEL
            </th>
            <th>
              ADDRESS
            </th>
            <th>
              DELETE
            </th>
          </tr>
          <tr v-for="(store, i) in stores" :key="i">
            <th>
              {{ store["id"] }}
            </th>
            <th>
              {{ store["name"] }}
            </th>
            <th>
              {{ store["branch"] }}
            </th>
            <th>
              {{ store["tel"] }}
            </th>
            <th>
              {{ store["address"] }}
            </th>
            <th>
              <div class="deleteBtn" @click="del('store', store['id'])">
                DELETE
              </div>
            </th>
          </tr>
        </table>
        <div class="loadMore" @click="storeLoadMore()">
          더보기
        </div>
      </div>
      
      <div v-if="reviewFlag == true">
        <!-- {{ reviews }} -->
        <table>
          <tr>
            <th>
              ID
            </th>
            <th>
              STORE_NAME
            </th>
            <th>
              SCORE
            </th>
            <th>
              CONTENT
            </th>
            <th>
              REG_TIME
            </th>
            <th>
              DELETE
            </th>
          </tr>
          <tr v-for="(review, i) in reviews" :key="i">
            <th>
              {{ review["id"] }}
            </th>
            <th>
              {{ review["store_name"] }}
            </th>
            <th>
              {{ review["score"] }}
            </th>
            <th>
              {{ review["content"] }}
            </th>
            <th>
              {{ review["reg_time"] }}
            </th>
            <th>
              <div class="deleteBtn" @click="del('review', review['id'])">
                DELETE
              </div>
            </th>
          </tr>
        </table>
        <div class="loadMore" @click="reviewLoadMore()">
          더보기
        </div>
      </div>

      <div v-if="userFlag == true">
        <table>
          <tr>
            <th>
              ID
            </th>
            <th>
              EMAIL
            </th>
            <th>
              AGE
            </th>
            <th>
              GENDER
            </th>
            <th>
              IS_STAFF
            </th>
            <th>
              REVIEW_COUNT
            </th>
          </tr>
          <tr v-for="(user, i) in addUser" :key="i">
            <th>
              {{ user["id"] }}
            </th>
            <th>
              {{ user["email"] }}
            </th>
            <th>
              {{ user["age"] }}
            </th>
            <th>
              {{ user["gender"] }}
            </th>
            <th>
              {{ user["is_staff"] }}
              <div style="display: inline;" class="chageBtn" @click="changeStaff(user['id'])">
                권한변경
              </div>
            </th>
            <th>
              {{ user["review_count"] }}
            </th>
            <th>
              <div class="deleteBtn" @click="del('user', user['id'])">
                DELETE
              </div>
            </th>
          </tr>
        </table>
        <div class="loadMore" @click="userLoadMore()">
          더보기
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex"
import router from "../router"

export default {
  data() {
    return {
      storeFlag: false,
      reviewFlag: false,
      userFlag: false,
      loading: true,
      storeName: "",
      addUser: [],
      userpage: 1,
    }
  },
  computed: {
    ...mapState({
      stores: state => state.data.storeSearchList,
      page: state => state.data.storeSearchPage,
      reviews: state => state.data.userReviewList,
      reviewpage: state => state. data.userReviewPage,
      users: state => state.data.userList
    })
  },
  watch: {
    users: function() {
      this.addUser = this.users.slice(0,10)
    }
  },
  methods: {
    goHome() {
      router.push("/")
    },
    del(type, pk) {
      const params = [
        type, pk
      ]
      this.adminDelete(params)
    },
    ...mapActions("data", ["getStores"]),
    ...mapActions("data", ["getUserReview"]),
    ...mapActions("data", ["adminDelete"]),
    ...mapActions("data", ["getUserData"]),
    ...mapActions("data", ["setUserStaff"]),
    async showUsers() {
      var target = document.getElementById("tab3").style
      var else1 = document.getElementById("tab1").style
      var else2 = document.getElementById("tab2").style
      if (target.color == "") {
        target.color = "white"
        target.backgroundColor = "black"
        else1.color = ""
        else1.backgroundColor = ""
        else2.color = ""
        else2.backgroundColor = ""
      } else {
        target.color = ""
        target.backgroundColor = ""
      }
      if ( this.userFlag == false) {
        this.userFlag = true
        this.reviewFlag = false
        this.storeFlag = false
      } else {
        this.userFlag = false
      }
      this.getUserData()
    },
    async showReviews() {
      var target = document.getElementById("tab2").style
      var else1 = document.getElementById("tab1").style
      var else2 = document.getElementById("tab3").style
      if (target.color == "") {
        target.color = "white"
        target.backgroundColor = "black"
        else1.color = ""
        else1.backgroundColor = ""
        else2.color = ""
        else2.backgroundColor = ""
      } else {
        target.color = ""
        target.backgroundColor = ""
      }
      if ( this.reviewFlag == false) {
        this.reviewFlag = true
        this.userFlag = false
        this.storeFlag = false
      } else {
        this.reviewFlag = false
      }
      const params = {
        page: 1,
        append: true,
        page_size: 10,
        reset: true,
      };
      await this.getUserReview(params);
    },
    async showStores() {
      var target = document.getElementById("tab1").style
      var else1 = document.getElementById("tab2").style
      var else2 = document.getElementById("tab3").style
      if (target.color == "") {
        target.color = "white"
        target.backgroundColor = "black"
        else1.color = ""
        else1.backgroundColor = ""
        else2.color = ""
        else2.backgroundColor = ""
      } else {
        target.color = ""
        target.backgroundColor = ""
      }
      if ( this.storeFlag == false) {
        this.storeFlag = true
        this.userFlag = false
        this.reviewFlag = false
      } else {
        this.storeFlag = false
      }
      const params = {
        page: 1,
        append: true,
        page_size: 10,
        reset: true,
      };
      await this.getStores(params)
    },
    storeLoadMore: async function() {
      this.loading = true;
      const params = {
        page: this.page,
        append: true,
        page_size: 10,
      };
      await this.getStores(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    reviewLoadMore: async function() {
      this.loading = true;
      const params = {
        page: this.reviewpage,
        append: true,
        page_size: 10,
      };
      await this.getUserReview(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    userLoadMore() {
      let start, end
      start = this.addUser.length
      end = this.addUser.length + 10
      for (let i = start; i < end; ++i) {
        this.addUser.push(this.users[i])
      }
    },
    changeStaff(params) {
      // console.log(params)
      this.setUserStaff(params)
    }
  }
}
</script>

<style scoped>
.tab {
  border: 1px solid black;
  display: inline-block;
  width: 24vw;
  padding: auto;
  font-size: 50px;
  text-align: center;
}
.tab:hover {
  background-color: black;
  color: white;
}
.loadMore {
  font-size: 40px;
  text-align: center;
  cursor: pointer;
}
table {
	border-collapse: collapse;
	border-spacing: 0;
	width: 100%;
	border: 1px solid #ddd;
}
th{
	text-align: left;
	padding: 16px;
}
tr:nth-child(even) {
  background-color: #ddd;
}
.deleteBtn {
  border: 1px solid black;
  padding: 1px;
  text-align: center;
  background-color: red;
  color: white;
  cursor: pointer;
}
.chageBtn {
  border: 1px solid black;
  padding: 1px;
  text-align: center;
  background-color: green;
  color: white;
  cursor: pointer;
}
</style>