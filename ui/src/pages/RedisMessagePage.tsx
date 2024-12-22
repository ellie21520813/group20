import React, { useEffect, useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { notificationController } from '@app/controllers/notificationController';
import { useSearchParams } from 'react-router-dom';
import { Divider, List, Typography } from 'antd';
import { readToken } from '@app/services/localStorage.service';
import { Card } from '@app/components/common/Card/Card';

import * as S from '@app/components/tables/Tables/Tables.styles';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
const RedisMessagePage: React.FC = () => {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [messageHistory, setMessageHistory] = useState<string[]>([]);
  const [lastMessage, setLastMessage] = useState<string>();

  const evtSource = new EventSource(
    `${process.env.REACT_APP_API_URL}/v1/lstm/logs?token=${readToken()}&queue=${searchParams.get('queue')}`,
  );

  useEffect(() => {
    if (searchParams.get('queue') != null) {
      evtSource.addEventListener('new_message', function (event) {
        setMessageHistory((message) => [event.data, ...message]);
        setLastMessage(event.data);
        console.log(event.data);
      });
      evtSource.addEventListener('end_event', function (event) {
        evtSource.close();
      });

      return () => {
        evtSource.close();
      };
    }
  }, [lastMessage]);

  return (
    <>
      <PageTitle>Redis Message</PageTitle>
      <Card id="rabbitmq-logs" title="Redis Message" padding="1.25rem">
        <List
          size="small"
          header={<span>Last Message: {lastMessage}</span>}
          bordered
          dataSource={messageHistory}
          renderItem={(item) => (
            <List.Item>
              <Typography.Text>[+] </Typography.Text>
              {item}
            </List.Item>
          )}
        />
      </Card>
    </>
  );
};
export default RedisMessagePage;
