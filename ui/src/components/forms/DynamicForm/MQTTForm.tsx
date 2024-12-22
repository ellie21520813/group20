import React, { useState } from 'react';
import { Col, Row, List, Typography, Space } from 'antd';
import { useTranslation } from 'react-i18next';
import * as mqtt from 'mqtt';
import { PlusOutlined } from '@ant-design/icons';
import { BaseButtonsForm } from '@app/components/common/forms/BaseButtonsForm/BaseButtonsForm';
import { Input } from '@app/components/common/inputs/Input/Input';
import { Select, Option } from '@app/components/common/selects/Select/Select';
import { Button } from '@app/components/common/buttons/Button/Button';
import { notificationController } from '@app/controllers/notificationController';

interface MQTTConfig {
  connection: string;
  subscribeTopic: [any];
}

export const MQTTForm: React.FC = () => {
  const [isFieldsChanged, setFieldsChanged] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [form] = BaseButtonsForm.useForm();
  const [messages, setMessages] = useState<string[]>([]);
  const [mqttClient, setMQTTClient] = useState<mqtt.MqttClient>();
  const { t } = useTranslation();

  const connection = [{ label: 'Hive Cloud', value: process.env.REACT_APP_MQTT_CONNECTION }];

  const onFinish = (values: MQTTConfig) => {
    setLoading(true);
    setTimeout(() => {
      const clientId = 'emqx_react_' + Math.random().toString(16).substring(2, 8);
      const username = process.env.REACT_APP_MQTT_USER;
      const password = process.env.REACT_APP_MQTT_PASSWORD;
      const mqttClient = mqtt.connect(values.connection, {
        clientId,
        username,
        password,
      });
      setMQTTClient(mqttClient);
      values.subscribeTopic.forEach((topic) => {
        mqttClient.subscribe(topic.topic);
      });

      setLoading(false);
      setFieldsChanged(false);
      notificationController.success({ message: t('common.success') });
    }, 1000);
  };

  mqttClient?.on('message', (topic, message) => {
    console.log(`${topic}: ${message}`);
    setMessages((msg) => [message.toString(), ...msg]);
  });

  const handleChange = () => {
    form.setFieldsValue({ topics: [] });
  };

  return (
    <Row key="mqtt_message" gutter={[10, 10]}>
      <Col span={24}>
        <BaseButtonsForm
          form={form}
          name="mqttForm"
          isFieldsChanged={isFieldsChanged}
          loading={isLoading}
          onFinish={onFinish}
          autoComplete="off"
          onFieldsChange={() => setFieldsChanged(true)}
        >
          <BaseButtonsForm.Item
            name="connection"
            label="Connection"
            rules={[{ required: true, message: 'Connection is required' }]}
          >
            <Select options={connection} onChange={handleChange} />
          </BaseButtonsForm.Item>
          <BaseButtonsForm.List name="subscribeTopic">
            {(fields, { add, remove }) => (
              <>
                {fields.map((field) => (
                  <Row key={field.key} wrap={false} gutter={[10, 10]} align="middle" justify="space-between">
                    <Col span={24}>
                      <BaseButtonsForm.Item
                        noStyle
                        shouldUpdate={(prevValues: any, curValues: any) =>
                          prevValues.area !== curValues.area || prevValues.sights !== curValues.sights
                        }
                      >
                        {() => (
                          <BaseButtonsForm.Item
                            {...field}
                            label="Topic"
                            name={[field.name, 'topic']}
                            key={'topic-name'}
                            rules={[{ required: true, message: 'Topic is required' }]}
                          >
                            <Input />
                          </BaseButtonsForm.Item>
                        )}
                      </BaseButtonsForm.Item>
                    </Col>
                  </Row>
                ))}

                <BaseButtonsForm.Item>
                  <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                    Add Subscribe Topic
                  </Button>
                </BaseButtonsForm.Item>
              </>
            )}
          </BaseButtonsForm.List>
        </BaseButtonsForm>
      </Col>
      <Col span={24}>
        <List
          size="small"
          header={<span>Message:</span>}
          bordered
          dataSource={messages}
          renderItem={(item) => (
            <List.Item>
              <Typography.Text>[+] </Typography.Text>
              {item}
            </List.Item>
          )}
        />
      </Col>
    </Row>
  );
};
