import "./App.css";
import { ConfigProvider, Layout, theme } from "antd";
import MyContent from "./components/MyContent";
import { useState } from "react";
import MySider from "./components/MySider";


function App() {
  const [isDarkTheme, setIsDarkTheme] = useState(true);
  const toggleTheme = () => setIsDarkTheme(!isDarkTheme);
  

  return (
    <ConfigProvider
      componentSize="small"
      theme={{
        // dark theme by default
        algorithm: isDarkTheme ? theme.darkAlgorithm : theme.defaultAlgorithm,
      }}
    >
      <Layout style={{ minHeight: "100vh" }}>
        <MySider />
        <MyContent isDarkTheme={isDarkTheme} onToggleTheme={toggleTheme} />
      </Layout>
    </ConfigProvider>
  );
}

export default App;
