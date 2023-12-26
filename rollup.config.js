import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";
import css from "rollup-plugin-css-only";

export default [
  {
    input: "imports.js",
    output: {
      file: "static/js/bundle.built.js",
      format: "iife",
      name: "bundle",
    },
    plugins: [nodeResolve(), terser()],
  },
  {
    input: "imports.styles.js",
    output: {
      file: "static/css/bundle.built.css",
      name: "styles",
    },
    plugins: [nodeResolve(), css({ output: "bundle.built.css" })],
  },
];
