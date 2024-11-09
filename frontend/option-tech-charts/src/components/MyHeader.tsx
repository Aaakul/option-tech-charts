import { SunOutlined, MoonOutlined, GithubOutlined } from "@ant-design/icons";
import { Header } from "antd/es/layout/layout";
import React from "react";

interface TitleProps {
  isDarkTheme: boolean;
  onToggleTheme: () => void;
}

const MyHeader: React.FC<TitleProps> = ({ isDarkTheme, onToggleTheme }) => {
  return (
    <Header>
      <div className="title-container">
        <div className="toggle-theme" onClick={onToggleTheme}>
          {isDarkTheme ? <SunOutlined /> : <MoonOutlined />}
        </div>
        <div className="titles">
          <h2>chart 1</h2>
        </div>
        <a
          href="https://www.github.com/aaakul"
          target="_blank"
          rel="noopener noreferrer"
          className="main-card-extra"
        >
          <GithubOutlined />
        </a>
      </div>
    </Header>
  );
};

export default MyHeader;
