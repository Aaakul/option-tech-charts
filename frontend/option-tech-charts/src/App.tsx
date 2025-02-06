import "./App.css";
import { ConfigProvider, Layout, theme } from "antd";
import MyContent from "./components/MyContent";
import { useState } from "react";

function App() {
  const [isDarkTheme, setIsDarkTheme] = useState(true);
  const toggleTheme = () => setIsDarkTheme(!isDarkTheme);

  return (
    <ConfigProvider
      componentSize="small"
      theme={{
        // dark theme by default
        algorithm: isDarkTheme ? theme.darkAlgorithm : theme.defaultAlgorithm,
        components: {
          Layout: {
            headerBg: isDarkTheme ? "#001529" : "#ffffff",
            headerHeight: "2.5rem",
            headerPadding: "0",
          },
        },
      }}
    >
      <Layout style={{ minHeight: "100vh" }}>
        <MyContent isDarkTheme={isDarkTheme} onToggleTheme={toggleTheme} />
      </Layout>
    </ConfigProvider>
  );
}

export default App;
