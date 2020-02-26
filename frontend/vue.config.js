const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  publicPath:
    process.env.NODE_ENV === "development" ? "http://0.0.0.0:8080/" : "/",
  outputDir: "./dist/",
  assetsDir: "static",
  pwa: {
    name: "Temperature recorder",
    appleMobileWebAppCapable: "yes",
    iconPaths: {
      favicon32: "static/icons/favicon-32x32.png",
      favicon16: "static/icons/favicon-16x16.png",
      appleTouchIcon: "static/icons/apple-touch-icon-152x152.png"
    }
  },

  chainWebpack: config => {
    config.optimization.splitChunks(false);

    config
      .plugin("BundleTracker")
      .use(BundleTracker, [{ filename: "../frontend/webpack-stats.json" }]);

    config.resolve.alias.set("__STATIC__", "static");

    config.devServer
      .public("http://0.0.0.0:8080")
      .host("0.0.0.0")
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ "Access-Control-Allow-Origin": ["*"] });
  },

  transpileDependencies: ["vuetify"]
};
