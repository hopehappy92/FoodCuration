<template>
  <div>
    <div id="map" style="width:100%;height:350px;"></div>
  </div>
</template>

<script>
import router from "@/router";
export default {
  props: {
    longitude: Number,
    latitude: Number,
    stores: Object
  },
  methods: {
    showMap() {
      console.log(this.longitude, this.latitude);
      var mapContainer = document.getElementById("map"), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(this.latitude, this.longitude), // 지도의 중심좌표
          level: 4 // 지도의 확대 레벨
        };

      var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
      var stores = this.stores;
      var positions = [];
      for (let store of stores) {
        positions.push({
          content: `<div>${store.name}</div>`,
          latlng: new kakao.maps.LatLng(store.lat, store.lng),
          storeId: store.id
        });
      }

      for (var i = 0; i < positions.length; i++) {
        // 마커를 생성합니다
        var marker = new kakao.maps.Marker({
          map: map, // 마커를 표시할 지도
          position: positions[i].latlng, // 마커의 위치
          clickable: true
        });

        var infowindow = new kakao.maps.InfoWindow({
          content: positions[i].content // 인포윈도우에 표시할 내용
        });

        let storeId = positions[i].storeId;
        kakao.maps.event.addListener(
          marker,
          "mouseover",
          makeOverListener(map, marker, infowindow)
        );
        kakao.maps.event.addListener(
          marker,
          "mouseout",
          makeOutListener(infowindow)
        );
        kakao.maps.event.addListener(marker, "click", function() {
          router.push({
            name: "StoreDetail",
            params: { storeId: storeId }
          });
        });
      }

      function makeOverListener(map, marker, infowindow) {
        return function() {
          infowindow.open(map, marker);
        };
      }

      function makeOutListener(infowindow) {
        return function() {
          infowindow.close();
        };
      }
    }
  }
};
</script>

<style>
</style>