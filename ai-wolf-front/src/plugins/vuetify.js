import "vuetify/styles"
import { createVuetify } from "vuetify"
import * as components from "vuetify/components"
import * as directives from "vuetify/directives"

const customTheme = {
  colors: {
    primary: "#00001c",
  }
}

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "customTheme",
    themes: { customTheme }
  },
})