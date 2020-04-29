<template>
  <div>
    <div id="my_sidebar">
      <div class="my_sidebar_box">
        <div id="user_nickname">
          {{ user_name }}
        </div>
        <div id="user_id">
          {{ user_email }}
        </div>
        <div id="user_gender_age">
          {{ user_gender }} / {{ user_age }}
        </div>
        <div id="user_like_store" @click="likeStores()">
          <mypageUserLike
            :user-like-list="userLikeList"
          >
            <button slot="click">좋아요 모아보기</button>
          </mypageUserLike>
        </div>
      </div>
      <div class="my_sidebar_box">
        <div id="user_categories">
          <div>
            카테고리 모아보기
          </div>
          <hr style="margin: 8px 0;">
          <button 
            v-for="category in category_lst.slice(0,10)" 
            :id="`${category[0]}`" 
            :key="category[0]"
            class="user_category"
            @click="goSearchByCategory(`${ category[0] }`); onclickEvent(`${ category[0] }`)"
          >
            {{ category[0] }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MypageUserLike from "../components/MypageUserLike"
import { mapState, mapActions } from "vuex"

export default {
  components: {
    MypageUserLike
  },
  data() {
    return {
      cates: {},
      category_lst: "",
      flag: true,
      user_name: "",
      user_email: "",
      user_gender: "",
      user_age: ""
    }
  },
  computed: {
    ...mapState({
      reviews: state => state.data.reviewListForCate,
      userLikeList: state => state.data.userLikeList
    })
  },
  watch: {
    reviews: function() {
      if (this.flag) {
        // console.log(this.reviews)
        for (let i = 0; i < this.reviews.length; ++i) {
          // console.log(this.reviews[i].categories)
          for (let j = 0; j <= this.reviews[i].categories.length; ++j) {
            if (this.reviews[i].categories[j]) {
              if (this.reviews[i].categories[j] in this.cates) {
                this.cates[`${this.reviews[i].categories[j]}`] += 1
              } else {
                this.cates[`${this.reviews[i].categories[j]}`] = 1
              }
            }
          }
        }
        // console.log(this.cates)
        var dict = this.cates;
        this.category_lst = Object.keys(dict).map(function(key) {
          return [key, dict[key]];
        });
        this.category_lst.sort(function(first, second) {
          return second[1] - first[1];
        });
        // console.log(this.category_lst.slice(0,5));
        this.flag = false
      }
    },
    user_age: function() {
      if (0 <= this.user_age < 10) {
        this.user_age = "유소년"
      } else if (10 <= this.user_age < 20) {
        this.user_age = "10대"
      } else if (20 <= this.user_age < 30) {
        this.user_age = "20대"
      } else if (30 <= this.user_age < 40) {
        this.user_age = "30대"
      } else if (40 <= this.user_age < 50) {
        this.user_age = "40대"
      } else if (50 <= this.user_age < 60) {
        this.user_age = "50대"
      } else if (60 <= this.user_age < 70) {
        this.user_age = "60대"
      } else {
        this.user_age = "청춘"
      }
    }
  },
  mounted() {
    this.user_name = localStorage.getItem("username")
    this.user_email = localStorage.getItem("email")
    this.user_gender = localStorage.getItem("gender")
    this.user_age = localStorage.getItem("age")
    const params = {
      user: this.$route.params.userId,
      page_size: 1000
    };
    this.getReviewsForCate(params)
  },
  methods: {
    ...mapActions("data", ["getReviewsForCate"]),
    ...mapActions("data", ["resetCategoryList"]),
    ...mapActions("data", ["userLikeStores"]),
    goSearchByCategory(keyword) {
      // console.log(keyword)
      this.$emit("searchcate", keyword);
    },
    onclickState(word) {
      var target = document.getElementById(word)
      if (target.style.length == 0) {
        target.style.color = "white"
        target.style.backgroundColor = "black"
      } else {
        target.style = ""
      }
    },
    onclickEvent(word) {
      var el = document.getElementById("user_categories")
      el.addEventListener("click", this.onclickState(word), false)
    },
    likeStores() {
      this.userLikeStores()
    }
  }
}
</script>

<style scoped>
#my_sidebar {
  width: 22%;
  float: left;
  text-align: center;
  /* border: 1px solid black; */
  /* padding: 20px; */
  /* position: fixed; */
  /* background-color: rgba(255, 255, 255, 0.9); */
}
.my_sidebar_box {
  background-color: white;
  padding: 20px;
  margin-bottom: 20px;
  font-family: "Do Hyeon", sans-serif;
}
#user_nickname {
  font-size: 24px;
  margin-bottom: 10px;
}
#user_id {
  font-size: 20px;
  margin-bottom: 10px;
}
#user_gender_age {
  font-size: 20px;
  margin-bottom: 10px;
}
#user_like_store {
  font-size: 20px;
  height: 30px;
  border: 1px solid black;
  background-color: silver;
  transition: all .5s;
}
#user_like_store:hover {
  background-color: black;
  color: white;
}
#user_categories {
  /* display: flex; */
  font-size: 20px;
}
.user_category {
  /* display: flex; */
  font-size: 20px;
  margin: 10px;
  border: 1px solid black;
  padding: 5px;
  background-color: silver;
  transition: all .5s;
}
.user_category:hover,
.user_category_all:hover {
  background-color: black;
  color: white;
}
.user_category_all {
  font-size: 16px;
  margin: 10px;
  border: 1px solid black;
  padding: 5px;
  background-color: silver;
  transition: all .5s;
  display: block;
  width: 90%;
}

@media screen and (max-width: 600px) {
  #my_sidebar {
    width: 100%;
    float: none;
  }
  .my_sidebar_box {
    padding: 0px;
    background-color: rgb(255, 255, 255);
  }
  #user_nickname {
    font-size: 18px;
    margin-bottom: 0px;
  }
  #user_id {
    font-size: 14px;
    margin-bottom: 0px;
  }
  #user_gender_age {
    font-size: 14px;
    margin-bottom: 0px;
  }
  #user_categories {
    padding: 5px;
  }
  .user_category {
    font-size: 14px;
    margin: 5px;
  }
}

</style>