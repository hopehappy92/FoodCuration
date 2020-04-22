module.exports = {
  publicPath: "/",
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000/"
      }
    }
  },
  transpileDependencies: ["vuetify"],
  configureWebpack: {
    devServer: {
        host: 'http://i02d106.p.ssafy.io',
        port: '80'
    }
}
};
