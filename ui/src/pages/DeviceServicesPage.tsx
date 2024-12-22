import React, { useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom';
import ReactPlayer from 'react-player';
import { useTranslation } from 'react-i18next';
import { Button, Card, List, Dropdown, Image } from 'antd';
import { LikeOutlined, MessageOutlined, StarOutlined, LineChartOutlined , DownOutlined, VideoCameraOutlined } from '@ant-design/icons';
import { useSearchParams } from 'react-router-dom';
import { Avatar, Col, Row, Space, TablePaginationConfig, message } from 'antd';
import type { MenuProps } from 'antd';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import { DiscoverTable } from '@app/components/tables/DeviceTable/DiscoverTable';
import { Spinner } from '@app/components/common/Spinner/Spinner';
import * as S from '@app/components/tables/Tables/Tables.styles';
import { httpApi } from '@app/api/http.api';
import { getDevice, getRtspConfig } from '@app/api/device.api';
import { readToken } from '@app/services/localStorage.service';
import Column from 'antd/lib/table/Column';
import { notificationController } from '@app/controllers/notificationController';
import useWebSocket, { ReadyState } from 'react-use-websocket';


const DeviceServicesPage: React.FC = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [deviceId, setDeviceID] = useState<string>('');
  const [services, setServices] = useState<any>();
  const [intervalID, setIntervalID] = useState<NodeJS.Timer>();
  const [resultHTMLContent, setResultHTMLContent] = useState<string>('');
  const [showVideoPlayer, setShowVideoPlayer] = useState<boolean>(false);
  const [showFaceDetect, setShowFaceDetect] = useState<boolean>(false);
  const [streamingUrl, setStreamingURL] = useState<string>();
  const [contentLoading, setContentLoading] = useState<boolean>(false);
  const [streamingProcessID, setStreamingProcessID] = useState();
  // const [faceResults, setFaceResults] = useState<any[]>([]);
  const [faceResults, setFaceResults] = useState<Blob[]>([new Blob()]);
  const [socketUrl, setSocketUrl] = useState("");
  const ws = useRef<WebSocket>();
 
  const palyerRef = React.useRef()


  useEffect(() => {
    const deviceIDParam = searchParams.get('device_id');
    setDeviceID(deviceIDParam || '');
    return () => {
      ws.current?.close();
    }
  }, []);

  useEffect(() => {
    if (!ws.current) return;
    ws.current.onmessage = e => {
      const message = e.data;
      setFaceResults(blob => [message, ...blob]);
      // setFaceResults(old => [{id: i, blob: e.data}, ...old]);
    }
  })
  

  // use API to get a list of service categories: todo later, hardcode for testing
  const items: MenuProps['items'] = [
    {
      key: '1',
      label: "Camera Services",
      icon: <VideoCameraOutlined />
    },
    {
      key: '2',
      label: "Timeseries Services",
      icon: <LineChartOutlined />,
    },
  ];

  const startService = (service: any) => {
    ws.current?.close();
    setResultHTMLContent("");
    setShowVideoPlayer(false);
    setShowFaceDetect(false);
    setContentLoading(true);
    // call API to excute service
    if (service["id"] == "1"){
      getRtspConfig(deviceId).then(response => {
        console.log(response);
        httpApi.post(`/v1/camera/capture`, response, {responseType: 'blob'}).then(res => {
          setResultHTMLContent(
            `<img style="max-width: 100%" alt="Image" src="${URL.createObjectURL(res.data)}" />`
          )
          setContentLoading(false);
        });
      });
    }
    if (service["id"] == "2"){
      getRtspConfig(deviceId).then(response => {
        httpApi.post(`/v1/camera/start-streaming`, response).then(res => {
          if (res.data["stream_url"]){
            setStreamingURL(`${res.data["stream_url"]}?token=${readToken()}`);
            setStreamingProcessID(res.data['process_id']);
          } 
          if (res.data["message"]){
            notificationController.info({message: res.data["message"]})
          }
          setShowVideoPlayer(true);
          setContentLoading(false);
        });
      });
    }
    if (service["id"] == "3"){
      getRtspConfig(deviceId).then(response => { 
        var stream_url = response["url"];
        var socket_url = `ws://${process.env.REACT_APP_BE}/ws/camera/${deviceId}?url=${stream_url}`
        setSocketUrl(socket_url)

        ws.current = new WebSocket(socket_url);
        ws.current.onopen = () => {
          console.log("ws opened");
        }
        ws.current.onclose = () => {
          console.log("ws closed")
        }
        var interval = setInterval(() => {
          if (ws.current?.readyState == WebSocket.OPEN){
            setContentLoading(false);
            setShowFaceDetect(true);
            clearInterval(interval);
          }
        }, 2000);
      })
      


      // var i = 0;
      // setInterval(() => {
      //   setFaceResults(e => [{
      //     id: i,
      //     img: `https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png`,
      //     content: Date.now().toLocaleString()
      //   }, ...e])
      // }, 1000);

      // getRtspConfig(deviceId).then(response => {
      //   console.log(response);
      //   httpApi.post(`/v1/camera/face-detect`, response, {responseType: 'blob'}).then(res => {
      //     setResultHTMLContent(
      //       `<img style="max-width: 100%" alt="Image" src="${URL.createObjectURL(res.data)}" />`
      //     )
      //     setContentLoading(false);
      //   });
      // });
    }
  }

  const stopStreaming = () => {
    getRtspConfig(deviceId).then(response => {
      httpApi.post(`/v1/camera/stop-streaming`, response).then(res => {
        setShowVideoPlayer(false);
        notificationController.success({message: res.data["message"]});
      })
    })
  }

  const stopFaceDetect = () => {
    ws.current?.close(); 
    window.location.reload();
    setShowFaceDetect(false);
  }

  const onClick: MenuProps['onClick'] = ({ key }) => {
    // call API get list services: todo later, hardcode for testing
    if (key == '1'){
      setServices(
        {
          category: 1,
          description: "services for camera",
          services: [
            {
              id: 1,
              name: "Image Capture"
            },
            {
              id: 2,
              name: "Video Stream"
            },
            {
              id: 3,
              name: "Face Detect"
            }
          ]
        }
      );
    }
    if (key == '2'){
      setServices(
        {
          category: 2,
          description: "services for time series data",
          services: [
            {
              id: 3,
              name: "RNN"
            },
            {
              id: 4,
              name: "LSTM"
            }
          ]
        }
      );
    }
  };

  

  return (
    <>
      <PageTitle>Device</PageTitle>
      <S.TablesWrapper>
        <S.Card id="device-services" title="Device Services" key="device-service" padding="1.25rem 1.25rem 1.25rem">
          <Row gutter={16}>
            <Col span={24}>
              <Row gutter={16}>
                <Space direction='vertical'>
                  <Dropdown menu={{ items, onClick }}>
                    <a onClick={(e) => e.preventDefault()}>
                      <Space>
                        Services
                        <DownOutlined />
                      </Space>
                    </a>
                  </Dropdown>
                  {
                    services != undefined &&
                    <Space>
                      {
                        services.services.map((item: any) => {
                          return (
                            <Button disabled={contentLoading} onClick={() => startService(item)} key={item["id"]} size="small" type="primary" block>
                              {item["name"]}
                            </Button>
                          )
                        })
                      }
                    </Space>
                  }
                </Space>
              </Row>
              <Row style={{marginTop: "10px"}} gutter={16}>
                <Spinner style={{margin: "auto"}} spinning={contentLoading}>
                  
                </Spinner>
                <div style={{width: "100%"}} dangerouslySetInnerHTML={{__html: resultHTMLContent}}>
            
                </div>
                { showVideoPlayer && 
                  <Space direction='horizontal'>
                    <ReactPlayer
                      url={streamingUrl}
                      controls={true}
                      height="50%"
                    />
                    <Button onClick={stopStreaming}>Stop</Button>
                  </Space>
                }
                { showFaceDetect &&
                  <Space direction='horizontal'>
                    <img
                      alt="logo"
                      src={URL.createObjectURL(faceResults[0])}
                    />
                    <Button onClick={stopFaceDetect}>Stop</Button>
                  </Space>
                  // <Space direction='vertical'>
                  //   {
                  //     faceResults.map(blob => {
                  //       return <img
                  //               width={272}
                  //               alt="logo"
                  //               src={URL.createObjectURL(blob)}
                  //             />
                  //     })
                  //   }
                  // </Space>
                  // <List
                  //   itemLayout="vertical"
                  //   size="small"
                  //   style={{"width": "100%"}}
                  //   pagination={{
                  //     onChange: (page) => {
                  //       console.log(page);
                  //     },
                  //     pageSize: 3,
                  //   }}
                  //   dataSource={faceResults}
                  //   renderItem={(item) => (
                  //     <List.Item
                  //       key={item.id}
                  //     >
                  //       <img
                  //           width={272}
                  //           alt="logo"
                  //           src={URL.createObjectURL(item.blob)}
                  //         />
                  //     </List.Item>
                  //   )}
                  // />
                }
              </Row>
            </Col>
          </Row>
        </S.Card>
      </S.TablesWrapper>
    </>
  );
};
export default DeviceServicesPage;
