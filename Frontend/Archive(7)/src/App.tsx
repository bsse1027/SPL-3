import React from "react";
import "./App.css";
import AppBody from "./components/AppBody";
import { Assets } from "./assets/index";
import ReactQueryProvider from "./helpers/ReactQueryProvider";

function App() {
  return (
    <ReactQueryProvider>
      <div className="App">
        <header className="App-header">
          <div className="flex">
            <h1>GAYnomaly</h1>
            <img src={Assets.Logo} alt="logo" height={25} />
          </div>
          <AppBody />
        </header>
      </div>
    </ReactQueryProvider>
  );
}

export default App;
