import { useEffect } from "react";
import { Modal, Form, Input, InputNumber, Select, DatePicker } from "antd";
import dayjs from "dayjs";

const COUNTRY_CURRENCY = {
  India: "INR", USA: "USD", UK: "GBP", Germany: "EUR", Singapore: "SGD",
};

export default function EmployeeForm({ open, employee, onSubmit, onCancel }) {
  const [form] = Form.useForm();

  useEffect(() => {
    if (!open) return;
    if (employee) {
      form.setFieldsValue({ ...employee, date_joined: dayjs(employee.date_joined) });
    } else {
      form.resetFields();
    }
  }, [open, employee, form]);

  const onCountryChange = (country) => form.setFieldValue("currency", COUNTRY_CURRENCY[country]);

  const handleOk = async () => {
    const values = await form.validateFields();
    onSubmit({ ...values, date_joined: values.date_joined.format("YYYY-MM-DD") });
  };

  return (
    <Modal
      title={employee ? "Edit Employee" : "Add Employee"}
      open={open}
      onOk={handleOk}
      onCancel={onCancel}
      okText="Save"
    >
      <Form form={form} layout="vertical">
        <Form.Item name="full_name" label="Full name" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="email" label="Email" rules={[{ required: true, type: "email" }]}>
          <Input />
        </Form.Item>
        <Form.Item name="job_title" label="Job title" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="department" label="Department" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="country" label="Country" rules={[{ required: true }]}>
          <Select
            onChange={onCountryChange}
            options={Object.keys(COUNTRY_CURRENCY).map((c) => ({ value: c, label: c }))}
          />
        </Form.Item>
        <Form.Item name="currency" label="Currency" rules={[{ required: true }]}>
          <Input maxLength={3} />
        </Form.Item>
        <Form.Item name="salary" label="Salary" rules={[{ required: true }]}>
          <InputNumber min={1} style={{ width: "100%" }} />
        </Form.Item>
        <Form.Item name="date_joined" label="Date joined" rules={[{ required: true }]}>
          <DatePicker style={{ width: "100%" }} />
        </Form.Item>
      </Form>
    </Modal>
  );
}