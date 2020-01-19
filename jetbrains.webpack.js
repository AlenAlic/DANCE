// This file can be used to enhance auto-completion for WebStorm
// Languages & Frameworks -> JavaScript -> Webpack
module.exports = {
  resolve: {
    alias: {
      // eslint-disable-next-line no-undef
      ["@"]: path.resolve(__dirname, "src")
    }
  }
};
