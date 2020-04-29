<template>
  <div>
    <div id="map" style="width:100%;height:350px;" />
  </div>
</template>

<script>
import router from "@/router";
export default {
  props: {
    longitude: Number,
    latitude: Number,
    startSearch: Number,
    dis: Number,
    stores: {
      type: Array,
      default: false
    }
  },
  data() {
    return {
      location: Object
    };
  },
  methods: {
    showMap() {
      // var mapContainer = document.getElementById("map"),
      //   mapOption = {
      //     center: new kakao.maps.LatLng(this.latitude, this.longitude),
      //     level: 3
      //   };
      // var map = new kakao.maps.Map(mapContainer, mapOption);
      // var markerPosition = new kakao.maps.LatLng(this.latitude, this.longitude);
      // var marker = new kakao.maps.Marker({
      //   position: markerPosition
      // });
      // marker.setMap(map);
      const that = this;
      // console.log("지도야 나와라!!!!");
      var mapContainer = document.getElementById("map"), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(this.latitude, this.longitude), // 지도의 중심좌표
          level: that.dis > 300 ? 5 : 4 // 지도의 확대 레벨
        };

      var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
      var markerPosition = new kakao.maps.LatLng(this.latitude, this.longitude);

      var imageSrc = "https://image.flaticon.com/icons/svg/1792/1792071.svg",
        imageSize = new kakao.maps.Size(52, 47), // 마커이미지의 크기입니다
        imageOption = { offset: new kakao.maps.Point(27, 69) };
      var markerImage = new kakao.maps.MarkerImage(
        imageSrc,
        imageSize,
        imageOption
      );
      var marker = new kakao.maps.Marker({
        position: markerPosition,
        image: markerImage
      });
      marker.setMap(map);

      var stores = this.stores;
      var positions = [];
      kakao.maps.event.addListener(map, "center_changed", function() {
        var latlng = map.getCenter();
        that.location = latlng;
        that.$emit("child", that.location);
      });

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