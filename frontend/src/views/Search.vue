<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
    class="bgAll"
  >
    <v-container fill-height fluid grid-list-xl>
      <v-layout justify-center wrap mt-5>
        <v-flex xs12 md8>
          <card title="맛집 검색">
            <v-form>
              <v-container py-0>
                <v-layout wrap>
                  <v-flex xs12 md12>
                    <v-text-field v-if="location" v-model="storeName" label="음식점 이름" />
                    <v-text-field v-else v-model="storeName" label="음식점 이름" />
                    <p v-if="location === 0" id="desc_map">거리를 설정하고 탐색하고 싶은 위치로 지도를 움직여주세요</p>
                    <v-radio-group v-if="location === 0" v-model="dis" row class="radio">
                      <v-radio label="200m" value="200" color="black" />
                      <v-radio label="400m" value="400" color="black" />
                      <v-radio label="600m" value="600" color="black" />
                      <v-radio label="800m" value="800" color="black" />
                    </v-radio-group>
                    <v-flex v-if="location === 0" id="mapCard">
                      <StoresLocation
                        ref="showMap"
                        :latitude="lat"
                        :longitude="lon"
                        :stores="stores"
                        @child="changedLocation"
                      ></StoresLocation>
                    </v-flex>
                    <v-radio-group v-model="sort_value" row class="radio">
                      <v-radio label="주변검색" value="주변검색" color="black" />
                      <v-radio label="일반검색" value="일반검색" color="black" />
                    </v-radio-group>
                  </v-flex>
                  <v-flex xs12 text-center>
                    <v-btn
                      large
                      class="indigo white--text ma-5"
                      rounded
                      color="blue lighten-1"
                      @click="onSubmit"
                      v-if="location"
                    >전지역 검색</v-btn>
                    <v-btn
                      large
                      class="indigo white--text ma-5"
                      rounded
                      color="blue lighten-1"
                      @click="locationSubmit"
                      v-else
                    >위치기반 검색</v-btn>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </card>
          <v-divider class="mx-4" />
        </v-flex>
        <!-- <v-flex xs12 md8 v-show="showMap">
          <StoresLocation
            ref="showMap"
            :latitude="lat"
            :longitude="lon"
            :stores="stores"
            @child="changedLocation"
          ></StoresLocation>
        </v-flex>-->
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
import router from "@/router";
import StoreListCard from "@/components/StoreListCard";
import StoresLocation from "@/components/StoresLocation";
import { mapState, mapActions } from "vuex";
import axios from "axios";
export default {
  components: {
    Card,
    StoreListCard,
    StoresLocation
  },
  data: () => ({
    storeName: "",
    loading: true,
    lon: 0,
    lat: 0,
    location: 1, //location 0이 위치가 있는거, 1이 현재 위치 없는 것
    sort_value: "",
    showMap: 0,
    dis: 300
  }),
  watch: {
    sort_value: function() {
      if (this.sort_value == "주변검색") {
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
    onSubmit: async function() {
      const params = {
        name: this.storeName,
        page: 1,
        append: false
      };
      await this.getStores(params);
      this.loading = false;
      // this.showMap = 0;
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
        that.lat = pos.coords.latitude;
        that.lon = pos.coords.longitude;
        that.location = 0;
        setTimeout(() => {
          that.$refs.showMap.showMap();
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
    },
    changedLocation(location) {
      this.lat = location.Ha;
      this.lon = location.Ga;
    }
  }
};
</script>
<style scoped>
.bgAll {
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
</style>