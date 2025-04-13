/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Add declaration for .js modules
declare module '*.js' {
  const value: any; // Use 'any' for simplicity, or define specific module shapes if needed
  export default value;
}
