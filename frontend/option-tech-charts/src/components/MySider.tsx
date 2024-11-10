import { Menu } from "antd";
import Sider from "antd/es/layout/Sider";
import React, { useState } from "react";

const siderItems = [
  {
    key: "1",
    label: "OI",
  },
  {
    key: "2",
    label: "GEX",
  },
  {
    key: "3",
    label: "DEX",
  },
  {
    key: "4",
    label: "Other",
  },
];

const MySider: React.FC = () => {
  const [collapsed, setCollapsed] = useState(true);
  return (
    <Sider
      collapsible
      collapsed={collapsed}
      collapsedWidth={50}
      width={100}
      onCollapse={(value) => setCollapsed(value)}
    >
      <div className="demo-logo-vertical" />
      <Menu
        defaultSelectedKeys={["1"]}
        mode="inline"
        theme="dark"
        items={siderItems}
      />
    </Sider>
  );
};

export default MySider;
