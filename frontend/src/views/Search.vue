<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
    class="bgAll"
  >
    <v-container id="bgControl" fill-height fluid grid-list-xl class="bgControl">
      <v-layout justify-center wrap mt-5>
        <v-flex xs12 md8>
          <card class="upperCard">
            <div style="text-align: center; font-size: 40px; margin-top: 10px; margin-bottom: 10px; color: black; font-weight: 700;">
              {{ title }}
            </div>  
            <v-container py-0>
              <v-layout wrap>
                <v-flex xs12 md12>
                  <div class="searchBar_innder_middle">
                    <v-select
                      id="my_page_head_option"
                      v-model="options_value"
                      :items="options"
                      dense
                      item-color="black"
                      color="rgba(0, 0, 0, 1)"
                      style="display: inline-block; width: 200px; font-size: 15px;"
                      @change="selectOption"
                    />
                    <input
                      v-if="location"
                      v-model="storeName"
                      type="text"
                      placeholder="  상호명"
                      @keydown="enterKey"
                    >
                    <input
                      v-else
                      v-model="storeName"
                      type="text"
                      placeholder="  상호명 or 메뉴"
                      @keydown="enterKey"
                    >
                    <i v-if="location" class="fas fa-search" @click="onSubmit" />
                    <i v-else class="fas fa-search" @click="locationSubmit" />
                    <!-- <v-select
                      id="my_page_head_option"
                      v-model="options_value"
                      :items="options"
                      dense
                      item-color="black"
                      color="rgba(0, 0, 0, 1)"
                      style="display: inline-block; width: 200px; font-size: 15px; transform: translateY(-7.5%); margin-left: 10px;"
                      @change="selectOption"
                    /> -->
                  </div>
                  <p v-if="location === 0" id="desc_map">탐색하고 싶은 위치로 지도를 움직이고 범위를 선택해주세요</p>
                  <div v-if="location === 0" id="disBody">
                    <button id="btn1" @click.prevent="setDis(100)">100m</button>
                    <button id="btn2" @click.prevent="setDis(200)">200m</button>
                    <button id="btn3" class="underlined" @click.prevent="setDis(300)">300m</button>
                    <button id="btn4" @click.prevent="setDis(400)">400m</button>
                    <button id="btn5" @click.prevent="setDis(500)">500m</button>
                  </div>
                  <v-flex v-if="location === 0" id="mapCard">
                    <StoresLocation
                      ref="showMap"
                      :latitude="lat"
                      :longitude="lon"
                      :stores="stores"
                      :dis="dis"
                      @child="changedLocation"
                    />
                  </v-flex>
                </v-flex>
                <!-- <v-flex xs12 text-center>
                  <v-btn
                    v-if="location"
                    large
                    class="sliver --text ma-3"
                    rounded
                    dark
                    color="sliver lighten-1"
                    @click="onSubmit"
                  >전국 음식점 검색</v-btn>
                  <v-btn
                    v-else
                    large
                    class="sliver--text ma-3"
                    rounded
                    dark
                    color="sliver lighten-1"
                    @click="locationSubmit"
                  >주변 음식점 검색</v-btn>
                </v-flex> -->
              </v-layout>
            </v-container>
          </card>
          <v-divider class="mx-4" />
        </v-flex>
        <v-flex xs12 md8>
          <v-flex v-for="store in stores" :key="store.id" pa-4>
            <router-link
              :to="{ name: 'StoreDetail', params: {
                storeId: store.id
              }}"
            >
              <store-list-card
                :id="store.id"
                :name="store.name"
                :categories="store.categories"
                :address="store.address"
                :tel="store.tel"
              />
            </router-link>
          </v-flex>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Card from "@/components/Card";
