import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // makes it work inside Docker
    port: 3000,
    proxy: {
      "/api": "http://backend:8000", // proxy to backend container
    },
  },
});
