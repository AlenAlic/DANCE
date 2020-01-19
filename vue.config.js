// Version used for forcing file cache invalidation in exceptional cases
const VERSION = "1";

module.exports = {
  transpileDependencies: ["vuetify"],
  // https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-pwa
  pwa: {
    appleMobileWebAppCapable: "yes",
    appleMobileWebAppStatusBarStyle: "black",
    workboxPluginMode: "GenerateSW",
    workboxOptions: {
      skipWaiting: true,
      clientsClaim: true
    },
    iconPaths: {
      favicon32: "img/pwa/favicon-32x32.png",
      favicon16: "img/pwa/favicon-16x16.png",
      appleTouchIcon: "img/pwa/apple-touch-icon-152x152.png",
      maskIcon: "img/pwa/safari-pinned-tab.svg",
      msTileImage: "img/pwa/mstile-144x144.png"
    },
    themeColor: "#FFFFFF",
    msTileColor: "#4169E1"
  },
  productionSourceMap: false,
  chainWebpack: config => {
    if (process.env.NODE_ENV === "production") {
      // Add version suffix to file names to force cache invalidation (CDN, Browser, and SW) in exceptional cases
      config.output.filename(`js/[name].[contenthash:8].v${VERSION}.js`);
      config.output.chunkFilename(`js/[name].[contenthash:8].v${VERSION}.js`);
      // Don't copy over testing and dev configs
      config.plugin("copy").tap(([options]) => {
        options[0].ignore.push("config/testing.json");
        options[0].ignore.push("config/development.json");
        return [options];
      });
    }
    // Don't copy over .example files
    config.plugin("copy").tap(([options]) => {
      options[0].ignore.push("*.example");
      return [options];
    });
  },
  css: {
    extract:
      process.env.NODE_ENV === "production"
        ? {
            filename: `css/[name].[contenthash:8].v${VERSION}.css`,
            chunkFilename: `css/[name].[contenthash:8].v${VERSION}.css`
          }
        : undefined
  }
};
