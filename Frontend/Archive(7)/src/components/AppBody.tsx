import { useState } from "react";
import { TailSpin } from "react-loader-spinner";
import { useQuery } from "react-query";
import { Assets } from "../assets/index";
import { runAnalytics } from "../APIs/api";
import { QUERY_KEY } from "../APIs/query_keys";

const AppBody: React.FC = () => {
  const [fileName, setFileName] = useState<string>("");

  const { refetch, isRefetching } = useQuery(
    QUERY_KEY.ANALYTICS,
    () => runAnalytics(),
    {
      enabled: false,
      retry: false,
      onSuccess: (res) => {
        console.log(res);
      },
    }
  );

  const handleFileUpload = (event: any) => {
    const file = event.target.files[0].name;
    setFileName(file);
  };

  const handleRunAnalytics = () => {
    refetch();
  };

  return (
    <>
      {fileName.length === 0 ? (
        <>
          <label htmlFor="file" className="upload-btn">
            Upload CSV
          </label>
          <input
            type="file"
            id="file"
            accept=".csv"
            className="d-none"
            onChange={handleFileUpload}
          />
        </>
      ) : (
        <div className="flex file-list">
          {fileName}

          <button className="run-btn" onClick={handleRunAnalytics}>
            <div className="flex">
              {isRefetching ? (
                <TailSpin
                  height="20"
                  width="20"
                  color="#fff"
                  ariaLabel="tail-spin-loading"
                  radius="1"
                  wrapperStyle={{}}
                  wrapperClass=""
                  visible={true}
                />
              ) : (
                <img src={Assets.Run} alt="play button" />
              )}
              Run Anal
            </div>
          </button>
          <button className="remove-btn" onClick={() => setFileName("")}>
            Remove
          </button>
        </div>
      )}
    </>
  );
};

export default AppBody;