// import router from "@/router";
import StoreListCard from "@/components/StoreListCard";
import StoresLocation from "@/components/StoresLocation";
// import Nav from "@/components/Nav";
import { mapState, mapActions, mapMutations } from "vuex";
export default {
  components: {
    Card,
    StoreListCard,
    StoresLocation,
    // Nav
  },
  data: () => ({
    storeName: "",
    loading: true,
    lon: 0,
    lat: 0,
    location: 1, //location 0이 위치가 있는거, 1이 현재 위치 없는 것
    sort_value: "",
    showMap: 0,
    dis: 300,
    options: [
      { text: "일반검색", value: 1 },
      { text: "주변검색", value: 2 }
    ],
    options_value: 1,
    title: "일반검색"
  }),
  watch: {
    options_value: function() {
      if (this.options_value == 2) {
        this.getLocation();
      } else {
        this.noLocation();
      }
    }
  },
  computed: {
    ...mapState({
      stores: state => state.data.storeSearchList,
      page: state => state.data.storeSearchPage
    })
  },
  methods: {
    ...mapActions("data", ["getStores"]),
    ...mapActions("data", ["searchByLocation"]),
    ...mapMutations("data", ["checkNavSearch"]),
    ...mapMutations("data", ["resetNavState"], null, { root: true }),
    onSubmit: async function() {
      const params = {
        name: this.storeName,
        page: 1,
        append: false
      };
      await this.getStores(params);
      this.loading = false;
      let bgControl = document.getElementById("bgControl");
      bgControl.classList.toggle("bgControl", false);
    },
    loadMore: async function() {
      this.loading = true;
      const params = {
        name: this.storeName,
        page: this.page,
        append: true
      };
      if (this.location) {
        await this.getStores(params);
        setTimeout(() => {
          this.loading = false;
        }, 1000);
      }
    },
    getLocation() {
      const that = this;
      navigator.geolocation.getCurrentPosition(function(pos) {
        console.log(pos.coords.longitude, pos.coords.latitude);
        setTimeout(() => {
          that.lat = Number(pos.coords.latitude);
          that.lon = Number(pos.coords.longitude);
          that.location = 0;
          setTimeout(() => {
            that.$refs.showMap.showMap();
          }, 500);
        }, 500);
      });
    },
    noLocation() {
      this.location = 1;
    },
    locationSubmit: async function() {
      console.log(this.lat);
      console.log(this.lon);
      console.log(this.storeName);
      const params = {
        latitude: this.lat,
        longitude: this.lon,
        words: this.storeName,
        dis: Number(this.dis)
      };
      await this.searchByLocation(params);
      this.loading = false;
      this.$refs.showMap.showMap();
      this.showMap = 1;
      let bgControl = document.getElementById("bgControl");
      bgControl.classList.toggle("bgControl", false);
    },
    changedLocation(location) {
      this.lat = location.Ha;
      this.lon = location.Ga;
    },
    setDis(distance) {
      let btn1 = document.getElementById("btn1");
      let btn2 = document.getElementById("btn2");
      let btn3 = document.getElementById("btn3");
      let btn4 = document.getElementById("btn4");
      let btn5 = document.getElementById("btn5");
      this.dis = distance;
      switch (distance) {
        case 100:
          btn1.classList.toggle("underlined", true);
          btn2.classList.toggle("underlined", false);
          btn3.classList.toggle("underlined", false);
          btn4.classList.toggle("underlined", false);
          btn5.classList.toggle("underlined", false);
          this.locationSubmit();
          break;
        case 200:
          btn1.classList.toggle("underlined", false);
          btn2.classList.toggle("underlined", true);
          btn3.classList.toggle("underlined", false);
          btn4.classList.toggle("underlined", false);
          btn5.classList.toggle("underlined", false);
          this.locationSubmit();
          break;
        case 300:
          btn1.classList.toggle("underlined", false);
          btn2.classList.toggle("underlined", false);
          btn3.classList.toggle("underlined", true);
          btn4.classList.toggle("underlined", false);
          btn5.classList.toggle("underlined", false);
          this.locationSubmit();
          break;
        case 400:
          btn1.classList.toggle("underlined", false);
          btn2.classList.toggle("underlined", false);
          btn3.classList.toggle("underlined", false);
          btn4.classList.toggle("underlined", true);
          btn5.classList.toggle("underlined", false);
          this.locationSubmit();
          break;
        case 500:
          btn1.classList.toggle("underlined", false);
          btn2.classList.toggle("underlined", false);
          btn3.classList.toggle("underlined", false);
          btn4.classList.toggle("underlined", false);
          btn5.classList.toggle("underlined", true);
          this.locationSubmit();
          break;
        default:
          console.log("뭔일이고?");
      }
    },
    selectOption(value) {
      this.options_value = value;
      if (this.options_value === 1) {
        this.title = "일반 검색";
      } else {
        this.title = "주변 검색";
      }
    },
    enterKey() {
      if (window.event.keyCode == 13) {
        if (this.location === 1) {
          this.onSubmit();
        } else {
          this.locationSubmit();
        }
      }
    }
  },
  mounted() {
    setTimeout(() => {
      this.checkNavSearch(1);
      if (this.$store.state.data.searchFromNav) {
        console.log("들어왔다");
        this.storeName = this.$store.state.data.storeNameFromNav;
        this.onSubmit();
        setTimeout(() => {
          this.resetNavState();
        }, 500);
      }
    }, 500);
  }
};
</script>
<style scoped>
.bgAll {
  height: 100%;
  background: rgb(14, 14, 14); /* Old browsers */
  background: -moz-linear-gradient(
    left,
    rgba(14, 14, 14, 1) 0%,
    rgba(125, 126, 125, 1) 49%,
    rgba(125, 126, 125, 1) 56%,
    rgba(14, 14, 14, 1) 100%
  ); /* FF3.6-15 */
  background: -webkit-linear-gradient(
    left,
    rgba(14, 14, 14, 1) 0%,
    rgba(125, 126, 125, 1) 49%,
    rgba(125, 126, 125, 1) 56%,
    rgba(14, 14, 14, 1) 100%
  ); /* Chrome10-25,Safari5.1-6 */
  background: linear-gradient(
    to right,
    rgba(14, 14, 14, 1) 0%,
    rgba(125, 126, 125, 1) 49%,
    rgba(125, 126, 125, 1) 56%,
    rgba(14, 14, 14, 1) 100%
  ); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#0e0e0e', endColorstr='#0e0e0e',GradientType=1 ); /* IE6-9 */
}
#mapCard {
  width: 100%;
}
#desc_map {
  text-align: center;
}
#disBody {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-around;
  border-top: 1px rgb(107, 107, 107) solid;
  border-bottom: 1px rgb(107, 107, 107) solid;
}
#disBody > button {
  width: 10em;
  height: 2.5em;
  justify-content: center;
  font-size: 1em;
}
#disBody > button:hover {
  width: 10em;
  height: 2.5em;
  justify-content: center;
  font-weight: bold;
}
.underlined {
  text-decoration: none;
  font-weight: bold;
  position: relative;
  z-index: 1;
  display: inline-flex;
  padding-left: 10px;
  padding-bottom: 5px;
  padding-right: 10px;
}
.underlined::before {
  content: "";
  width: 50%;
  height: 80%;
  background-image: linear-gradient(
    to top,
    #696969 10%,
    rgb(255, 255, 255) 30%
  );
  position: absolute;
  left: 30px;
  bottom: 2px;
  z-index: -1;
  will-change: width;
  transform: rotate(-2deg);
  transform-origin: left bottom;
}
.searchBar_innder_middle {
  width: 100%;
  display: flex;
  align-items: baseline;
  justify-content: center;
}
.searchBar_innder_middle > input {
  /* background: #f1f1f1; */
  width: 100%;
  height: 40px;
  /* border-radius: 10px; */
  transform: translateY(-4px);
  border-bottom: 1px solid black;
}
.searchBar_innder_middle > input::placeholder {
  font-size: 17px;
  transform: translateY(6px);
}
.searchBar_innder_middle > i {
  font-size: 20px;
  padding: 5px;
  display: flex;
  align-items: center;
  position: relative;
  right: 30px;
}
.searchBar_innder_middle > i:hover {
  cursor: pointer;
}
input:focus::-webkit-input-placeholder {
  color: transparent;
  outline: none;
}
input:focus {
  outline: none;
}
.bgControl {
  height: 100%;
}
@media screen and (max-width: 600px) {
  .underlined::before {
    left: 18px;
  }
}
</style>