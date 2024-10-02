// src/App.tsx
import React from "react";
import "./App.css";
import Images from "./components/images/Images";
import CurveComponent from "./components/IOCurves";

const App: React.FC = () => {
  return (
    <div className="App">
      <Images />
      <CurveComponent />
    </div>
  );
};

export default App;
